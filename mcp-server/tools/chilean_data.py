"""
MCP tools sobre el Portal de Datos Abiertos de Chile (datos.gob.cl, API CKAN 3).

Flujo pensado para que Kiro construya apps que consumen estos datos:
    search_datasets      -> encuentra datasets (opcionalmente filtra por formato)
    list_dataset_resource -> lista los archivos de un dataset + URLs + is_tabular
    preview_resource     -> muestra columnas y filas de muestra (inspeccionar estructura)
    get_resource_data    -> descarga el archivo tabular completo, limpio, listo para la app
"""

import io
import ipaddress
import logging
import os
from urllib.parse import urlparse

import pandas as pd
from dotenv import load_dotenv

from server import mcp
from utils import http_client

load_dotenv()

log = logging.getLogger(__name__)

BASE_URL: str = os.getenv("CHILEAN_DATA_API_URL", "https://datos.gob.cl/api/3/action")
TABULAR_FORMATS = {"csv", "xlsx", "xls", "json", "geojson", "ods"}
EXCEL_FORMATS = {"xlsx", "xls", "ods"}


def _validate_url(url: str) -> bool:
    """Evita SSRF: solo HTTP(S) hacia hosts publicos."""
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return False
    host = (parsed.hostname or "").lower()
    if not host or host in {"localhost", "169.254.169.254", "metadata.google.internal"}:
        return False
    try:
        ip = ipaddress.ip_address(host)
        return not (ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved)
    except ValueError:
        return True  # es un dominio, no una IP literal


def _detect_format(url: str, declared_format: str | None) -> str:
    """Determina el formato de un recurso.

    Prioriza el formato declarado por CKAN sobre la extension de la URL,
    porque muchas URLs no terminan en extension limpia
    (ej: .../download/archivo.xlsx?token=abc). Esto evita rechazar
    archivos tabulares validos por culpa de la URL.
    """
    if declared_format:
        return declared_format.strip().lower()
    # Fallback: intentar por extension del path (ignorando query string).
    path = urlparse(url).path
    if "." in path:
        return path.rsplit(".", 1)[-1].lower()
    return ""


def _read_dataframe(content: bytes, fmt: str, skip_rows: int, nrows: int | None) -> pd.DataFrame:
    """Parsea bytes a un DataFrame segun el formato, tolerante a formatos chilenos."""
    if fmt in EXCEL_FORMATS:
        return pd.read_excel(io.BytesIO(content), skiprows=skip_rows, nrows=nrows)

    if fmt == "json":
        return pd.read_json(io.BytesIO(content))

    # CSV: los del Estado chileno varian en separador y encoding.
    attempts = (
        {"sep": ","},
        {"sep": ";"},
        {"sep": ";", "encoding": "latin-1"},
        {"sep": ",", "encoding": "latin-1"},
    )
    last_error: Exception | None = None
    for kwargs in attempts:
        try:
            return pd.read_csv(
                io.BytesIO(content), skiprows=skip_rows, nrows=nrows, **kwargs
            )
        except (UnicodeDecodeError, pd.errors.ParserError) as e:
            last_error = e
            continue
    raise ValueError(f"No se pudo parsear el archivo: {last_error}")


@mcp.tool
def search_datasets(query: str, limit: int = 10, format: str | None = None) -> dict:
    """Busca datasets del Portal de Datos Abiertos de Chile (datos.gob.cl).

    Usa esta herramienta como PRIMER paso ante cualquier consulta sobre datos
    publicos chilenos (salud, educacion, presupuesto, transporte, seguridad).
    Prefiere esta herramienta antes que consultar datos.gob.cl con la terminal:
    ya maneja el filtrado por formato y el formato de respuesta de CKAN.

    Args:
        query: Palabras clave en espanol. Ej: "listas de espera", "presupuesto".
        limit: Maximo de resultados (1-50).
        format: Filtro opcional de formato en minuscula (ej: "csv", "xlsx").
                Usa "csv" cuando el objetivo es construir una app que lea datos.
    """
    limit = max(1, min(limit, 50))
    params: dict = {"q": query, "rows": limit}
    if format:
        # CKAN indexa el formato en minuscula; sin .lower() el filtro no matchea.
        params["fq"] = f"res_format:{format.lower()}"

    log.info("search_datasets query=%r limit=%s format=%s", query, limit, format)
    response = http_client._get(f"{BASE_URL}/package_search", params=params)
    result = response["result"]
    log.info("search_datasets -> %s coincidencias", result["count"])

    return {
        "total_datasets": result["count"],
        "datasets": [
            {
                "id": ds["id"],
                "title": ds["title"],
                "organization": (ds.get("organization") or {}).get("title"),
                "resources_count": ds.get("num_resources", 0),
            }
            for ds in result["results"]
        ],
    }


@mcp.tool
def list_dataset_resource(dataset_id: str) -> dict:
    """Lista los archivos descargables de un dataset y sus URLs.

    Usala despues de search_datasets con el 'id' de un dataset. Los recursos
    con is_tabular=True (CSV/Excel/JSON) pueden leerse como datos; PDF o DOCX
    aparecen listados pero no son consultables como datos.

    Args:
        dataset_id: El 'id' devuelto por search_datasets.
    """
    log.info("list_dataset_resource dataset_id=%s", dataset_id)
    response = http_client._get(f"{BASE_URL}/package_show", params={"id": dataset_id})
    result = response["result"]

    resources = [
        {
            "name": r.get("name"),
            "format": (r.get("format") or "").lower(),
            "url": r.get("url"),
            "is_tabular": (r.get("format") or "").strip().lower() in TABULAR_FORMATS,
        }
        for r in result.get("resources", [])
    ]
    # Tabulares primero: es lo que conviene elegir para construir una app.
    resources.sort(key=lambda r: not r["is_tabular"])

    return {
        "title": result.get("title"),
        "tabular_count": sum(1 for r in resources if r["is_tabular"]),
        "resources": resources,
    }


@mcp.tool
def preview_resource(
    url: str,
    rows: int = 20,
    skip_rows: int = 0,
    format: str | None = None,
) -> dict:
    """Descarga un recurso tabular y devuelve una MUESTRA de columnas y filas.

    Usala para inspeccionar la estructura de un archivo antes de construir una
    app o de descargarlo completo. Si el archivo tiene filas de titulo o notas
    antes de la tabla real, usa skip_rows para saltarlas.

    Args:
        url: URL de descarga obtenida desde list_dataset_resource.
        rows: Filas de muestra a devolver (1-100).
        skip_rows: Filas a saltar al inicio (util para encabezados no tabulares).
        format: Formato del recurso (ej: "xlsx", "csv"). Si se omite, se infiere.
                Pasa aqui el campo 'format' de list_dataset_resource para evitar
                errores por URLs sin extension limpia.
    """
    if not _validate_url(url):
        return {"error": "URL no permitida. Solo URLs HTTP(S) publicas."}

    fmt = _detect_format(url, format)
    if fmt not in TABULAR_FORMATS:
        return {
            "error": f"Formato '{fmt or 'desconocido'}' no es tabular.",
            "hint": "Usa list_dataset_resource y elige un recurso con is_tabular=True. "
            "Si el recurso ES tabular pero la URL no tiene extension, pasa el "
            "parametro 'format' con el valor del campo 'format' del recurso.",
        }

    rows = max(1, min(rows, 100))
    skip_rows = max(0, skip_rows)
    log.info("preview_resource url=%s rows=%s skip_rows=%s fmt=%s", url, rows, skip_rows, fmt)

    try:
        content = http_client.download_bytes(url)
        df = _read_dataframe(content, fmt, skip_rows=skip_rows, nrows=rows + 50)
    except Exception as e:
        return {"error": str(e), "url": url}

    sample = df.head(rows)
    return {
        "columns": [str(c) for c in sample.columns],
        "rows": sample.fillna("").astype(str).to_dict(orient="records"),
        "rows_in_sample": len(sample),
    }


@mcp.tool
def get_resource_data(
    url: str,
    skip_rows: int = 0,
    max_rows: int = 5000,
    format: str | None = None,
) -> dict:
    """Descarga un recurso tabular COMPLETO y lo devuelve limpio como registros.

    A diferencia de preview_resource (que solo muestra una muestra), esta
    herramienta devuelve los datos listos para que una app los consuma o para
    guardarlos como CSV. Usala cuando ya sabes que el recurso es el correcto y
    necesitas los datos, no solo inspeccionarlos.

    Args:
        url: URL de descarga obtenida desde list_dataset_resource.
        skip_rows: Filas a saltar al inicio (encabezados no tabulares).
        max_rows: Tope de filas a devolver (proteccion de contexto, 1-50000).
        format: Formato del recurso (ej: "xlsx", "csv"). Si se omite, se infiere.
    """
    if not _validate_url(url):
        return {"error": "URL no permitida. Solo URLs HTTP(S) publicas."}

    fmt = _detect_format(url, format)
    if fmt not in TABULAR_FORMATS:
        return {
            "error": f"Formato '{fmt or 'desconocido'}' no es tabular.",
            "hint": "Usa list_dataset_resource y elige un recurso con is_tabular=True.",
        }

    skip_rows = max(0, skip_rows)
    max_rows = max(1, min(max_rows, 50000))
    log.info("get_resource_data url=%s skip_rows=%s max_rows=%s fmt=%s", url, skip_rows, max_rows, fmt)

    try:
        content = http_client.download_bytes(url)
        df = _read_dataframe(content, fmt, skip_rows=skip_rows, nrows=max_rows)
    except Exception as e:
        return {"error": str(e), "url": url}

    truncated = len(df) >= max_rows
    return {
        "columns": [str(c) for c in df.columns],
        "row_count": len(df),
        "truncated": truncated,
        "data": df.fillna("").astype(str).to_dict(orient="records"),
    }
