# Agentic Development CL — Taller

Taller práctico para construir aplicaciones sobre datos públicos del Estado de
Chile usando **Kiro** y un **servidor MCP** que actúa como puente hacia el
[Portal de Datos Abiertos](https://datos.gob.cl).

## Qué vas a aprender

- Cómo un servidor MCP expone datos externos como herramientas para un agente.
- Cómo Kiro descubre e invoca esas herramientas.
- Cómo usar los datos obtenidos para construir una app (por ejemplo, en Streamlit)
  que resuelva un caso de negocio simple.

## Arquitectura

```
Kiro (IDE)  ──MCP (stdio)──►  MCP server (este repo)  ──HTTP──►  datos.gob.cl
```

- **Kiro** es el agente: descubre las herramientas del MCP y las usa.
- **El MCP server** es el puente: busca datasets, lista sus archivos e inspecciona
  su contenido.
- **La app que construyas** consume los datos directamente usando las URLs que
  entrega el MCP.

## Requisitos previos

- [Kiro](https://kiro.dev) instalado.
- Conexión a internet (para consultar datos.gob.cl).
- No necesitas tener Python ni uv preinstalados: el script de instalación se
  encarga de uv y las dependencias.

## Puesta en marcha (3 pasos)

### 1. Clonar el repositorio

```bash
git clone <URL-del-repo>
cd agentic-development-cl
```

### 2. Instalar

macOS / Linux:

```bash
./install.sh
```

Windows:

```bat
install.bat
```

El script instala `uv` si falta, crea el entorno del server, instala las
dependencias y verifica que todo arranca.

### 3. Conectar a Kiro

Abre esta carpeta como workspace en Kiro y sigue **[GUIA-KIRO.md](GUIA-KIRO.md)**.
La configuración del MCP ya viene incluida en el repo, así que Kiro lo detecta
automáticamente.

## Herramientas que expone el MCP

| Herramienta | Qué hace |
|---|---|
| `search_datasets` | Busca datasets por palabra clave (filtro opcional de formato). |
| `list_dataset_resource` | Lista los archivos de un dataset con sus URLs. |
| `preview_resource` | Muestra columnas y filas de muestra de un archivo tabular. |
| `get_resource_data` | Descarga un archivo tabular completo y limpio. |

## Estructura del repositorio

```
agentic-development-cl/
├── mcp-server/             # El servidor MCP (código fuente)
│   ├── main.py             # entry point (stdio)
│   ├── server.py           # instancia FastMCP compartida
│   ├── tools/              # las 4 herramientas MCP
│   ├── utils/              # cliente HTTP
│   └── pyproject.toml      # dependencias (uv)
├── .kiro/
│   ├── settings/mcp.json   # configuración del MCP (Kiro la lee al abrir el repo)
│   └── steering/           # guía de comportamiento para Kiro
├── install.sh              # instalación macOS/Linux
├── install.bat             # instalación Windows
├── GUIA-KIRO.md            # cómo conectar y probar el MCP en Kiro
└── README.md               # este archivo
```

## Idea de ejercicio

1. Pídele a Kiro que busque un dataset de un tema que te interese
   (salud, educación, transporte, seguridad...).
2. Inspecciona su estructura con las herramientas del MCP.
3. Pídele a Kiro que construya una app Streamlit que consuma ese dataset y
   muestre algo útil: un gráfico, un filtro por región, un indicador.

El servidor MCP te da el contexto; Kiro escribe el código; tú diseñas el caso
de uso.
