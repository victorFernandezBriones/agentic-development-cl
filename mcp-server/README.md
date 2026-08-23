# MCP Server — Datos Públicos de Chile

Servidor MCP que expone datos del [Portal de Datos Abiertos de Chile](https://datos.gob.cl)
(API CKAN 3) como herramientas que Kiro puede usar.

## Herramientas

| Herramienta | Qué hace |
|---|---|
| `search_datasets` | Busca datasets por palabra clave, con filtro opcional de formato. |
| `list_dataset_resource` | Lista los archivos de un dataset con sus URLs y flag `is_tabular`. |
| `preview_resource` | Devuelve una muestra de columnas y filas de un archivo tabular. |
| `get_resource_data` | Descarga un archivo tabular completo y limpio como registros. |

## Estructura

```
mcp-server/
├── main.py                 # entry point: configura logging y arranca el server (stdio)
├── server.py               # instancia compartida de FastMCP
├── tools/
│   └── chilean_data.py     # las 4 herramientas MCP
├── utils/
│   └── http_client.py      # cliente HTTP genérico (GET + descarga con límite)
├── pyproject.toml          # dependencias (gestionadas con uv)
└── .env.example            # variables de entorno de ejemplo
```

## Ejecutar de forma aislada (para probar)

```bash
uv sync
uv run main.py
```

Si arranca sin errores y queda esperando, está funcionando por stdio. Corta con `Ctrl+C`.
La configuración para conectarlo a Kiro está en la guía del repositorio raíz.
