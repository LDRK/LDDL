<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/sweetalert/dist/sweetalert.min.js"></script>
    <link rel="stylesheet" href="../../assets/css/style.css">
    <title>Singup</title>
</head>

<body>


    <div class=" flex min-h-full flex-col justify-center px-6 py-12 lg:px-8 ">
        <div class="sm:mx-auto sm:w-full sm:max-w-md h-full shadow-lg rounded-md form-registro">
            <div class="sm:mx-auto sm:w-full sm:max-w-sm">
                <img class="mx-auto h-10 w-auto" src="https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=600"
                    alt="Your Company">
                <h2 class="mt-1 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">Registro </h2>
            </div>

            <div class="mt-6 sm:mx-auto sm:w-full sm:max-w-sm ">
                <form class="space-y-6" id="formSingup">
                    <div>
                        <label for="nombre" class="block text-sm font-medium leading-6 text-black">Nombre</label>
                        <div class="mt-2">
                            <input id="nombre" name="nombre" type="text" autocomplete="" required
                                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 pl-2">
                        </div>
                    </div>
                    <div>
                        <label for="usuario" class="block text-sm font-medium leading-6 text-black">Usuario</label>
                        <div class="mt-2">
                            <input id="usuario" name="usuario" type="text" autocomplete="" required
                                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 pl-2">
                        </div>
                    </div>
                    <div>
                        <label for="email" class="block text-sm font-medium leading-6 text-black">Correo</label>
                        <div class="mt-2">
                            <input id="correo" name="correo" type="email" autocomplete="email" required
                                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 pl-2">
                        </div>
                    </div>
                    <div>
                        <label for="contrasena"
                            class="block text-sm font-medium leading-6 text-black">Contraseña</label>
                        <div class="mt-2">
                            <input id="contrasena" name="contrasena" type="password" autocomplete="" required
                                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 pl-2">
                        </div>

                    </div>




                    <div>
                        <button type="submit"
                            class="flex w-full justify-center rounded-md  px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm  focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 btn-registro "
                            name="btn-singup">Registrar</button>
                    </div>
                </form>

                <p class="mt-7 text-center text-sm  p-regitrar">
                    Ya tienes cuenta?
                    <a href="./login.php" class="font-semibold leading-6  a-regitrar">Iniciar
                        Sesion</a>
                </p>
            </div>
        </div>

    </div>

    <script src="../../assets/js/scriptLogica.js " defer></script>
</body>

</html>