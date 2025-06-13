import random
import sys

def eliminar_atomos(nombre_archivo, porcentaje):
    with open(nombre_archivo, 'r') as archivo:
        lineas = archivo.readlines()

    # Excluimos las dos primeras líneas
    atomos = lineas[2:]
    num_atomos = len(atomos)

    # Calculamos cuántos átomos eliminar
    num_eliminar = int(num_atomos * porcentaje / 100)

    # Eliminamos aleatoriamente átomos
    for _ in range(num_eliminar):
        atomos.remove(random.choice(atomos))

    # Actualizamos la primera línea con la nueva cantidad de átomos
    lineas[0] = str(len(atomos)) + '\n'

    # Escribimos el resultado en el archivo
    with open(nombre_archivo, 'w') as archivo:
        archivo.writelines(lineas[:2] + atomos)

# Usamos la función con el archivo 'dump-5.xyz' y un porcentaje del 10%
name=sys.argv[1]
percent=int(sys.argv[2])
eliminar_atomos(name, percent)
