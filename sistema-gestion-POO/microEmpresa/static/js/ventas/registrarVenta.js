document.addEventListener("DOMContentLoaded", () => {
    const contentArea = document.getElementById("content-area");
    

    contentArea.addEventListener("click", (event) => {
        if (event.target.id === "registerSaleButton") {
            formRegistroVenta();
        }
    });

    function formRegistroVenta() {
        fetch("/dashboard/ventas/rVenta/")
            .then(response => response.text())
            .then(html => {
                contentArea.innerHTML = html;
                inicializarFormularioVenta();  // Ejecuta esto tras cargar la vista
                registrarVenta();
            })
            .catch(error => console.error("Error al cargar el formulario de venta:", error));
    }

    function inicializarFormularioVenta() {
        const tabla = document.getElementById("tabla-carrito");
        const productos = JSON.parse(localStorage.getItem("carrito")) || [];

        productos.forEach(prod => {
            const subtotal = prod.precio * prod.cantidad;
            tabla.innerHTML += `
                <tr>
                    <td>${prod.nombre}</td>
                    <td>${prod.cantidad}</td>
                    <td>${prod.precio.toFixed(2)}</td>
                    <td>${subtotal.toFixed(2)}</td>
                </tr>
            `;
        });

       
    }

    function registrarVenta() {
        const formVentaCliente = document.getElementById("formVentaCliente");

        if (formVentaCliente) {
            formVentaCliente.addEventListener("submit", (event) => {
                event.preventDefault();

                const cliente = {
                    cedula: document.getElementById("cedula").value,
                    nombre: document.getElementById("nombre").value,
                    apellido: document.getElementById("apellido").value,
                    correo: document.getElementById("correo").value,
                    celular: document.getElementById("celular").value
                };

                const productos = JSON.parse(localStorage.getItem("carrito")) || [];

                fetch("/dashboard/ventas/rVenta/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCookie("csrftoken")
                    },
                    body: JSON.stringify({
                        cliente: cliente,
                        carrito: productos
                    })
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.ok) {
                            swal("¡Éxito!", "Venta registrada correctamente", "success");
                            localStorage.removeItem("carrito");
                            formVentaCliente.reset();
                        } else {
                            swal("¡Oops!", "Error en el registro de la venta", "error");
                        }
                    })
                    .catch(error => {
                        console.error("Error:", error);
                        swal("¡Oops!", "Error en el registro de la venta", "error");
                    });
            });
        }
    }

    // Obtener token CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith(name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});