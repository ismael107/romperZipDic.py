#!/usr/bin/env python
import zipfile
import sys
import os

if len(sys.argv) != 3:
    print("Uso: python fuerzaBrutaZip.py <archivo_zip> <archivo_contraseñas>")
    sys.exit(1)

# Abre el archivo zip y el archivo de contraseñas
zFile = zipfile.ZipFile(sys.argv[1], "r")
passFile = open(sys.argv[2], "r")

# Lee las contraseñas del archivo
passwords = passFile.readlines()

# Abre /dev/null para redirigir las contraseñas incorrectas
with open(os.devnull, 'w') as devnull:
    # Intenta cada contraseña
    for password in passwords:
        password = password.strip()  # Elimina cualquier espacio o salto de línea
        try:
            # Itera sobre los archivos dentro del zip
            for info in zFile.infolist():
                # Intenta abrir el archivo con la contraseña
                zFile.extract(info, pwd=password.encode('utf-8'))
            # Si llegamos aquí, significa que la contraseña es correcta para todos los archivos
            print("password encontrado: " + password)
            zFile.close()
            passFile.close()
            sys.exit(0)  # Sal del script si la contraseña es encontrada
        except (RuntimeError, zipfile.BadZipFile, zipfile.LargeZipFile) as e:
            if 'Bad password for file' in str(e):
                print(f"Contraseña incorrecta: {password}", file=devnull)
            else:
                print(f"Error desconocido: {e}", file=devnull)
        except Exception as e:
            print(f"Error desconocido: {e}", file=devnull)

# Cierra los archivos abiertos
zFile.close()
passFile.close()
print("No se encontró la contraseña correcta.")
sys.exit(1)
