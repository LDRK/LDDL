document.addEventListener("DOMContentLoaded", () => {
    const contentArea = document.getElementById("content-area");
    const verCarrito = document.getElementById("ver-carrito");
    const carritoCantidad = document.getElementById("contador-carrito");

    actualizarCantidadCarrito();

    if (verCarrito) {
        verCarrito.addEventListener("click", (e) => {
            e.preventDefault();
            mostrarCarrito();
        });
    }

    contentArea.addEventListener("click", (event) => {
        // Agregar producto
        if (event.target.classList.contains("btnAgregarAlCarrito")) {
            const button = event.target;
            const id = button.getAttribute("data-producto-id");
            const nombre = button.getAttribute("data-nombre");
            const precio = parseFloat(button.getAttribute("data-precio"));

            agregarProductoAlCarrito({ id, nombre, precio });
        }

        // Vaciar carrito
        if (event.target.id === "vaciar-carrito") {
            localStorage.removeItem("carrito");
            actualizarCantidadCarrito();
            contentArea.innerHTML = "<p class='text-center text-gray-600 mt-6'>El carrito está vacío.</p>";
        }

        // Aumentar cantidad
        if (event.target.classList.contains("btn-mas")) {
            const id = event.target.dataset.id;
            modificarCantidad(id, 1);
        }

        // Disminuir cantidad
        if (event.target.classList.contains("btn-menos")) {
            const id = event.target.dataset.id;
            modificarCantidad(id, -1);
        }

        // Eliminar producto
        if (event.target.classList.contains("btn-eliminar")) {
            const id = event.target.dataset.id;
            eliminarProducto(id);
        }
    });

    function agregarProductoAlCarrito(producto) {
        let carrito = JSON.parse(localStorage.getItem("carrito")) || [];
        const index = carrito.findIndex(item => item.id === producto.id);

        if (index !== -1) {
            carrito[index].cantidad += 1;
        } else {
            producto.cantidad = 1;
            carrito.push(producto);
        }

        localStorage.setItem("carrito", JSON.stringify(carrito));
        actualizarCantidadCarrito();
    }

    function actualizarCantidadCarrito() {
        const carrito = JSON.parse(localStorage.getItem("carrito")) || [];
        const total = carrito.reduce((sum, item) => sum + item.cantidad, 0);
        if (carritoCantidad) {
            carritoCantidad.textContent = total;
        }
    }

    function modificarCantidad(id, cambio) {
        let carrito = JSON.parse(localStorage.getItem("carrito")) || [];
        const index = carrito.findIndex(item => item.id === id);

        if (index !== -1) {
            carrito[index].cantidad += cambio;

            if (carrito[index].cantidad <= 0) {
                carrito.splice(index, 1); // eliminar si llega a 0
            }

            localStorage.setItem("carrito", JSON.stringify(carrito));
            actualizarCantidadCarrito();
            mostrarCarrito();
        }
    }

    function eliminarProducto(id) {
        let carrito = JSON.parse(localStorage.getItem("carrito")) || [];
        carrito = carrito.filter(item => item.id !== id);

        localStorage.setItem("carrito", JSON.stringify(carrito));
        actualizarCantidadCarrito();
        mostrarCarrito();
    }

    function mostrarCarrito() {
        const carrito = JSON.parse(localStorage.getItem("carrito")) || [];

        fetch("/dashboard/ventas/carrito/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),
            },
            body: JSON.stringify(carrito),
        })
        .then(response => response.text())
        .then(html => {
            contentArea.innerHTML = html;
        })
        .catch(error => console.error("Error al mostrar el carrito:", error));
    }

    function getCSRFToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        return cookieValue || '';
    }
});
