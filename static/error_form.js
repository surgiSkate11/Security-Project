// Script para vista previa dinámica de íconos en formularios (usado en módulos y otros forms)

document.addEventListener('DOMContentLoaded', function() {
    // Busca el input del icono y el contenedor de vista previa
    const iconInput = document.querySelector('input[name="icon"]');
    const iconPreview = document.getElementById('iconPreview');

    if (iconInput && iconPreview) {
        function updateIconPreview() {
            const iconClass = iconInput.value.trim();
            if (iconClass) {
                iconPreview.className = iconClass + ' text-3xl text-blue-600 dark:text-blue-400';
            } else {
                iconPreview.className = 'bi bi-x-octagon text-3xl text-gray-400';
            }
        }
        // Inicializa la vista previa al cargar
        updateIconPreview();
        // Actualiza la vista previa en tiempo real
        iconInput.addEventListener('input', updateIconPreview);
        iconInput.addEventListener('keyup', updateIconPreview);
        iconInput.addEventListener('change', updateIconPreview);
    }
});