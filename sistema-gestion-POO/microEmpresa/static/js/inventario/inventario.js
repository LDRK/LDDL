document.addEventListener("DOMContentLoaded", () => {
    const contentArea = document.getElementById("content-area");
    const tablaInventario = document.getElementById("tablaInventario");


    // Cargar la tabla de productos al hacer clic
    tablaInventario.addEventListener("click", () => {
        viewTablaInventario();
    });
    
    // Delegación de eventos para el botón de registro
    contentArea.addEventListener("click", (event) => {
        if (event.target.id === "btnFormInventario") {
            formRegistroInventario();
        }
      
        
    });

    // Función para cargar el formulario de registro de productos
    function formRegistroInventario() {
        fetch("/dashboard/inventario/rStore/")
            .then(response => response.text())
            .then(html => {
                contentArea.innerHTML = html;
                registrarInventario();
            })
            .catch(error => console.error("Error al cargar el formulario de Categoria:", error));
    }

    // Función para cargar la tabla de productos
    function viewTablaInventario() {
        fetch("/dashboard/inventario/store/")
            .then(response => response.text())
            .then(html => {
                contentArea.innerHTML = html;
            })
            .catch(error => console.error("Error al cargar la tabla de productos:", error));
    }

    function registrarInventario() {
        const formInventario = document.getElementById("formInventario");
        if (formInventario) {
            formInventario.addEventListener("submit", (event) => {
                event.preventDefault();

                const formData = new FormData(formInventario);

                fetch("/dashboard/inventario/rStore/", {
                    method: "POST",
                    body: formData,
                })
                .then(response => response.json())
                .then(data => {
                    if (data.ok) {
                        swal("¡Éxito!", "Stock registrado correctamente", "success");
                        // window.location.href = data.redirect_url; // En lugar de redirigir al dashboard, se carga la tabla de productos
                        viewTablaInventario();
                    } else {
                        swal("¡Oops!", "Error en el registro de Stock", "error");
                    }
                })
                .catch(error => console.error("Error al registrar Stock:", error));
            });
        } else {
            console.error("No se encontró el formulario de Stock.");
        }
    }
});