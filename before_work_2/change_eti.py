import sys

def cambiar_etiquetas_xyz(nombre_archivo, dict_etiquetas, nombre_archivo_salida):
    with open(nombre_archivo) as f:
        lineas = f.readlines()

    num_atomos = int(lineas[0])
    atpos = []

    for linea in lineas[2:2 + num_atomos]:
        partes = linea.split()
        etiqueta = int(partes[0])
        x, y, z = map(float, partes[1:])
        if etiqueta in dict_etiquetas:
            elemento = dict_etiquetas[etiqueta]
        else:
            print(f"Advertencia: No se encontró la etiqueta {etiqueta} en el diccionario de etiquetas. Se usará la etiqueta original.")
            elemento = str(etiqueta)
        atpos.append([elemento, x, y, z])

    with open(nombre_archivo_salida, 'w') as f:
        f.write(str(num_atomos) + '\n\n')
        for atom in atpos:
            f.write('{0:2s}{1:12.5f}{2:12.5f}{3:12.5f}\n'.format(atom[0], atom[1], atom[2], atom[3]))


if __name__ == '__main__':
    dump = sys.argv[1]
    dict_etiquetas = {1: 'Pt', 2: 'Pd', 3: 'Co'}  # Diccionario de etiquetas

cambiar_etiquetas_xyz(dump, dict_etiquetas, dump)