"""
Sistema de Generación Automática de Documentos PEI - CEPLAN
Versión Python con Flask
"""

from flask import Flask, render_template, request, jsonify, send_file
from datetime import datetime
import os
import re
import zipfile
import tempfile
import io

app = Flask(__name__)

TEMPLATE_DOCX_FOLDER = 'templates_docx'


def formatear_fecha(fecha_iso):
    """
    Convierte fecha ISO (YYYY-MM-DD) a formato español (DD de MES de YYYY)
    Ejemplo: 2026-02-11 -> 11 de febrero de 2026
    """
    meses = [
        'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
        'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'
    ]
    try:
        fecha = datetime.strptime(fecha_iso, '%Y-%m-%d')
        return f"{fecha.day} de {meses[fecha.month - 1]} de {fecha.year}"
    except Exception as e:
        raise ValueError(f"Error en formato de fecha: {str(e)}")


def xml_escape(valor):
    """Escapa caracteres especiales XML en un valor de texto"""
    return (str(valor)
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;'))


def reemplazar_en_xml(xml_content, marcadores):
    """
    Reemplaza marcadores «Nombre» en el XML de un documento Word.

    Aplica dos pre-procesos y tres pasos de reemplazo:

    Pre-proceso 1 — Elimina <w:proofErr/> (marcadores del corrector ortográfico
    de Word que fragmentan runs sin afectar contenido ni formato).

    Pre-proceso 2 — Consolida marcadores partidos en 3 runs:
      run1:<w:t>texto«</w:t>  run2:<w:t>Nombre</w:t>  run3:<w:t>»texto</w:t>
    Los fusiona en un solo <w:t>texto«Nombre»texto</w:t>.

    Paso 1 — Word MERGEFIELD (sección Asunto del IT):
      <fldChar begin/> MERGEFIELD Nombre <fldChar separate/>
      <w:t>«Nombre»</w:t> <fldChar end/>

    Paso 2 — Marcador partido entre dos runs (diferente rsidRPr):
      <w:t>«Nombre</w:t></w:r>  <w:r...><w:t>»</w:t></w:r>

    Paso 3 — Marcador simple en un solo <w:t>:
       <w:t>«Nombre»</w:t>  o  <w:t>texto «Nombre» más texto</w:t>
       El caso más común en el cuerpo del documento.

    Nota: También elimina <w:proofErr/> (corrector ortográfico de Word) que pueden
    fragmentar runs adicionales. Estos elementos no afectan el contenido ni el formato.
    """
    result = xml_content

    # ── Pre-proceso 1: Eliminar proofErr ─────────────────────────────────────
    # Word inserta <w:proofErr/> (corrector ortográfico) entre runs, fragmentando
    # marcadores. Al eliminarlos, los runs quedan adyacentes para el siguiente paso.
    result = re.sub(r'<w:proofErr[^/]*/>', '', result)

    # ── Pre-proceso 2: Consolidar marcadores partidos en 3 runs ──────────────
    # Ocurre cuando Word parte «Nombre» en tres runs separados:
    #   run1: <w:t>texto«</w:t></w:r>
    #   run2: <w:t>Nombre_Marcador</w:t></w:r>
    #   run3: <w:t>»texto</w:t></w:r>
    # Los fusionamos en un solo <w:t>texto«Nombre_Marcador»texto</w:t>
    # para que los pasos siguientes puedan tratarlos como marcadores simples.
    RUN_INTER = r'</w:t></w:r><w:r[^>]*>(?:<w:rPr>(?:<w:[^>]+/>)*</w:rPr>)?<w:t[^>]*>'
    p_3run = (r'<w:t[^>]*>([^«»<]*)«' +
              RUN_INTER +
              r'([^«»<]+)' +
              RUN_INTER +
              r'»([^<]*)</w:t>')
    def merge_3run(m):
        return f'<w:t>{m.group(1)}«{m.group(2)}»{m.group(3)}</w:t>'
    result = re.sub(p_3run, merge_3run, result)

    for nombre, valor in marcadores.items():
        valor_escaped = xml_escape(valor)

        # ── Paso 1: MERGEFIELD de Word ────────────────────────────────────────
        # Estructura: ...MERGEFIELD Nombre...<fldChar separate/><w:t>valor</w:t><fldChar end/>
        def replacer_mf(m, v=valor_escaped):
            return f'{m.group(1)}<w:t>{v}</w:t>{m.group(2)}'

        pattern_mf = (
            r'(MERGEFIELD\s+' + re.escape(nombre) + r'\s[^<]*'
            r'<w:fldChar w:fldCharType="separate"/>)'
            r'<w:t[^>]*>[^<]*</w:t>'
            r'(<w:fldChar w:fldCharType="end"/>)'
        )
        result = re.sub(pattern_mf, replacer_mf, result)

        # ── Paso 2: Marcador partido entre dos runs ───────────────────────────
        # Ocurre cuando «Nombre está en un <w:t> y » en otro <w:t> de otro run
        # (por diferencias en rsidRPr u otros atributos de run, sin proofErr).
        pattern_cross = (
            r'(<w:t[^>]*>)'
            r'([^«»<]*)'
            r'«' + re.escape(nombre) +
            r'[^«»<]*'
            r'</w:t></w:r>'
            r'(?:<w:r[^>]*>(?:<w:rPr>[^<]*(?:<w:[^>]+/>[^<]*)*</w:rPr>)?<w:t[^>]*>[^«»<]*)*'
            r'»'
            r'([^<]*)'
            r'(?:</w:t>(?:</w:r>)?)?'
        )

        def replacer_cross(m, v=valor_escaped):
            return f'{m.group(1)}{m.group(2)}{v}{m.group(3)}</w:t></w:r>'

        result = re.sub(pattern_cross, replacer_cross, result)

        # ── Paso 3: Marcador simple en un solo run (caso estándar) ───────────
        # Cubre la mayoría de casos, incluyendo marcadores con texto adicional
        # en el mismo <w:t>, por ejemplo: «Numero_Expediente»)
        result = result.replace(f'«{nombre}»', valor_escaped)

    return result


def generar_documento_en_memoria(template_path, marcadores):
    """
    Genera un documento Word en memoria (sin escribir en disco).
    Devuelve un objeto BytesIO listo para enviar al navegador.
    Preserva íntegramente el formato original: negritas, colores, sombreados, etc.
    """
    buffer = io.BytesIO()

    with tempfile.TemporaryDirectory() as tmpdir:
        # Descomprimir el .docx
        with zipfile.ZipFile(template_path, 'r') as z:
            z.extractall(tmpdir)

        # Procesar todos los archivos XML relevantes
        for xml_name in [
            'word/document.xml',
            'word/header1.xml',
            'word/header2.xml',
            'word/footer1.xml',
            'word/footer2.xml',
        ]:
            archivo_xml = os.path.join(tmpdir, xml_name)
            if not os.path.exists(archivo_xml):
                continue
            with open(archivo_xml, 'r', encoding='utf-8') as f:
                contenido = f.read()
            contenido_nuevo = reemplazar_en_xml(contenido, marcadores)
            with open(archivo_xml, 'w', encoding='utf-8') as f:
                f.write(contenido_nuevo)

        # Comprimir directamente al buffer en memoria
        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as z:
            for root, dirs, files in os.walk(tmpdir):
                for file in files:
                    filepath = os.path.join(root, file)
                    arcname = os.path.relpath(filepath, tmpdir)
                    z.write(filepath, arcname)

    buffer.seek(0)
    return buffer


# Almacén temporal en memoria: { nombre_archivo: BytesIO }
_documentos_en_memoria = {}


@app.route('/')
def index():
    """Página principal con el formulario"""
    return render_template('index.html')


@app.route('/api/generar-documentos', methods=['POST'])
def generar_documentos():
    """Endpoint para generar los documentos PEI"""
    try:
        datos_form = request.json

        print("=" * 80)
        print("📥 Solicitud recibida para generar documentos")
        print("=" * 80)

        # Validar campos obligatorios
        campos_obligatorios = [
            'fechaHoy', 'periodoPEI', 'fechaOficioMunicipalidad',
            'nombreMunicipalidad', 'codigoPliego', 'departamento', 'provincia',
            'nombreRepresentante', 'cargoRepresentante', 'numeroOficioMunicipalidad',
            'numeroExpediente', 'numeroResolucionGrupoTrabajo', 'ordenanzaPlanDesarrollo',
            'numeroRevisiones', 'planDesarrolloConcertado', 'numeroOEI', 'numeroAEI',
            'nombreEspecialista'
        ]

        campos_faltantes = [c for c in campos_obligatorios if c not in datos_form]
        if campos_faltantes:
            return jsonify({
                'success': False,
                'error': 'Campos obligatorios faltantes',
                'camposFaltantes': campos_faltantes
            }), 400

        # Formatear fechas
        try:
            fecha_hoy_formateada = formatear_fecha(datos_form['fechaHoy'])
            fecha_oficio_formateada = formatear_fecha(datos_form['fechaOficioMunicipalidad'])
        except ValueError as e:
            return jsonify({'success': False, 'error': str(e)}), 400

        # Contexto de marcadores (nombre_marcador -> valor)
        context = {
            'Fecha_Hoy':                                fecha_hoy_formateada,
            'Nombre_Especialista':                      datos_form['nombreEspecialista'],
            'Numero_Oficio_Municipalidad':              datos_form['numeroOficioMunicipalidad'],
            'Numero_Expediente':                        datos_form['numeroExpediente'],
            'Fecha_Oficio_Municipalidad':               fecha_oficio_formateada,
            'Nombre_Representante_Municipalidad':       datos_form['nombreRepresentante'],
            'Cargo_Representante_Municipalidad':        datos_form['cargoRepresentante'],
            'Nombre_Municipalidad':                     datos_form['nombreMunicipalidad'],
            'Periodo_PEI':                              datos_form['periodoPEI'],
            'Codigo_Pliego':                            datos_form['codigoPliego'],
            'Numero_Resolucion_Grupo_Trabajo':          datos_form['numeroResolucionGrupoTrabajo'],
            'Numero_Revisiones':                        datos_form['numeroRevisiones'],
            'Plan_Desarrollo_Concertado_Inmediato_Sup': datos_form['planDesarrolloConcertado'],
            'Ordenanza_Plan_Desarrollo_Concertado':     datos_form['ordenanzaPlanDesarrollo'],
            'Numero_OEI':                               datos_form['numeroOEI'],
            'Numero_AEI':                               datos_form['numeroAEI'],
            'Provincia':                                datos_form['provincia'],
            'Departamento':                             datos_form['departamento'],
        }

        # Nombres de archivo con timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        nombre_it     = f'Informe_Tecnico_PEI_{timestamp}.docx'
        nombre_oficio = f'Oficio_PEI_{timestamp}.docx'

        # Rutas de plantillas
        template_it     = os.path.join(TEMPLATE_DOCX_FOLDER, 'IT_PEI_formulado.docx')
        template_oficio = os.path.join(TEMPLATE_DOCX_FOLDER, 'Oficio_PEI_Formulado.docx')

        print("📝 Generando documentos en memoria...")

        # Generar en memoria (sin tocar el disco)
        _documentos_en_memoria[nombre_it]     = generar_documento_en_memoria(template_it, context)
        _documentos_en_memoria[nombre_oficio] = generar_documento_en_memoria(template_oficio, context)

        print("✅ Documentos generados exitosamente")
        print(f"   Informe Técnico: {nombre_it}")
        print(f"   Oficio:          {nombre_oficio}")
        print("=" * 80)

        return jsonify({
            'success': True,
            'message': 'Documentos generados exitosamente',
            'archivos': {
                'informeTecnico': {
                    'nombre': nombre_it,
                    'url': f'/descargar/{nombre_it}'
                },
                'oficio': {
                    'nombre': nombre_oficio,
                    'url': f'/descargar/{nombre_oficio}'
                }
            }
        })

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'detalles': str(e)
        }), 500


@app.route('/descargar/<filename>')
def descargar_archivo(filename):
    """Endpoint para descargar documentos generados (servidos desde memoria)"""
    buffer = _documentos_en_memoria.get(filename)
    if buffer is None:
        return jsonify({'error': 'Archivo no encontrado'}), 404

    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )


@app.route('/api/health')
def health():
    """Endpoint de salud del servidor"""
    return jsonify({
        'status': 'ok',
        'message': 'Servidor funcionando correctamente',
        'timestamp': datetime.now().isoformat()
    })


if __name__ == '__main__':
    print("=" * 80)
    print("🚀 SERVIDOR DE GENERACIÓN DE DOCUMENTOS PEI INICIADO")
    print("=" * 80)
    print("📍 URL: http://localhost:5000")
    print("🕐 Hora de inicio:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("=" * 80)
    print("\nPresiona Ctrl+C para detener el servidor\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
