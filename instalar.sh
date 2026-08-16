#!/bin/bash

echo "============================================================"
echo "INSTALACION DEL GENERADOR DE DOCUMENTOS PEI - CEPLAN"
echo "Version Python"
echo "============================================================"
echo ""

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python no está instalado"
    echo ""
    echo "Por favor instale Python 3.8 o superior:"
    echo "  Mac: brew install python3"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo ""
    exit 1
fi

echo "[OK] Python detectado"
python3 --version
echo ""

# Verificar si pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo "[ERROR] pip no está instalado"
    exit 1
fi

echo "[OK] pip detectado"
pip3 --version
echo ""

# Instalar dependencias
echo "============================================================"
echo "Instalando librerías de Python..."
echo "============================================================"
echo ""

pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Hubo un problema al instalar las dependencias"
    echo ""
    exit 1
fi

echo ""
echo "============================================================"
echo "INSTALACION COMPLETADA EXITOSAMENTE"
echo "============================================================"
echo ""
echo "Para iniciar el servidor, ejecute:"
echo "  python3 app.py"
echo ""
echo "Luego abra su navegador en:"
echo "  http://localhost:5000"
echo ""
