@echo off
call env.bat

:: Cambia al directorio del proyecto
cd /d "%PROJECT_DIR%" >nul 2>&1

:: Comprueba si el entorno virtual ya existe
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo.
    echo El entorno virtual no existe. Creando uno nuevo...
    python -m venv "%VENV_DIR%" >nul 2>&1
    if errorlevel 1 (
        echo Error al crear el entorno virtual.
        exit /b
    )
)
echo.
echo Entorno virtual listo.

:: Activa el entorno virtual
call "%VENV_DIR%\Scripts\activate" >nul 2>&1
if errorlevel 1 (
    echo Error al activar el entorno virtual.
    exit /b
)
echo.
echo Entorno activado correctamente.

:: Comprueba si las dependencias ya están instaladas
pip show -q python-telegram-bot >nul 2>&1
if errorlevel 1 (
    echo.
    echo Instalando dependencias...
    pip install -r requirements.txt >nul 2>&1
    if errorlevel 1 (
        echo Error al instalar las dependencias.
        exit /b
    )
)
echo.
echo Dependencias listas.

:: Ejecuta el bot
echo.
echo Iniciando el bot...
python "%BOT_SCRIPT%"

:: Mensaje de cierre
pause
