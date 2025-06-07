document.addEventListener("DOMContentLoaded", () => {
    const contentArea = document.getElementById("content-area");

    // Delegación de eventos para el botón de registro
    contentArea.addEventListener("click", (event) => {
        if (event.target.id === "btnFormCategoria") {
            formRegistroCategoria();
        }
        //Evento para el boton editar
        if (event.target.classList.contains("btnEditarStock")) {
            const inventarioId = event.target.getAttribute("data-stock-id");
            formEditarStock(inventarioId);
        }
      
    
    });

    //Logica para el registro de usurios
    // Función para cargar el formulario de registro de productos
    function formRegistroCategoria() {
        fetch("/dashboard/inventario/rCategoria/")
            .then(response => response.text())
            .then(html => {
                contentArea.innerHTML = html;
                registrarCategoria();
            })
            .catch(error => console.error("Error al cargar el formulario de Categoria:", error));
    }

    // Función para cargar la tabla de productos
    function tablaProductos() {
        fetch("/dashboard/inventario/productos/")
            .then(response => response.text())
            .then(html => {
                contentArea.innerHTML = html;
            })
            .catch(error => console.error("Error al cargar la tabla de productos:", error));
    }

    // Función para cargar la tabla de inventario
    function tablaInventario() {
        fetch("/dashboard/inventario/store/")
            .then(response => response.text())
            .then(html => {
                contentArea.innerHTML = html;
            })
            .catch(error => console.error("Error al cargar la tabla de inventario:", error));
    }

    function registrarCategoria() {
        const formCategoria = document.getElementById("formCategoria");
        if (formCategoria) {
            formCategoria.addEventListener("submit", (event) => {
                event.preventDefault();

                const formData = new FormData(formCategoria);

                fetch("/dashboard/inventario/rCategoria/", {
                    method: "POST",
                    body: formData,
                })
                .then(response => response.json())
                .then(data => {
                    if (data.ok) {
                        swal("¡Éxito!", "Categoria registrada correctamente", "success");
                        // window.location.href = data.redirect_url; // En lugar de redirigir al dashboard, se carga la tabla de productos
                        tablaProductos();
                    } else {
                        swal("¡Oops!", "Error en el registro de Categoria", "error");
                    }
                })
                .catch(error => console.error("Error al registrar usuario:", error));
            });
        } else {
            console.error("No se encontró el formulario de Categoria.");
        }
    }



     //Logica para edicion del Stock 
     function formEditarStock(inventarioId) {
        fetch(`/dashboard/inventario/editar/stock/${inventarioId}/`)
            .then(response => response.text())
            .then(html => {
                contentArea.innerHTML = html;
                editarStock(inventarioId);  // Función nueva para manejar el submit
            })
            .catch(error => console.error("Error al cargar formulario de edición:", error));
    }

    function editarStock(inventarioId) {
        const formInventario = document.getElementById("formInventario");
        if (formInventario) {
            formInventario.addEventListener("submit", (event) => {
                event.preventDefault();

                const formData = new FormData(formInventario);
                formData.append("inventario_id", inventarioId);

                fetch(`/dashboard/inventario/editar/stock/${inventarioId}/`, {
                    method: "POST",
                    body: formData,
                })
                .then(response => response.json())
                .then(data => {
                    if (data.ok) {
                        swal("Stock actualizado!", "Cargando la tabla...", "success");
                        tablaInventario();
                    } else {
                        swal("¡Oops!", "Hubo un error al editar", "error");
                    }
                })
                .catch(error => console.error("Error al editar Inventario:", error));
            });
        } else {
            console.error("No se encontró el formulario de edición.");
        }
    }
    
});