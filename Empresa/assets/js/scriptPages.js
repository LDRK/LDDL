// Funcionalidad del botón del perfil en Dashboard
const menuBtn = document.getElementById("user-menu-button");
const menu = document.getElementById("options-menu");

menuBtn.addEventListener("click", (event) => {
  event.preventDefault(); // Evita la recarga de la página
  menu.classList.toggle("hidden"); // Alterna entre mostrar/ocultar el menú
});

// Funcionalidad del menú móvil
const mobileMenuButton = document.querySelector(
  '[aria-controls="mobile-menu"]'
);
const mobileMenu = document.getElementById("mobile-menu");

mobileMenuButton.addEventListener("click", () => {
  mobileMenu.classList.toggle("hidden");

  // Alternar iconos de menú abierto/cerrado
  const iconClose = mobileMenuButton.querySelector(".hidden");
  const iconOpen = mobileMenuButton.querySelector(".block");

  iconOpen.classList.toggle("hidden");
  iconClose.classList.toggle("hidden");
});
