document.addEventListener('DOMContentLoaded', function() {
    const togglePanelBtn = document.getElementById('togglePanel');
    const updatePanel = document.getElementById('updatePanel');
    const cancelButton = document.getElementById('cancelButton');

    togglePanelBtn.addEventListener('click', function() {
        const isVisible = updatePanel.style.display === 'block';

        if (!isVisible) {
            updatePanel.style.display = 'block'; // Muestra el panel
            setTimeout(() => {
                updatePanel.classList.add('show'); // Agrega la clase para la animación
            }, 10); // Espera un momento para permitir la transición
        } else {
            updatePanel.classList.remove('show'); // Elimina la clase para la animación
            setTimeout(() => {
                updatePanel.style.display = 'none'; // Oculta después de la animación
            }, 300); // Tiempo que coincide con la duración de la transición
        }
    });

    cancelButton.addEventListener('click', function() {
        updatePanel.classList.remove('show'); // Elimina la clase para la animación
        setTimeout(() => {
            updatePanel.style.display = 'none'; // Oculta después de la animación
        }, 300); // Tiempo que coincide con la duración de la transición
    });
});
