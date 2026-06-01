from config import SEPARADOR_CSV


class Producto:
    """Representa un producto con id, nombre, categoría y precio."""

    def __init__(self, id_producto, nombre, categoria, precio):
        self.id = id_producto
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio

    def __str__(self):
        # Formato amigable para listados (precio con separador de miles)
        return (f"[{self.id}] {self.nombre} | {self.categoria} | "
                f"${self.precio:,.0f}")

    def to_csv(self):
        """Serializa el producto a una línea de texto para el archivo."""
        return (f"{self.id}{SEPARADOR_CSV}{self.nombre}{SEPARADOR_CSV}"
                f"{self.categoria}{SEPARADOR_CSV}{self.precio}")

    @staticmethod
    def from_csv(linea):
        """Crea un Producto a partir de una línea del archivo.

        Lanza ValueError si la línea no tiene el formato esperado.
        """
        partes = linea.strip().split(SEPARADOR_CSV)
        if len(partes) != 4:
            raise ValueError(f"Línea de catálogo inválida: {linea!r}")

        id_producto = int(partes[0])
        nombre = partes[1]
        categoria = partes[2]
        precio = int(float(partes[3]))  # admite "2500" o "2500.0"
        return Producto(id_producto, nombre, categoria, precio)
