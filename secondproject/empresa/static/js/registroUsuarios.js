document.addEventListener("DOMContentLoaded", () => {
    const contentArea = document.getElementById("content-area");
    const btnForm = document.getElementById("btnForm");

    // Manejar el clic del botón para mostrar el formulario
    btnForm.addEventListener("click", () => {
        fetch("/formUsuarios/") // Ruta estática del formulario
            .then((response) => response.text())
            .then((html) => {
                contentArea.innerHTML = html; // Cargar el formulario en el contenedor

                

                // Ahora que el formulario está cargado, podemos agregar el event listener
                const formUsuario = document.getElementById('formUsuario');
                if (formUsuario) {
                    formUsuario.addEventListener('submit', (event) => {
                        event.preventDefault();

                        // Aquí va el código de la solicitud de envío
                        const formData = new FormData(formUsuario)
                        console.log(formData)
                        fetch('/registroUsuarios/', {
                            method: 'POST',
                            body: formData,
                        })
                            .then(response => response.json())
                            .then(data => {
                                if (data.ok) {
                                    swal("Exitoso!", "Registro de Usuario", "success"); // mensaje de éxito
                                    window.location.href = data.redirect_url;
                                    formUsuario.reset();
                                } else {
                                    swal("Oops!", "Ocurrió un error en el registro!", "error");
                                }
                            })
                            .catch(error => console.error('Error al registrar empleado:', error));
                    });
                } else {
                    console.error("No se encontró el formulario con ID 'formUsuario'");
                }
            })
            .catch((error) => console.error("Error al cargar el formulario:", error));
    });


     // Manejar clic en botón de edición
     document.addEventListener('click', function(e) {
        if (e.target.classList.contains('btn-editar')) {
            e.preventDefault();
            const usuarioId = e.target.dataset.id;
            
            fetch(`/usuarios/editar/${usuarioId}/`)
                
            .then(response => {
                
                return response.text();
            })
            .then(html => {
                contentArea.innerHTML = html;
            })
            .catch(error => console.error("Error completo:", error));
        }
    });



    // Por defecto, carga la tabla de empleados
    fetch("/tablaUsuarios/") // Ruta estática de la tabla
        .then((response) => response.text())
        .then((html) => {
            contentArea.innerHTML = html; // Cargar la tabla en el contenedor
        })
        .catch((error) => console.error("Error al cargar la tabla:", error));
});

