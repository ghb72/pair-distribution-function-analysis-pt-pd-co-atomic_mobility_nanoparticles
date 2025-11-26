import sys

def leer_xyz(nombre_archivo):
    with open(nombre_archivo) as f:
        lineas = f.readlines()

    num_atomos = int(lineas[0])
    atpos = []
    eleList = []

    for linea in lineas[2:2 + num_atomos]:
        partes = linea.split()
        elemento = partes[0]
        x, y, z = map(float, partes[1:])
        atpos.append([elemento, x, y, z])
        if elemento not in eleList:
            eleList.append(elemento)
    return atpos, eleList


def percent(atpos, eleList):
    tot = len(atpos)
    print(f'atomos totales : {tot}')
    for element in eleList:
        empty = []
        for atom in atpos:
            if atom[0] == element:
                empty.append(atom[0])
        percentes=len(empty)
        print(f'{element} : {100*percentes/tot} %, {percentes}')
    


name = sys.argv[1]
atpos, eleList = leer_xyz(name)
print(name)
percent(atpos,eleList)