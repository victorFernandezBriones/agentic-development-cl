#!/usr/bin/env bash
#
# Instalación completa del MCP server del taller (macOS / Linux).
# - Instala uv si no está presente.
# - Sincroniza las dependencias del server.
# - Verifica que el server arranca correctamente.
#
# Uso:
#   ./install.sh
#
set -euo pipefail

# Directorio de este script (raíz del repo), para funcionar desde cualquier ruta.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVER_DIR="$SCRIPT_DIR/mcp-server"

info()  { printf "\033[0;34m[info]\033[0m %s\n" "$1"; }
ok()    { printf "\033[0;32m[ok]\033[0m %s\n" "$1"; }
warn()  { printf "\033[0;33m[warn]\033[0m %s\n" "$1"; }
err()   { printf "\033[0;31m[error]\033[0m %s\n" "$1" >&2; }

# 1. Verificar / instalar uv
if command -v uv >/dev/null 2>&1; then
    ok "uv ya está instalado ($(uv --version))"
else
    info "uv no encontrado. Instalando..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # uv se instala en ~/.local/bin; agregarlo al PATH de esta sesión.
    export PATH="$HOME/.local/bin:$PATH"
    if command -v uv >/dev/null 2>&1; then
        ok "uv instalado ($(uv --version))"
    else
        err "No se pudo instalar uv. Instálalo manualmente: https://docs.astral.sh/uv/getting-started/installation/"
        exit 1
    fi
fi

# 2. Sincronizar dependencias del server
info "Instalando dependencias del MCP server (uv sync)..."
cd "$SERVER_DIR"
uv sync
ok "Dependencias instaladas."

# 3. Verificar que el server arranca
info "Verificando que el server arranca correctamente..."
# Se le pasa una entrada vacía por stdin: el server inicia y termina sin bloquear.
if echo "" | uv run python -c "import server, tools.chilean_data; print('tools cargadas OK')" >/tmp/mcp_check.log 2>&1; then
    ok "El server importa y registra las tools correctamente."
else
    err "El server no arrancó. Detalle:"
    cat /tmp/mcp_check.log >&2
    exit 1
fi

echo ""
ok "Instalación completa. El servidor MCP ya está listo y configurado."
echo ""
info "Único paso restante: abre esta carpeta en Kiro (File → Open Folder)."
info "Kiro detectará el servidor MCP automáticamente. Verifica en el panel 'MCP Servers'."
info "Detalles y ejemplos en README.md"
