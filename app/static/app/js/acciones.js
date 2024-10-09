document.addEventListener('DOMContentLoaded', function() {
    console.log("El script acciones.js se ha cargado correctamente.");
    document.querySelectorAll('.editar-btn').forEach(button => {
        button.addEventListener('click', function() {
            const id = this.getAttribute('data-id');
            const nombre = this.closest('.card').querySelector('.card-title').innerText;
            const especie = this.closest('.card').querySelector('.card-text:nth-of-type(1)').innerText.split(': ')[1];
            const edad = this.closest('.card').querySelector('.card-text:nth-of-type(2)').innerText.split(': ')[1];
            mostrarDetalles(id, nombre, especie, edad);
        });
    });

    // Función para mostrar detalles de la mascota
    function mostrarDetalles(id, nombre, especie, edad) {
        const detalleDiv = document.getElementById('mascota-detalle');
        detalleDiv.innerHTML = `
            <h5>${nombre}</h5>
            <p>Especie: ${especie}</p>
            <p>Edad: ${edad}</p>
            <p>ID: ${id}</p>
            <button class="btn btn-primary" onclick="editarMascota('${id}')">Guardar Cambios</button>
        `;
    }

    // Lógica para eliminar la mascota
    document.querySelectorAll('.eliminar-btn').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault(); // Evitar el envío del formulario de manera tradicional
            const id = this.closest('form').querySelector('input[name="mascota_id"]').value; // Obtener el ID desde el input hidden
            const confirmacion = confirm("¿Estás seguro de que deseas eliminar esta mascota?");
            if (confirmacion) {
                // Crear un formulario para enviar la solicitud de eliminación
                const formData = new FormData();
                formData.append('mascota_id', id);

                // Enviar la solicitud mediante fetch
                fetch(window.location.href, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'), // Asegúrate de enviar el CSRF token
                    }
                })
                .then(response => {
                    if (response.ok) {
                        // Mostrar mensaje de éxito
                        mostrarMensajeExito();
                        // Eliminar la tarjeta de la mascota del DOM
                        console.log("Eliminando la mascota con ID:", id); // Para depuración
                        this.closest('.col-md-12').remove(); // Cambiado para eliminar el contenedor correcto
                    } else {
                        alert('Error al eliminar la mascota.');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            }
        });
    });

    function mostrarMensajeExito() {
        const mensajeExito = document.getElementById('mensaje-exito');
        mensajeExito.classList.remove('d-none');
        setTimeout(() => {
            mensajeExito.classList.add('d-none');
        }, 3000); // Ocultar después de 3 segundos
    }

    // Función para obtener el CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    
    document.addEventListener('DOMContentLoaded', function() {
        function loadContent(sectionId) {
            let type = sectionId.split('-')[0]; // e.g., 'usuarios' from 'usuarios-section'
            fetch(`/api/${type}/`)
                .then(response => response.json())
                .then(data => {
                    let content = '<form>';
                    data.forEach(item => {
                        for (const [key, value] of Object.entries(item)) {
                            content += `<div class="form-group">
                                <label for="${key}">${key}</label>
                                <input type="text" class="form-control" id="${key}" value="${value}" readonly>
                            </div>`;
                        }
                    });
                    content += '</form>';
                    document.getElementById(`${type}-content`).innerHTML = content;
                })
                .catch(error => console.error('Error:', error));
        }

        console.log("El script se ha cargado correctamente.");

        // Manejar el clic en los botones de editar
        document.querySelectorAll('.editar-btn').forEach(button => {
            button.addEventListener('click', function() {
                const id = this.getAttribute('data-id');
                const nombre = this.closest('.card').querySelector('.card-title').innerText;
                const especie = this.closest('.card').querySelector('.card-text:nth-of-type(1)').innerText.split(': ')[1];
                const edad = this.closest('.card').querySelector('.card-text:nth-of-type(2)').innerText.split(': ')[1];
                mostrarDetalles(id, nombre, especie, edad);
            });
        });

        // Función para mostrar detalles de la mascota
        function mostrarDetalles(id, nombre, especie, edad) {
            const detalleDiv = document.getElementById('mascota-detalle');
            detalleDiv.innerHTML = `
                <h5>${nombre}</h5>
                <p>Especie: ${especie}</p>
                <p>Edad: ${edad}</p>
                <p>ID: ${id}</p>
                <button class="btn btn-primary" onclick="editarMascota('${id}')">Guardar Cambios</button>
            `;
        }
    });
});
