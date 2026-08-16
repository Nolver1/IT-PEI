/**
 * Lógica del frontend para el formulario de generación de documentos PEI
 */

// Elementos del DOM
const formulario = document.getElementById('formularioPEI');
const btnLimpiar = document.getElementById('btnLimpiar');
const btnGenerar = document.getElementById('btnGenerar');
const loading = document.getElementById('loading');
const resultados = document.getElementById('resultados');
const btnNuevoFormulario = document.getElementById('btnNuevoFormulario');

// Establecer fecha actual por defecto
window.addEventListener('DOMContentLoaded', () => {
    const hoy = new Date().toISOString().split('T')[0];
    document.getElementById('fechaHoy').value = hoy;
});

/**
 * Validar formato del periodo PEI
 */
document.getElementById('periodoPEI').addEventListener('input', (e) => {
    const valor = e.target.value;
    const patron = /^\d{4}-\d{4}$/;
    
    if (valor && !patron.test(valor)) {
        e.target.setCustomValidity('Formato inválido. Use: YYYY-YYYY (Ej: 2026-2030)');
    } else if (valor && patron.test(valor)) {
        const [inicio, fin] = valor.split('-').map(Number);
        if (fin <= inicio) {
            e.target.setCustomValidity('El año final debe ser mayor que el año inicial');
        } else if (fin - inicio !== 4) {
            e.target.setCustomValidity('El periodo debe ser de 5 años (Ej: 2026-2030)');
        } else {
            e.target.setCustomValidity('');
        }
    } else {
        e.target.setCustomValidity('');
    }
});

/**
 * Validar código de pliego
 */
document.getElementById('codigoPliego').addEventListener('input', (e) => {
    const valor = e.target.value;
    if (valor && !/^\d{6}$/.test(valor)) {
        e.target.setCustomValidity('Debe contener exactamente 6 dígitos');
    } else {
        e.target.setCustomValidity('');
    }
});

/**
 * Limpiar formulario
 */
btnLimpiar.addEventListener('click', () => {
    if (confirm('¿Está seguro de que desea limpiar todos los campos del formulario?')) {
        formulario.reset();
        // Restablecer fecha actual
        const hoy = new Date().toISOString().split('T')[0];
        document.getElementById('fechaHoy').value = hoy;
        
        // Ocultar resultados si están visibles
        resultados.classList.add('hidden');
        formulario.classList.remove('hidden');
    }
});

/**
 * Enviar formulario
 */
formulario.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Validar formulario
    if (!formulario.checkValidity()) {
        formulario.reportValidity();
        return;
    }
    
    // Recopilar datos del formulario
    const formData = new FormData(formulario);
    const datos = {};
    
    formData.forEach((value, key) => {
        datos[key] = value;
    });
    
    console.log('Datos a enviar:', datos);
    
    // Mostrar loading
    loading.classList.remove('hidden');
    btnGenerar.disabled = true;
    btnLimpiar.disabled = true;
    
    try {
        // Enviar petición al servidor
        const response = await fetch('/api/generar-documentos', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(datos)
        });
        
        const resultado = await response.json();
        
        if (!response.ok) {
            throw new Error(resultado.error || 'Error al generar documentos');
        }
        
        console.log('Respuesta del servidor:', resultado);
        
        // Mostrar resultados
        mostrarResultados(resultado.archivos);
        
    } catch (error) {
        console.error('Error:', error);
        alert(`Error al generar documentos: ${error.message}\n\nPor favor, intente nuevamente.`);
        btnGenerar.disabled = false;
        btnLimpiar.disabled = false;
    } finally {
        loading.classList.add('hidden');
    }
});

/**
 * Mostrar resultados con los archivos generados
 */
function mostrarResultados(archivos) {
    // Ocultar formulario
    formulario.classList.add('hidden');
    
    // Configurar enlaces de descarga
    const btnDescargarIT = document.getElementById('btnDescargarIT');
    const btnDescargarOficio = document.getElementById('btnDescargarOficio');
    const nombreIT = document.getElementById('nombreIT');
    const nombreOficio = document.getElementById('nombreOficio');
    
    // Informe Técnico
    btnDescargarIT.href = archivos.informeTecnico.url;
    btnDescargarIT.download = archivos.informeTecnico.nombre;
    nombreIT.textContent = archivos.informeTecnico.nombre;
    
    // Oficio
    btnDescargarOficio.href = archivos.oficio.url;
    btnDescargarOficio.download = archivos.oficio.nombre;
    nombreOficio.textContent = archivos.oficio.nombre;
    
    // Mostrar sección de resultados
    resultados.classList.remove('hidden');
    
    // Scroll hacia resultados
    resultados.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Botón para generar nuevos documentos
 */
btnNuevoFormulario.addEventListener('click', () => {
    resultados.classList.add('hidden');
    formulario.classList.remove('hidden');
    formulario.reset();
    
    // Restablecer fecha actual
    const hoy = new Date().toISOString().split('T')[0];
    document.getElementById('fechaHoy').value = hoy;
    
    // Habilitar botones
    btnGenerar.disabled = false;
    btnLimpiar.disabled = false;
    
    // Scroll hacia arriba
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

/**
 * Validación en tiempo real para números
 */
const inputsNumericos = ['numeroRevisiones', 'numeroOEI', 'numeroAEI'];
inputsNumericos.forEach(id => {
    const input = document.getElementById(id);
    input.addEventListener('input', (e) => {
        const valor = parseInt(e.target.value);
        if (valor < 1) {
            e.target.setCustomValidity('El valor debe ser mayor o igual a 1');
        } else {
            e.target.setCustomValidity('');
        }
    });
});

/**
 * Autocompletar campos de prueba (solo para desarrollo)
 * Descomentar para facilitar pruebas
 */
/*
function autocompletarPrueba() {
    document.getElementById('periodoPEI').value = '2026-2030';
    document.getElementById('nombreMunicipalidad').value = 'Municipalidad Distrital de San Isidro';
    document.getElementById('codigoPliego').value = '301534';
    document.getElementById('departamento').value = 'Lima';
    document.getElementById('provincia').value = 'Lima';
    document.getElementById('nombreRepresentante').value = 'Juan Carlos Pérez Flores';
    document.getElementById('cargoRepresentante').value = 'Alcalde';
    document.getElementById('numeroOficioMunicipalidad').value = '012-2026-MDSI/A';
    document.getElementById('numeroExpediente').value = '2025-01234';
    document.getElementById('numeroResolucionGrupoTrabajo').value = '045-2025-MDSI/A';
    document.getElementById('ordenanzaPlanDesarrollo').value = '015-2024-MDSI';
    document.getElementById('numeroRevisiones').value = '3';
    document.getElementById('planDesarrolloConcertado').value = 'Plan de Desarrollo Local Concertado del Distrito de San Isidro 2023-2030';
    document.getElementById('numeroOEI').value = '5';
    document.getElementById('numeroAEI').value = '15';
    document.getElementById('nombreEspecialista').value = 'Lleny García Flores';
    document.getElementById('fechaOficioMunicipalidad').value = '2026-01-15';
}

// Llamar función de prueba al presionar Ctrl+Shift+T
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.shiftKey && e.key === 'T') {
        autocompletarPrueba();
    }
});
*/
