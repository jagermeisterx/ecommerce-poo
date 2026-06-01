from catalogo import Catalogo
from usuarios import Admin, Cliente
from utils import separador, leer_texto


class Tienda:
    def __init__(self):
        self.catalogo = Catalogo()

    def iniciar(self):
        """Carga el catálogo y ejecuta el bucle principal de la tienda."""
        separador()
        print("*   BIENVENIDO AL ECOMMERCE CLI")
        separador()
        self.catalogo.cargar_desde_archivo()

        while True:
            usuario = self._seleccionar_rol()
            if usuario is None:  # el usuario eligió salir del programa
                print("Gracias por usar la tienda. ¡Hasta pronto!")
                break
            self._ejecutar_sesion(usuario)

    def _seleccionar_rol(self):
        """Pregunta el rol al inicio. Devuelve un Usuario o None para salir."""
        separador(40)
        print("* ¿Cómo desea ingresar?")
        print("* (1) ADMIN")
        print("* (2) CLIENTE")
        print("* (0) Salir del programa")
        separador(40)

        opcion = leer_texto("Seleccione una opción: ")
        if opcion == "1":
            nombre = leer_texto("Nombre del administrador: ")
            return Admin(nombre, self.catalogo)
        elif opcion == "2":
            nombre = leer_texto("Nombre del cliente: ")
            return Cliente(nombre, self.catalogo)
        elif opcion == "0":
            return None
        else:
            print("Opción no válida. Intente de nuevo.")
            return self._seleccionar_rol()

    def _ejecutar_sesion(self, usuario):
        """Bucle de menú genérico: funciona igual para Admin y Cliente.

        Es polimórfico: la Tienda no necesita saber el rol concreto, solo
        llama a mostrar_menu() y procesar_opcion() del usuario.
        """
        print(f"\nSesión iniciada como {usuario.rol}: {usuario.nombre}")
        activo = True
        while activo:
            usuario.mostrar_menu()
            try:
                opcion = int(input("Ingrese la opción deseada: "))
            except ValueError:
                print("Ingrese una opción válida (número).")
                continue
            activo = usuario.procesar_opcion(opcion)
