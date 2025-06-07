function toggleSidebar() {
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebar-overlay');
  
  if (sidebar.classList.contains('-translate-x-full')) {
    sidebar.classList.remove('-translate-x-full');
    overlay.classList.remove('hidden');
    document.body.classList.add('overflow-hidden');
} else {
    sidebar.classList.add('-translate-x-full');
    overlay.classList.add('hidden');
    document.body.classList.remove('overflow-hidden');
}
}

function toggleSubmenu() {
  const menuButtons = document.querySelectorAll('nav .relative > button, nav .relative > a');
  
  menuButtons.forEach(button => {
    button.addEventListener('click', function(e) {
      // Prevenir navegación si es un enlace
      if (button.tagName === 'A') {
        e.preventDefault();
      }
      
      // Buscar el submenú y la flecha
      const submenu = this.nextElementSibling;
      const arrow = this.querySelector('svg:last-child');
      
      // Alternar visibilidad del submenú
      submenu.classList.toggle('hidden');
      
      // Rotar flecha
      if (arrow) {
        arrow.classList.toggle('rotate-180');
      }
    });
  });
}