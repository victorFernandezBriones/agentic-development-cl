@echo off
REM Instalacion completa del MCP server del taller (Windows).
REM - Instala uv si no esta presente.
REM - Sincroniza las dependencias del server.
REM - Verifica que el server arranca correctamente.
REM
REM Uso (doble clic o desde cmd):
REM   install.bat

setlocal
set "SCRIPT_DIR=%~dp0"
set "SERVER_DIR=%SCRIPT_DIR%mcp-server"

echo [info] Verificando uv...
where uv >nul 2>nul
if %ERRORLEVEL%==0 (
    echo [ok] uv ya esta instalado.
) else (
    echo [info] uv no encontrado. Instalando...
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    where uv >nul 2>nul
    if not %ERRORLEVEL%==0 (
        echo [error] No se pudo instalar uv. Instalalo manualmente:
        echo         https://docs.astral.sh/uv/getting-started/installation/
        echo [error] Cierra y reabre la terminal si acabas de instalar uv, para refrescar el PATH.
        exit /b 1
    )
    echo [ok] uv instalado.
)

echo [info] Instalando dependencias del MCP server (uv sync)...
cd /d "%SERVER_DIR%"
uv sync
if not %ERRORLEVEL%==0 (
    echo [error] Fallo uv sync.
    exit /b 1
)
echo [ok] Dependencias instaladas.

echo [info] Verificando que el server arranca...
uv run python -c "import server, tools.chilean_data; print('tools cargadas OK')"
if not %ERRORLEVEL%==0 (
    echo [error] El server no arranco.
    exit /b 1
)
echo [ok] El server importa y registra las tools correctamente.

echo.
echo [ok] Instalacion completa. El servidor MCP ya esta listo y configurado.
echo [info] Unico paso restante: abre esta carpeta en Kiro (File -^> Open Folder).
echo [info] Kiro detectara el servidor MCP automaticamente. Verifica en el panel 'MCP Servers'.
echo [info] Detalles y ejemplos en README.md
endlocal
