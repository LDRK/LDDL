/** Formulario de registro de uusario
 * captura de datos y envio al controlador.
 */

document
  .getElementById("formSingup")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Evita que el formulario se envíe de manera tradicional

    const nombre = document.querySelector("#nombre").value;
    const usuario = document.querySelector("#usuario").value;
    const correo = document.querySelector("#correo").value;
    const contrasena = document.querySelector("#contrasena").value;
    console.log({ nombre, usuario, correo, contrasena });

    // Envía los datos al backend usando fetch
    fetch("../../controllers/controllerUsuario.php", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({
        nombre: nombre,
        usuario: usuario,
        correo: correo,
        contrasena: contrasena,
        formSingup: true, // Para que tu PHP lo reconozca
      }),
    })
      .then((response) => {
        // Verificar si la respuesta es válida
        if (response.ok) {
          return response.json(); // Parsear el JSON de la respuesta
        } else {
          throw new Error("Network response was not ok");
        }
      })
      .then((data) => {
        if (data.success) {
          // Si la respuesta es exitosa, redirigir al login
          window.location.href = data.redirect;
        } else {
          // Mostrar error si no es exitoso
          document.getElementById("message").innerText = data.error;
        }
      })
      .catch((error) => {
        console.log(error);
        //swal("Oops", "Something went wrong!", error);
      });
  });
