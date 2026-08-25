@echo off
REM Instalacion completa del MCP server del taller (Windows).
REM - Instala uv si no esta presente.
REM - Sincroniza las dependencias del server.
REM - Verifica que el server arranca correctamente.
REM
REM Uso: abre "Simbolo del sistema" (cmd) en esta carpeta y ejecuta:
REM   install.bat

setlocal enabledelayedexpansion
set "SCRIPT_DIR=%~dp0"
set "SERVER_DIR=%SCRIPT_DIR%mcp-server"

echo [info] Verificando uv...
REM uv se instala en %USERPROFILE%\.local\bin, que puede no estar en el PATH de
REM esta sesion. Lo agregamos ANTES de verificar, para detectar instalaciones
REM previas y hacer el script idempotente (soporta reejecuciones).
set "PATH=%USERPROFILE%\.local\bin;%PATH%"

where uv >nul 2>nul
if errorlevel 1 (
    echo [info] uv no encontrado. Instalando...
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

    REM Reafirmar el PATH tras instalar (el instalador no refresca esta sesion).
    set "PATH=%USERPROFILE%\.local\bin;!PATH!"

    where uv >nul 2>nul
    if errorlevel 1 (
        echo [error] No se pudo instalar uv automaticamente.
        echo         Instalalo manualmente: https://docs.astral.sh/uv/getting-started/installation/
        echo         Si ya lo instalaste, cierra y reabre cmd y vuelve a ejecutar .\install.bat
        exit /b 1
    )
    echo [ok] uv instalado.
) else (
    echo [ok] uv ya esta instalado.
)

echo [info] Instalando dependencias del MCP server (uv sync)...
cd /d "%SERVER_DIR%"
uv sync
if errorlevel 1 (
    echo [error] Fallo uv sync.
    exit /b 1
)
echo [ok] Dependencias instaladas.

echo [info] Verificando que el server arranca...
uv run python -c "import server, tools.chilean_data; print('tools cargadas OK')"
if errorlevel 1 (
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
