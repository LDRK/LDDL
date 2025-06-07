document.addEventListener("DOMContentLoaded", () => {
    const contentArea = document.getElementById("content-area");
    const btnForm = document.getElementById("btnForm");

    // Manejar el clic del botón para mostrar el formulario
    btnForm.addEventListener("click", () => {
        fetch("/registroEmpleados/") // Ruta estática del formulario
            .then((response) => response.text())
            .then((html) => {
                contentArea.innerHTML = html; // Cargar el formulario en el contenedor

                

                // Ahora que el formulario está cargado, podemos agregar el event listener
                const formEmpleado = document.getElementById('formEmpleado');
                if (formEmpleado) {
                    formEmpleado.addEventListener('submit', (event) => {
                        event.preventDefault();

                        // Aquí va el código de la solicitud de envío
                        const formData = new FormData(formEmpleado)

                        fetch('/registroEmpleados/', {
                            method: 'POST',
                            body: formData,
                        })
                            .then(response => response.json())
                            .then(data => {
                                if (data.ok) {
                                    swal("Exitoso!", "Registro de Empleado", "success"); // mensaje de éxito
                                    window.location.href = data.redirect_url;
                                    formEmpleado.reset();
                                } else {
                                    swal("Oops!", "Ocurrió un error en el registro!", "error");
                                }
                            })
                            .catch(error => console.error('Error al registrar empleado:', error));
                    });
                } else {
                    console.error("No se encontró el formulario con ID 'formEmpleado'");
                }
            })
            .catch((error) => console.error("Error al cargar el formulario:", error));
    });


     // Manejar clic en botón de edición
     document.addEventListener('click', function(e) {
        if (e.target.classList.contains('btn-editar')) {
            e.preventDefault();
            const empleadoId = e.target.dataset.id;
            
            fetch(`/dashboard/editar/${empleadoId}/`)
                
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
    fetch("/tablaEmpleados/") // Ruta estática de la tabla
        .then((response) => response.text())
        .then((html) => {
            contentArea.innerHTML = html; // Cargar la tabla en el contenedor
        })
        .catch((error) => console.error("Error al cargar la tabla:", error));
});

//Modal para cargar el excel
document.addEventListener("DOMContentLoaded", function () {
    const modalExcel = document.getElementById('modalExcel');
    const btnModalExcel = document.getElementById('btnModalExcel');

    if (modalExcel && btnModalExcel) {
        modalExcel.addEventListener('shown.bs.modal', () => {
            btnModalExcel.focus();
        });
    }
});
