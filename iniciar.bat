@echo off
echo ============================================================
echo GENERADOR DE DOCUMENTOS PEI - CEPLAN
echo Version Python
echo ============================================================
echo.

REM Verificar si Python esta instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no esta instalado
    echo.
    echo Por favor ejecute primero: instalar.bat
    echo.
    pause
    exit /b 1
)

REM Verificar si las dependencias estan instaladas
pip show Flask >nul 2>&1
if %errorlevel% neq 0 (
    echo [AVISO] Dependencias no instaladas
    echo.
    echo Ejecutando instalacion automatica...
    echo.
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        pip install -r requirements.txt --break-system-packages
    )
    echo.
)

echo Iniciando servidor...
echo.
echo Una vez que vea el mensaje "SERVIDOR INICIADO",
echo abra su navegador en: http://localhost:5000
echo.
echo Presione Ctrl+C para detener el servidor
echo.
echo ============================================================
echo.

python app.py
