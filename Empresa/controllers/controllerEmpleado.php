<?php
require_once '../models/registerEmployed.php'; // Archivo donde está el modelo

if (isset($_POST['enviarDatos'])) {
    class EmpleadoController {
        public function registrarEmpleado() {
            // Recibir los datos del formulario
            $nombre = $_POST['nombre'];
            $apellidoPaterno = $_POST['apellidoPaterno'];
            $apellidoMaterno = $_POST['apellidoMaterno'];
            $correo = $_POST['correo'];
            $departamento = $_POST['departamento'];
            $foto = $_POST['foto'];

            // Instanciar el modelo
            $personal = new Personal();

            // Llamar al método del modelo y obtener el resultado
            $resultado = $personal->crearEmpleado($nombre, $apellidoPaterno, $apellidoMaterno, $correo, $departamento,$foto);

            // Dependiendo del resultado, redirigir a la vista adecuada
            if ($resultado) {
                // Empleado creado con éxito
                header("Location: ../layout/pages/prueba.php");
            } else {
                // Error al crear el empleado
                header("Location: error.php");
            }
        }
    

   
}
 // Crear instancia del controlador y ejecutar el método
 $empleadoController = new EmpleadoController();
 $empleadoController->registrarEmpleado();
}
?>