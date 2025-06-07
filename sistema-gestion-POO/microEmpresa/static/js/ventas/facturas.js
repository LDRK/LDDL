document.addEventListener("DOMContentLoaded", () => {
    const contentArea = document.getElementById("content-area");
    const facturas = document.getElementById("facturas");
    const modal = document.getElementById("modalEditar");
    const modalContent = document.getElementById("modalContent");



    // Cargar las facturas al hacer clic
    facturas.addEventListener("click", () => {
        viewFacturas();
    });

    // Delegación de eventos para ver la factura en el modal
    contentArea.addEventListener("click", (event) => {
        if (event.target && event.target.classList.contains("ver-factura")) {
            const facturaId = event.target.getAttribute("data-id");
            if (facturaId) {
                mostrarFacturaEnModal(facturaId);
            } else {
                console.error("No se encontró el ID de la factura.");
            }
        }
    });

    // Función para cargar la lista de facturas
    function viewFacturas() {
        fetch("/dashboard/ventas/facturas/")
            .then(response => response.text())
            .then(html => {
                contentArea.innerHTML = html;
            })
            .catch(error => console.error("Error al cargar las facturas:", error));
    }

    // Función para cargar una factura específica y mostrarla en el modal
    function mostrarFacturaEnModal(facturaId) {
        fetch(`/dashboard/ventas/viewFactura/${facturaId}/`)
            .then(response => response.text())
            .then(html => {
                modalContent.innerHTML = html;
                modal.classList.remove("hidden");
            })
            .catch(error => console.error("Error al cargar la factura:", error));
    }

    document.addEventListener("click", (event) => {
    if (event.target && event.target.id === "cerrarModal") {
      modal.classList.add("hidden");
      modalContent.innerHTML = ""; // Limpio contenido para evitar mezclar datos
    }
  });
});
