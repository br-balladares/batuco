document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#registroForm').reset();

    const nombreInput = document.querySelector('#id_nombre');
    const rutInput = document.querySelector('#id_rut');
    const emailInput = document.querySelector('#id_correo');
    const telefonoInput = document.querySelector('#id_telefono');
    const comunaInput = document.querySelector('#id_comuna');
    const ciudadInput = document.querySelector('#id_ciudad');
    const passwordInput = document.querySelector('#id_password');
    const codigoPaisSelect = document.querySelector('#id_codigo_pais');

    const regexNombre = /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/;
    const regexRut = /^[0-9]{1,2}\.[0-9]{3}\.[0-9]{3}-[0-9kK]{1}$/;
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    const telefonoRegex = /^\+\d{1,3} \d{9,15}$/;
    const textoRegex = /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/;
    const passwordRegex = /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&+=]).{8,}$/;

    const validarCampo = (input, regex, mensajeError, errorId) => {
        input.addEventListener('input', function() {
            if (!regex.test(input.value) && input.value !== "") {
                input.classList.add('is-invalid');
                document.querySelector(`#${errorId}`).textContent = mensajeError;
            } else {
                input.classList.remove('is-invalid');
                document.querySelector(`#${errorId}`).textContent = "";
            }
        });
    };

    // Aplicar validaciones en tiempo real
    validarCampo(nombreInput, regexNombre, "El nombre solo puede contener letras y espacios.", 'nombreError');
    validarCampo(rutInput, regexRut, "El RUT debe tener el formato 12.345.678-9.", 'rutError');
    validarCampo(comunaInput, textoRegex, "La comuna solo puede contener letras y espacios.", 'comunaError');
    validarCampo(ciudadInput, textoRegex, "La ciudad solo puede contener letras y espacios.", 'ciudadError');

    emailInput.addEventListener('input', function() {
        if (emailInput.value === "" || emailRegex.test(emailInput.value)) {
            emailInput.classList.remove('is-invalid');
            document.querySelector('#emailError').textContent = "";
        } else {
            emailInput.classList.add('is-invalid');
            document.querySelector('#emailError').textContent = "Por favor, ingresa un correo electrónico válido.";
        }
    });

    passwordInput.addEventListener('input', function() {
        if (!passwordRegex.test(passwordInput.value)) {
            passwordInput.classList.add('is-invalid');
            document.querySelector('#passwordError').textContent = "La contraseña debe tener al menos 8 caracteres, incluir una mayúscula, una minúscula, un número y un carácter especial.";
        } else {
            passwordInput.classList.remove('is-invalid');
            document.querySelector('#passwordError').textContent = "";
        }
    });

    telefonoInput.addEventListener('input', function() {
        const telefono = telefonoInput.value;
        const codigoPais = codigoPaisSelect.value;
        const telefonoCompleto = `${codigoPais} ${telefono}`;

        if (!telefonoRegex.test(telefonoCompleto)) {
            document.querySelector('#telefonoError').textContent = "El teléfono debe incluir el código de país y tener entre 9 y 15 dígitos.";
            telefonoInput.classList.add('is-invalid');
        } else {
            document.querySelector('#telefonoError').textContent = "";
            telefonoInput.classList.remove('is-invalid');
        }
    });

    document.querySelector('#registroForm').addEventListener('submit', function(event) {
        let isValid = true;

        // Validaciones finales antes de enviar el formulario
        if (!regexNombre.test(nombreInput.value)) isValid = false;
        if (!regexRut.test(rutInput.value)) isValid = false;
        if (emailInput.value !== "" && !emailRegex.test(emailInput.value)) isValid = false;
        const telefonoCompleto = `${codigoPaisSelect.value} ${telefonoInput.value}`;
        if (!telefonoRegex.test(telefonoCompleto)) isValid = false;
        if (!textoRegex.test(comunaInput.value)) isValid = false;
        if (!textoRegex.test(ciudadInput.value)) isValid = false;
        if (!passwordRegex.test(passwordInput.value)) isValid = false;

        if (!isValid) {
            event.preventDefault(); // Prevenir el envío del formulario si hay errores
        }
    });
});
