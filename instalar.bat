@echo off
echo ============================================================
echo INSTALACION DEL GENERADOR DE DOCUMENTOS PEI - CEPLAN
echo Version Python
echo ============================================================
echo.

REM Verificar si Python esta instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no esta instalado
    echo.
    echo Por favor descargue e instale Python desde:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANTE: Durante la instalacion, marque la opcion:
    echo "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo [OK] Python detectado
python --version
echo.

REM Verificar si pip esta instalado
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] pip no esta instalado
    pause
    exit /b 1
)

echo [OK] pip detectado
pip --version
echo.

REM Instalar dependencias
echo ============================================================
echo Instalando librerias de Python...
echo ============================================================
echo.

pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Hubo un problema al instalar las dependencias
    echo Intentando con --break-system-packages...
    echo.
    pip install -r requirements.txt --break-system-packages
)

echo.
echo ============================================================
echo INSTALACION COMPLETADA EXITOSAMENTE
echo ============================================================
echo.
echo Para iniciar el servidor, ejecute:
echo   python app.py
echo.
echo O simplemente haga doble clic en:
echo   iniciar.bat
echo.
echo Luego abra su navegador en:
echo   http://localhost:5000
echo.
pause
