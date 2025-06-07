// Esperar a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    // Obtener referencias a los elementos
    const searchInput = document.getElementById('table-search');
    
    // Verificar que el input de búsqueda existe
    if (!searchInput) {
        console.error('Elemento con ID "table-search" no encontrado');
        return; // Salir si no existe
    }
    
    const tableRows = document.querySelectorAll('#table-producto tbody tr');
    
    // Verificar que hay filas en la tabla
    if (tableRows.length === 0) {
        console.warn('No se encontraron filas en la tabla de productos');
        return; // Salir si no hay filas
    }
    
    // Función para filtrar los productos
    function filtrarProductos() {
        // Obtener el valor de búsqueda y convertirlo a minúsculas
        const busqueda = searchInput.value.toLowerCase().trim();
        
        // Iterar por cada fila de la tabla
        tableRows.forEach(row => {
            try {
                // Obtener el texto de las celdas relevantes con comprobación de existencia
                const nombreCell = row.querySelector('td:nth-child(2)');
                const descripcionCell = row.querySelector('td:nth-child(3)');
                const categoriaCell = row.querySelector('td:nth-child(5)');
                
                const nombre = nombreCell ? nombreCell.textContent.toLowerCase() : '';
                const descripcion = descripcionCell ? descripcionCell.textContent.toLowerCase() : '';
                const categoria = categoriaCell ? categoriaCell.textContent.toLowerCase() : '';
                
                // Verificar si alguno de los campos contiene el texto de búsqueda
                const coincide = nombre.includes(busqueda) || 
                                descripcion.includes(busqueda) || 
                                categoria.includes(busqueda);
                
                // Mostrar u ocultar la fila según el resultado
                if (coincide || busqueda === '') {
                    row.style.display = ''; // Mostrar la fila
                } else {
                    row.style.display = 'none'; // Ocultar la fila
                }
            } catch (error) {
                console.error('Error al procesar fila:', error);
            }
        });
    }
    
    // Escuchar el evento 'input' para filtrar en tiempo real mientras el usuario escribe
    searchInput.addEventListener('input', filtrarProductos);
    
    // También podemos filtrar cuando el usuario presiona Enter
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            filtrarProductos();
        }
    });
    
    console.log('Funcionalidad de búsqueda inicializada correctamente');
});