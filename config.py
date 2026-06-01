# Configuración de rutas de archivos.
import os

# Carpeta donde vive este archivo y carpeta de datos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Archivos de persistencia
RUTA_CATALOGO = os.path.join(DATA_DIR, "catalogo.csv")
RUTA_ORDENES = os.path.join(DATA_DIR, "ordenes.txt")

# Separador usado en el CSV (";" para no chocar con comas dentro de los nombres)
SEPARADOR_CSV = ";"
