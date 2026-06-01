def separador(largo=50):
    """Imprime una línea de asteriscos (estilo heredado del Módulo 3)."""
    print("*" * largo)


def leer_texto(mensaje, permitir_vacio=False):
    """Lee texto desde consola. Por defecto no permite vacío."""
    while True:
        valor = input(mensaje).strip()
        if valor or permitir_vacio:
            return valor
        print("El valor no puede estar vacío.")


def leer_entero(mensaje, minimo=None):
    """Lee un entero validando el formato y, si se indica, un mínimo.

    Devuelve None si el usuario ingresa algo no numérico (para que el
    llamador decida qué hacer).
    """
    try:
        valor = int(input(mensaje))
    except ValueError:
        print("Debe ingresar un número entero.")
        return None

    if minimo is not None and valor < minimo:
        print(f"El valor debe ser mayor o igual a {minimo}.")
        return None
    return valor
