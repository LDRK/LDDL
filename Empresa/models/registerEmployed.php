<?php
require_once '../models/connection/connection.php';

class Personal{
    private $conexion;

    public function __construct(){
        $this->conexion = new Conexion();
        $this->conexion = $this->conexion->conectar();
    }

    public function crearEmpleado($nombre, $apellidoPaterno, $apellidoMaterno, $correo, $departamento, $foto) {
        $query = "INSERT INTO empleado(nombre, apellido_paterno, apellido_materno, correo, departamento, foto) VALUES (:nombre, :apellidoPaterno, :apellidoMaterno, :correo, :departamento, :foto)";
                  
        $stmt = $this->conexion->prepare($query);
        $stmt->bindParam(':nombre', $nombre);
        $stmt->bindParam(':apellidoPaterno', $apellidoPaterno);
        $stmt->bindParam(':apellidoMaterno', $apellidoMaterno);
        $stmt->bindParam(':correo', $correo);  // Aquí estaba faltando este parámetro
        $stmt->bindParam(':departamento', $departamento);
        $stmt->bindParam(':foto', $foto);
    
        return $stmt->execute();
    }
    
}


?>