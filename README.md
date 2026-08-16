# 🏛️ Generador Automático de Documentos PEI - CEPLAN (Versión Python)

Sistema web para la generación automática de documentos del Plan Estratégico Institucional (PEI) desarrollado en **Python + Flask**.

## 📋 Descripción

Este sistema permite generar automáticamente dos documentos oficiales:

1. **Informe Técnico PEI** - Documento de validación técnica
2. **Oficio PEI** - Documento de comunicación oficial

## 🎯 ¿Por qué esta versión?

Esta es la **versión Python** del sistema, diseñada para usuarios que:
- ✅ Ya tienen Python instalado
- ✅ No quieren instalar Node.js
- ✅ Prefieren trabajar con tecnologías Python

## 🛠️ Tecnologías Utilizadas

- **Python 3.8+**
- **Flask 3.0** - Framework web
- **python-docx** - Manipulación de documentos Word
- **docxtpl** - Motor de plantillas para Word

## 📦 Requisitos Previos

- **Python 3.8 o superior**
- **pip** (gestor de paquetes de Python)

### ¿Cómo verificar si tienes Python?

Abre una terminal (CMD en Windows) y ejecuta:

```bash
python --version
```

Deberías ver algo como: `Python 3.10.5` o superior.

Si no tienes Python instalado, descárgalo desde: https://www.python.org/downloads/

**IMPORTANTE en Windows:** Durante la instalación, marca la opción **"Add Python to PATH"**

## 🚀 Instalación

### Windows

1. Extrae la carpeta `generador-pei-python`
2. Haz **doble clic** en: `instalar.bat`
3. Espera a que termine la instalación (1-2 minutos)

### Mac / Linux

```bash
cd generador-pei-python
chmod +x instalar.sh
./instalar.sh
```

### Instalación Manual

```bash
cd generador-pei-python
pip install -r requirements.txt
```

Si da error, intenta:
```bash
pip install -r requirements.txt --break-system-packages
```

## ▶️ Ejecución

### Windows

Haz **doble clic** en: `iniciar.bat`

### Mac / Linux

```bash
python3 app.py
```

### Manual

```bash
python app.py
```

## 🌐 Uso

1. **Abre tu navegador** en: http://localhost:5000
2. **Completa el formulario** con los datos del PEI
3. **Haz clic** en "Generar Documentos"
4. **Descarga** los archivos Word generados

## 📁 Estructura del Proyecto

```
generador-pei-python/
├── app.py                    # Aplicación Flask principal
├── requirements.txt          # Dependencias de Python
├── instalar.bat             # Instalador Windows
├── iniciar.bat              # Iniciador Windows
├── instalar.sh              # Instalador Mac/Linux
├── templates/               # Plantillas HTML (Flask)
│   └── index.html          # Formulario web
├── static/                  # Archivos estáticos
│   ├── styles.css          # Estilos CSS
│   └── app.js              # JavaScript del cliente
├── templates_docx/          # Plantillas Word
│   ├── IT_PEI_formulado.docx
│   └── Oficio_PEI_Formulado.docx
└── output/                  # Documentos generados (creado automáticamente)
```

## 🔧 Dependencias

Las siguientes librerías se instalan automáticamente:

```
Flask==3.0.0              # Framework web
python-docx==1.1.0        # Manipulación de archivos Word
docxtpl==0.16.7           # Motor de plantillas Word
Jinja2==3.1.2             # Motor de plantillas HTML
```

## 📝 Formato de Datos

### Fechas
- **Entrada**: Formato ISO desde selector (YYYY-MM-DD)
- **Salida**: Formato español (DD de MES de YYYY)
- Ejemplo: `2026-02-11` → `11 de febrero de 2026`

### Periodo PEI
- **Formato**: YYYY-YYYY
- **Validación**: Exactamente 5 años
- Ejemplo: `2026-2030` ✅

### Código de Pliego
- **Formato**: 6 dígitos numéricos
- Ejemplo: `301534` ✅

## 🧪 Datos de Prueba

Para probar rápidamente el sistema:

```
Fecha de emisión: 11/02/2026
Periodo PEI: 2026-2030
Fecha oficio: 15/01/2026
Nombre municipalidad: Municipalidad Distrital de San Isidro
Código pliego: 301534
Departamento: Lima
Provincia: Lima
Nombre representante: Juan Carlos Pérez Flores
Cargo: Alcalde
Número oficio: 012-2026-MDSI/A
Número expediente: 2025-01234
Resolución grupo: 045-2025-MDSI/A
Ordenanza PDLC: 015-2024-MDSI
Revisiones: 3
Plan superior: Plan de Desarrollo Local Concertado del Distrito de San Isidro 2023-2030
OEI: 5
AEI: 15
Especialista: Lleny García Flores
```

## 🐛 Solución de Problemas

### "Python no se reconoce como comando"

**Solución:**
1. Reinstala Python desde https://www.python.org/downloads/
2. **IMPORTANTE:** Marca "Add Python to PATH" durante instalación
3. Reinicia tu computadora
4. Verifica con: `python --version`

### "No module named 'flask'"

**Solución:**
```bash
pip install -r requirements.txt
```

Si da error:
```bash
pip install -r requirements.txt --break-system-packages
```

### "Puerto 5000 en uso"

**Solución 1 (cerrar el proceso):**
- Windows: Abre "Administrador de tareas" → Busca "Python" → Finalizar tarea
- Mac/Linux: `killall python`

**Solución 2 (cambiar puerto):**
Edita `app.py` en la última línea:
```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Cambia 5000 por 8080
```

### Error "Template not found"

**Verifica que existen:**
- `templates/index.html`
- `static/styles.css`
- `static/app.js`

### Los documentos no se generan

**Verifica que existen:**
- `templates_docx/IT_PEI_formulado.docx`
- `templates_docx/Oficio_PEI_Formulado.docx`

## 🔒 Seguridad

- Todos los archivos se procesan **localmente**
- No se envían datos a servidores externos
- Los documentos se guardan en la carpeta `output/`
- Recomendación: Limpia periódicamente la carpeta `output/`

## 🆚 Diferencias con la versión Node.js

| Aspecto | Versión Python | Versión Node.js |
|---------|---------------|-----------------|
| Lenguaje | Python 3.8+ | Node.js 18+ |
| Framework | Flask | Express |
| Puerto | 5000 | 3000 |
| Instalación | `pip install -r requirements.txt` | `npm install` |
| Inicio | `python app.py` | `npm start` |
| Librería Word | docxtpl | docxtemplater |

**Ambas versiones son 100% funcionales y generan los mismos documentos.**

## 📊 Flujo del Sistema

```
[Navegador] → [Formulario HTML]
     ↓
[POST /api/generar-documentos]
     ↓
[Flask Backend]
     ↓
[Formatear fechas a español]
     ↓
[docxtpl + python-docx]
     ↓
[Generar 2 archivos .docx]
     ↓
[Guardar en /output/]
     ↓
[Descargar archivos]
```

## 🎓 Comandos Útiles

```bash
# Ver versión de Python
python --version

# Ver paquetes instalados
pip list

# Actualizar pip
python -m pip install --upgrade pip

# Instalar una librería específica
pip install flask

# Desinstalar todas las dependencias
pip uninstall -r requirements.txt -y

# Ver logs del servidor
# (Los logs se muestran en la consola donde ejecutaste python app.py)
```

## 🚀 Despliegue en Producción

Para un entorno de producción, considera usar:

```bash
# Instalar gunicorn
pip install gunicorn

# Ejecutar con gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📞 Soporte

Si encuentras problemas:
1. Revisa la sección "Solución de Problemas"
2. Verifica los logs en la consola
3. Asegúrate de tener Python 3.8+
4. Verifica que todas las carpetas existen

## 📄 Licencia

Sistema desarrollado para el Centro Nacional de Planeamiento Estratégico (CEPLAN) - Perú.

---

**Desarrollado con 🐍 Python para el Sistema Nacional de Planeamiento Estratégico - SINAPLAN**

**Versión: 1.0.0 (Python) | Febrero 2026**
