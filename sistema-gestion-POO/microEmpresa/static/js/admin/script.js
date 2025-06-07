document.addEventListener("DOMContentLoaded", () => {
    const contentArea = document.getElementById("content-area");
    const tableUsers = document.getElementById("tableUsers");

    // Cargar la tabla de usuarios al hacer clic
    tableUsers.addEventListener("click", () => {
        cargarTablaUsuarios();
    });

    // Delegación de eventos para el botón de registro
    contentArea.addEventListener("click", (event) => {
        if (event.target.id === "btnForm") {
            cargarFormularioRegistro();
        }
        //Boton para editar el usuario.
        if (event.target.classList.contains("btnEditarUser")) {
            const userId = event.target.getAttribute("data-user-id");
            cargarFormularioEditarUser(userId);
        }
        //Boton para editar Perfil.
        if (event.target.classList.contains("btnEditarProfile")) {
            const userId = event.target.getAttribute("data-user-id");
            cargarFormularioEditarPerfil(userId);
        }
    });

    // Función para cargar la tabla de usuarios
    function cargarTablaUsuarios() {
        fetch("/dashboard/admin/users/")
            .then(response => response.text())
            .then(html => {
                contentArea.innerHTML = html;
            })
            .catch(error => console.error("Error al cargar la tabla de usuarios:", error));
    }

    //Logica para el registro de usurios
    // Función para cargar el formulario de registro
    function cargarFormularioRegistro() {
        fetch("/dashboard/register/")
            .then(response => response.text())
            .then(html => {
                contentArea.innerHTML = html;
                manejarRegistroUsuario();
            })
            .catch(error => console.error("Error al cargar el formulario de usuario:", error));
    }

    // Función para manejar el formulario de registro de usuario
    function manejarRegistroUsuario() {
        const formUsuario = document.getElementById("formUsuario");
        if (formUsuario) {
            formUsuario.addEventListener("submit", (event) => {
                event.preventDefault();

                const formData = new FormData(formUsuario);

                fetch("/dashboard/register/", {
                    method: "POST",
                    body: formData,
                })
                .then(response => response.json())
                .then(data => {
                    if (data.ok) {
                        swal("¡Éxito!", "Usuario registrado correctamente", "success");

                        // Cargar el formulario de perfil
                        cargarFormularioPerfil(data.user_id);
                    } else {
                        swal("¡Oops!", "Error en el registro de usuario", "error");
                    }
                })
                .catch(error => console.error("Error al registrar usuario:", error));
            });
        } else {
            console.error("No se encontró el formulario de usuario.");
        }
    }

    // Función para cargar el formulario de completar perfil
    function cargarFormularioPerfil(userId) {
        fetch(`/completeProfile/?user_id=${userId}`)
            .then(response => response.text())
            .then(profileHtml => {
                contentArea.innerHTML = profileHtml;
                setTimeout(() => {
                    manejarPerfilUsuario(userId);
                }, 100);
            })
            .catch(error => console.error("Error al cargar el formulario de perfil:", error));
    }

    // Función para manejar el formulario de completar perfil
    function manejarPerfilUsuario(userId) {
        const formProfile = document.getElementById("formProfile");
        if (formProfile) {
            formProfile.addEventListener("submit", (event) => {
                event.preventDefault();

                const formData = new FormData(formProfile);
                formData.append("user_id", userId);

                fetch("/completeProfile/", {
                    method: "POST",
                    body: formData,
                })
                .then(response => response.json())
                .then(data => {
                    if (data.ok) {
                        swal("¡Perfil Completado!", "Cargando la tabla de usuarios...", "success");
                        setTimeout(() => {
                            // En lugar de redirigir al dashboard, se carga la tabla de usuarios
                            cargarTablaUsuarios();
                        }, 2000);
                    } else {
                        swal("¡Oops!", "Error al completar perfil", "error");
                    }
                })
                .catch(error => console.error("Error al completar perfil:", error));
            });
        } else {
            console.error("No se encontró el formulario de perfil.");
        }
    }

    //Logica para edicion del usuario 
    function cargarFormularioEditarUser(userId) {
        fetch(`/dashboard/editar/${userId}/`)
            .then(response => response.text())
            .then(html => {
                contentArea.innerHTML = html;
                editarUsuario(userId);  // Función nueva para manejar el submit
            })
            .catch(error => console.error("Error al cargar formulario de edición:", error));
    }

    function editarUsuario(userId) {
        const formUsuario = document.getElementById("formUsuario");
        if (formUsuario) {
            formUsuario.addEventListener("submit", (event) => {
                event.preventDefault();

                const formData = new FormData(formUsuario);
                formData.append("user_id", userId);

                fetch(`/dashboard/editar/${userId}/`, {
                    method: "POST",
                    body: formData,
                })
                .then(response => response.json())
                .then(data => {
                    if (data.ok) {
                        swal("¡Usuario actualizado!", "Cargando la tabla...", "success");
                        setTimeout(() => {
                            cargarTablaUsuarios();
                        }, 2000);
                    } else {
                        swal("¡Oops!", "Hubo un error al editar", "error");
                    }
                })
                .catch(error => console.error("Error al editar usuario:", error));
            });
        } else {
            console.error("No se encontró el formulario de edición.");
        }
    }

    //Logica para edicion de perfil de usuario
    function cargarFormularioEditarPerfil(userId){
        fetch(`/dashboard/editar/profile/${userId}/`)
            .then(response => response.text())
            .then(html => {
                contentArea.innerHTML = html;
                editarPerfil(userId);  // Función nueva para manejar el submit
            })
            .catch(error => console.error("Error al cargar formulario de edición:", error));
    }
    
    function editarPerfil(userId) {
        const formProfile = document.getElementById("formProfile");
        if (formProfile) {
            formProfile.addEventListener("submit", (event) => {
                event.preventDefault();

                const formData = new FormData(formProfile);
                formData.append("user_id", userId);

                fetch(`/dashboard/editar/profile/${userId}/`, {
                    method: "POST",
                    body: formData,
                })
                .then(response => response.json())
                .then(data => {
                    if (data.ok) {
                        swal("¡Perfil actualizado!", "Cargando la tabla...", "success");
                        setTimeout(() => {
                            cargarTablaUsuarios();
                        }, 2000);
                    } else {
                        swal("¡Oops!", "Hubo un error al editar", "error");
                    }
                })
                .catch(error => console.error("Error al editar usuario:", error));
            });
        } else {
            console.error("No se encontró el formulario de edición.");
        }
    }
});
