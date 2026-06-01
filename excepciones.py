"""Excepciones personalizadas del ecommerce.
Todas heredan de EcommerceError para poder capturarlas de forma general
cuando convenga, o de forma específica cuando se necesite un mensaje propio.
"""


class EcommerceError(Exception):
    # Excepción base del dominio del ecommerce.
    pass


class ProductoNoEncontradoError(EcommerceError):
    # Se lanza cuando no existe un producto con el ID buscado.
    pass


class CantidadInvalidaError(EcommerceError):
    # Se lanza cuando la cantidad no es un entero mayor que 0.
    pass


class CarritoVacioError(EcommerceError):
    # Se lanza al intentar confirmar una compra con el carrito vacío.
    pass


class IdDuplicadoError(EcommerceError):
    # Se lanza al intentar crear un producto con un ID ya existente.
    pass
