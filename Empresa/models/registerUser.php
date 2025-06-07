<?php
require_once '../models/connection/connection.php';

class User{
    private $conexion;

    public function __construct(){
        $this->conexion = new Conexion();
        $this->conexion = $this->conexion->conectar();
    }

    public function crearUsuario($nombre, $usuario, $correo, $contrasena) {
        try {
            $hashedPassword = password_hash($contrasena, PASSWORD_DEFAULT); // Hashear la contraseña
            $query = "INSERT INTO usuario(nombre, usuario, correo, contrasena) VALUES (:nombre, :usuario, :correo, :contrasena)";
            $stmt = $this->conexion->prepare($query);
            $stmt->bindParam(':nombre', $nombre);
            $stmt->bindParam(':usuario', $usuario);
            $stmt->bindParam(':correo', $correo);
            $stmt->bindParam(':contrasena', $hashedPassword);  
            $stmt->execute();
            return true; // Devuelve verdadero si se ejecuta correctamente
        } catch (Exception $e) {
            echo json_encode(['success' => false, 'error' => $e->getMessage()]);
            exit;
        }
    }

    public function Login($usuario, $contrasena) {
        try {
            // Consulta para obtener el usuario y su contraseña hasheada
            $query = "SELECT id_usuario, contrasena FROM usuario WHERE usuario = :usuario"; // Asegúrate de usar el campo correcto
            $stmt = $this->conexion->prepare($query);
            $stmt->bindParam(':usuario', $usuario);
            $stmt->execute();
    
            // Verificar si se encontró el usuario
            if ($stmt->rowCount() === 1) {
                $row = $stmt->fetch(PDO::FETCH_ASSOC);
                // Verificar la contraseña
                if (password_verify($contrasena, $row['contrasena'])) {
                    // Contraseña correcta
                    return ['success' => true]; // Indicar éxito
                } else {
                    // Contraseña incorrecta
                    return ['success' => false, 'error' => 'Contraseña incorrecta.'];
                }
            } else {
                // Usuario no encontrado
                return ['success' => false, 'error' => 'Usuario no encontrado.'];
            }
        } catch (Exception $e) {
            return ['success' => false, 'error' => $e->getMessage()];
        }
    }
    
    
        
    
    
}


?>