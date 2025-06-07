<?php

class Conexion {
    private $host = 'localhost';
    private $usuario = 'root';
    private $contrasena = '';
    private $bd = 'empresa';
    private $conexion;

    public function __construct() {
        try {
            // Crear una nueva conexión PDO
            $this->conexion = new PDO(
                "mysql:host=$this->host;dbname=$this->bd",
                $this->usuario,
                $this->contrasena,
                array(PDO::MYSQL_ATTR_INIT_COMMAND => "SET NAMES utf8")
            );
            // Configurar el modo de errores de PDO a excepciones
            $this->conexion->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        } catch (PDOException $e) {
            // Mostrar el mensaje de error si falla la conexión
            echo "Error de conexión: " . $e->getMessage();
        }
    }

    // Método para obtener la conexión
    public function conectar() {
        return $this->conexion;
    }
}
?>