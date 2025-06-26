from interfax import launch_gui
import subprocess
import sys

# Función para instalar paquetes
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


libraries = [ 'numpy', 'pandas', 'tkinter', 'ipaddress', 'Pillow', 'openpyxl'] 

for lib in libraries:
    try:
        __import__(lib)
    except ImportError:
        print(f"{lib} no está instalado. Instalando...")
        install(lib)

if __name__ == "__main__":
    launch_gui()
