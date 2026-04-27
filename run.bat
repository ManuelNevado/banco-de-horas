@echo off
cd /d "%~dp0"

:: Crear venv si no existe
if not exist ".venv\Scripts\activate.bat" (
    echo Creando entorno virtual...
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: No se encontro Python. Instala Python 3.11+ y vuelve a intentarlo.
        pause
        exit /b 1
    )
)

:: Activar venv
call .venv\Scripts\activate.bat

:: Instalar dependencias si streamlit no esta instalado
python -m streamlit --version >nul 2>&1
if errorlevel 1 (
    echo Instalando dependencias...
    pip install -r requirements.txt
)

:: Arrancar la app
python -m streamlit run app.py

pause
