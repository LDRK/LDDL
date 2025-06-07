document.addEventListener("DOMContentLoaded", () => {
    const contentArea = document.getElementById("content-area");
    const tablaProducto = document.getElementById("tablaProducto");

    

    // Cargar la tabla de productos al hacer clic
    tablaProducto.addEventListener("click", () => {
        tablaProductos();
    });

    

    // Delegación de eventos para el botón de registro
    contentArea.addEventListener("click", (event) => {
        if (event.target.id === "btnFormProducto") {
            formRegistroProducto();
        }
        // //Boton para editar el producto.
        if (event.target.classList.contains("btnEditarProducto")) {
            const productoId = event.target.getAttribute("data-producto-id");
            formEditarProducto(productoId);
        }

        // Botón para eliminar producto
        if (event.target.classList.contains("btnEliminarProducto")) {
            const productoId = event.target.getAttribute("data-producto-id");

            swal({
                title: "¿Estás seguro?",
                text: "Esta acción no se puede deshacer",
                icon: "warning",
                buttons: true,
                dangerMode: true,
                })
                .then((willDelete) => {
                    if (willDelete) {
                    eliminarProducto(productoId);
                }
             });
            }
        
    });

    // Función para cargar la tabla de productos
    function tablaProductos() {
        fetch("/dashboard/inventario/productos/")
            .then(response => response.text())
            .then(html => {
                contentArea.innerHTML = html;
            })
            .catch(error => console.error("Error al cargar la tabla de productos:", error));
    }

    
    // Función para cargar el formulario de registro de productos
    function formRegistroProducto() {
        fetch("/dashboard/inventario/rProducto/")
            .then(response => response.text())
            .then(html => {
                contentArea.innerHTML = html;
                registrarProducto();
            })
            .catch(error => console.error("Error al cargar el formulario de producto:", error));
    }

  // Función para manejar el formulario de registro de producto
    function registrarProducto() {
        const formProducto = document.getElementById("formProducto");
        if (formProducto) {
            formProducto.addEventListener("submit", (event) => {
                event.preventDefault();

                const formData = new FormData(formProducto);

                fetch("/dashboard/inventario/rProducto/", {
                    method: "POST",
                    body: formData,
                })
                .then(response => response.json())
                .then(data => {
                    if (data.ok) {
                        swal("¡Éxito!", "Producto registrado correctamente", "success");
                        tablaProductos(); //En lugar de redirigir al dashboard, se carga la tabla de productos
                    } else {
                        swal("¡Oops!", "Error en el registro del producto", "error");
                    }
                })
                .catch(error => console.error("Error al registrar Producto:", error));
            });
        } else {
            console.error("No se encontró el formulario de Producto.");
        }
    }


   

    //Logica para edicion del producto 
    function formEditarProducto(productoId) {
        fetch(`/dashboard/inventario/editar/${productoId}/`)
            .then(response => response.text())
            .then(html => {
                contentArea.innerHTML = html;
                editarProducto(productoId);  // Función nueva para manejar el submit
            })
            .catch(error => console.error("Error al cargar formulario de edición:", error));
    }

    function editarProducto(productoId) {
        const formProducto = document.getElementById("formProducto");
        if (formProducto) {
            formProducto.addEventListener("submit", (event) => {
                event.preventDefault();

                const formData = new FormData(formProducto);
                formData.append("producto_id", productoId);

                fetch(`/dashboard/inventario/editar/${productoId}/`, {
                    method: "POST",
                    body: formData,
                })
                .then(response => response.json())
                .then(data => {
                    if (data.ok) {
                        swal("¡Producto actualizado!", "Cargando la tabla...", "success");
                        tablaProductos();
                    } else {
                        swal("¡Oops!", "Hubo un error al editar", "error");
                    }
                })
                .catch(error => console.error("Error al editar Producto:", error));
            });
        } else {
            console.error("No se encontró el formulario de edición.");
        }
    }

    function eliminarProducto(productoId) {
        fetch(`/dashboard/inventario/eliminar/${productoId}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"), // Necesario para POST en Django
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.ok) {
                swal("¡Eliminado!", "El producto fue eliminado", "success");
                tablaProductos();
            } else {
                swal("¡Error!", "No se pudo eliminar el producto", "error");
            }
        })
        .catch(error => console.error("Error al eliminar producto:", error));
    }
    

  
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    
});

