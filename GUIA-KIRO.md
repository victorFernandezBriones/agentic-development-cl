# Guía: conectar el MCP server a Kiro

Esta guía asume que ya ejecutaste la instalación (`./install.sh` en macOS/Linux
o `install.bat` en Windows). Si no, hazlo primero.

## Paso 1: abrir el repo como workspace en Kiro

Abre en Kiro la carpeta **raíz de este repositorio** (`agentic-development-cl`),
no una carpeta superior. Esto es importante: el repo trae la configuración del
MCP en `.kiro/settings/mcp.json`, y Kiro solo la lee si esta carpeta es el
workspace.

Al abrirla, Kiro detecta automáticamente la configuración y arranca el server
`servidor-chile-datos-publicos`. No necesitas crear ni editar ningún archivo.

## Paso 2: verificar que el server está conectado

1. Abre el panel **MCP Servers** en la barra lateral de Kiro.
2. Deberías ver `servidor-chile-datos-publicos` en estado **conectado**, con sus
   cuatro herramientas:
   - `search_datasets`
   - `list_dataset_resource`
   - `preview_resource`
   - `get_resource_data`

Si aparece en error, ve a la sección de solución de problemas más abajo.

## Paso 3: probarlo

Pídele a Kiro algo como:

> Busca datasets de establecimientos de salud en formato CSV y muéstrame las
> columnas del principal.

Kiro debería invocar `search_datasets` y luego `preview_resource`. Verás las
llamadas a las herramientas en la conversación.

## Cómo está configurado (referencia)

La configuración ya viene en el repo, en `.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "servidor-chile-datos-publicos": {
      "command": "uv",
      "args": ["--directory", "mcp-server", "run", "main.py"],
      "disabled": false,
      "autoApprove": [
        "search_datasets",
        "list_dataset_resource",
        "preview_resource",
        "get_resource_data"
      ]
    }
  }
}
```

- **`command: "uv"`** y **`--directory mcp-server`**: Kiro lanza el server con uv
  dentro de la carpeta `mcp-server`. La ruta es relativa al workspace, por eso
  funciona en cualquier máquina sin editar nada.
- **`autoApprove`**: las cuatro herramientas son de solo lectura (consultan
  datos.gob.cl, no modifican nada), así que se ejecutan sin pedir confirmación.

## Solución de problemas

**El server aparece en estado de error o "no conectado".**
- Verifica que abriste la carpeta raíz del repo como workspace.
- Confirma que `uv` está en el PATH: abre una terminal y ejecuta `uv --version`.
  Si no lo reconoce, cierra y reabre Kiro (y la terminal) para refrescar el PATH
  tras instalar uv.
- Reconecta el server desde el panel MCP Servers (botón de recargar).

**Las herramientas no aparecen aunque el server esté conectado.**
- Reconecta el server para que recargue la lista de herramientas.
- Revisa el panel de salida/logs del MCP en Kiro: los mensajes del server van a
  stderr y ahí verás si hubo algún error al cargar las tools.

**Kiro usa `curl` o la terminal en vez del MCP.**
- El repo incluye un archivo de steering (`.kiro/steering/uso-datos-chile.md`)
  que instruye a Kiro a preferir el MCP. Debe cargarse solo al abrir el
  workspace.
- Sé específico en la petición: menciona "datasets" o "datos.gob.cl".
- Es un comportamiento del modelo, no siempre 100% garantizable. Si insiste,
  pídele explícitamente: "usa las herramientas del MCP servidor-chile-datos-publicos".

**Verificar el server por fuera de Kiro.**
Desde la raíz del repo:

```bash
uv --directory mcp-server run python -c "import server, tools.chilean_data; print('OK')"
```

Si imprime `OK`, el server está sano y el problema está en la conexión con Kiro,
no en el código.
