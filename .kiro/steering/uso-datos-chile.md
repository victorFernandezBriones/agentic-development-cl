---
inclusion: always
---

# Uso de datos públicos de Chile

Para CUALQUIER tarea que involucre datos públicos del Estado de Chile
(datasets, datos.gob.cl, salud, educación, presupuesto, transporte, seguridad,
establecimientos, indicadores del sector público chileno), usa SIEMPRE las
herramientas del servidor MCP `servidor-chile-datos-publicos`.

## Herramientas disponibles y cuándo usarlas

1. `search_datasets` — busca datasets. ÚSALA como primer paso. Acepta un filtro
   `format` (ej: "csv") para encontrar datasets con archivos consumibles.
2. `list_dataset_resource` — lista los archivos de un dataset con sus URLs y un
   flag `is_tabular`. Úsala para elegir el recurso correcto.
3. `preview_resource` — inspecciona columnas y filas de muestra de un archivo.
   Acepta `skip_rows` para saltar encabezados no tabulares.
4. `get_resource_data` — descarga el archivo tabular completo y limpio, listo
   para que una app lo consuma.

## Reglas

- NO uses la terminal (curl, wget, scripts con requests) para consultar
  datos.gob.cl cuando exista una herramienta MCP equivalente. Las herramientas
  del MCP ya manejan el filtrado por formato, los encabezados irregulares, los
  separadores y encodings de los CSV chilenos, y la validación de URLs.
- NO adivines URLs de archivos ni construyas nombres con fechas. La herramienta
  `list_dataset_resource` entrega la URL exacta de cada recurso.
- Si un archivo Excel/CSV tiene filas de título antes de la tabla real, usa el
  parámetro `skip_rows` de `preview_resource` o `get_resource_data`, en lugar de
  descargar el archivo manualmente.
- Recurre a la terminal SOLO si el servidor MCP no está disponible o ninguna de
  sus herramientas cubre el caso. Si eso ocurre, indícalo explícitamente antes.

## Objetivo del flujo

El servidor MCP es el puente para descubrir e inspeccionar datos. El código de
la aplicación (por ejemplo una app Streamlit) es quien consume los datos en
tiempo de ejecución usando las URLs que entrega el MCP.
