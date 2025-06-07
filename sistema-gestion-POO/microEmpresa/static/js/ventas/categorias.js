document.addEventListener("DOMContentLoaded", () => {
    const contentArea = document.getElementById("content-area");
    const categorias = document.getElementById("categorias");

    

    // Cargar las categorias al hacer clic
    categorias.addEventListener("click", () => {
        viewCategorias();
    });

    

     // Delegación de eventos para cargar los productos de una categoría
     contentArea.addEventListener("click", (event) => {
        if (event.target && event.target.classList.contains("ver-productos")) {
            const categoriaId = event.target.getAttribute("data-id");
            if (categoriaId) {
                tablaConProductos(categoriaId);
            } else {
                console.error("No se encontró el ID de la categoría.");
            }
        }
        
    });

    // Función para cargar las categorias
    function viewCategorias() {
        fetch("/dashboard/ventas/categorias/")
            .then(response => response.text())
            .then(html => {
                contentArea.innerHTML = html;
            })
            .catch(error => console.error("Error al cargar las categorias:", error));
    }

    // Función para cargar el formulario de registro de productos
    function tablaConProductos(categoriaId) {
        fetch(`/dashboard/ventas/producto/categoria/${categoriaId}/`)
            .then(response => response.text())
            .then(html => {
                contentArea.innerHTML = html;
            })
            .catch(error => console.error("Error al cargar la tabla con los productos:", error));
    }


    
});

