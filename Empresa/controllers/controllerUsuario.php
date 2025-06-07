<?php
require_once '../models/registerUser.php'; // Archivo donde está el modelo

if (isset($_POST['btn-singup'])) {
    class UsarioController {
        public function registrarUsuario() {
            // Recibir los datos del formulario
            $nombre = $_POST['nombre'];            
            $usuario = $_POST['usuario'];
            $correo = $_POST['correo'];
            $contrasena = $_POST['contrasena'];
          

            // Instanciar el modelo
            $user = new User();

            // Llamar al método del modelo y obtener el resultado
            $resultado = $user->crearUsuario($nombre, $usuario, $correo, $contrasena);

            header('Content-Type: application/json'); // Asegúrate de establecer el tipo de contenido
            if ($resultado) {
                 echo json_encode(['success' => true, 'redirect' => '../../layout/pages/login.php']);
            } else {
                echo json_encode(['success' => false, 'error' => 'Error al registrar el usuario.']);
            }
            exit; // Detener la ejecución del script después de enviar la respuesta
        }
    

   
}
 // Crear instancia del controlador y ejecutar el método
 $usuarioController = new UsarioController();
 $usuarioController->registrarUsuario();
}

// if (isset($_POST['btn-login'])) {
//     class LoginController {
//         public function loginUsuario() {
//             // Recibir los datos del formulario
                       
//             $usuario = $_POST['usuario'];
            
//             $contrasena = $_POST['contrasena'];
          

//             // Instanciar el modelo
//             $user = new User();

//             // Llamar al método del modelo y obtener el resultado
//             $resultado = $user->Login($usuario,$contrasena);

//             header('Content-Type: application/json'); // Asegúrate de establecer el tipo de contenido
//             if ($resultado) {
//                  echo json_encode(['success' => true, 'redirect' => '../../layout/pages/dashboard.php']);
//             } else {
//                 echo json_encode(['success' => false, 'error' => 'Error al registrar el usuario.']);
//             }
//             exit; // Detener la ejecución del script después de enviar la respuesta
//         }
    

   
// }
//  // Crear instancia del controlador y ejecutar el método
//  $LoginController = new LoginController();
//  $loginController->loginUsuario();
// }



?>