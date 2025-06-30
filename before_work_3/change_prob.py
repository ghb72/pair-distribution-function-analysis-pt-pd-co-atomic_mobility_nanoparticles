import sys
import random as ran

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


def cambiar_elementos_prob(atpos, dict_elementos):
    # Crear una nueva lista de posiciones atómicas
    new_atpos = []
    new_eleList = []
    for atom in atpos:
        # Elegir un nuevo elemento al azar de la lista de nuevos elementos
        nuevo_elemento = ran.choices(list(dict_elementos.keys()), weights=list(dict_elementos.values()), k=1)[0]
        # Cambiar el elemento con la probabilidad dada
        if ran.random() < dict_elementos[nuevo_elemento]:
            new_atpos.append([nuevo_elemento, atom[1], atom[2], atom[3]])
            if nuevo_elemento not in new_eleList:
                new_eleList.append(nuevo_elemento)
        else:
            new_atpos.append(atom)
            if atom[0] not in new_eleList:
                new_eleList.append(atom[0])
    return new_atpos, new_eleList

def cambiar_elementos_prop_2(atpos, dict_elementos):
    # Crear una nueva lista de posiciones atómicas
    new_atpos = []
    new_eleList = []
    total = len(atpos)
    counts = {elemento: int(total * prop) for elemento, prop in dict_elementos.items()}

    for atom in atpos:
        # Elegir un nuevo elemento al azar de la lista de nuevos elementos
        elementos_posibles = [ele for ele in counts.keys() if counts[ele] > 0]
        if elementos_posibles:
            nuevo_elemento = ran.choice(elementos_posibles)
            counts[nuevo_elemento] -= 1
            new_atpos.append([nuevo_elemento, atom[1], atom[2], atom[3]])
            if nuevo_elemento not in new_eleList:
                new_eleList.append(nuevo_elemento)
        else:
            new_atpos.append(atom)
            if atom[0] not in new_eleList:
                new_eleList.append(atom[0])

    return new_atpos, new_eleList


def wXYZ(atpos,name_out):

        xyzfile = open(name_out,'w')
        n = len(atpos)
        xyzfile.write(str(n) +'\n\n')
        for ele,x,y,z in atpos:
                xyzfile.write('{0:2s}{1:12.5f}{2:12.5f}{3:12.5f}\n'.format(ele, x, y, z))
        xyzfile.close()


###############################33
# cambia elementos con probabilidad#################
name = sys.argv[1] #archivo de entrada
atpos, eleList = leer_xyz(name) #lee el xyz

dict_elementos = {'Pt': 28, 'Pd': 45, 'Co': 27}  # Diccionario de nuevos elementos y sus probabilidades
# Pt 28%, Pd 45% y Co 27%.
new_atpos,new_eleList = cambiar_elementos_prob(atpos, dict_elementos)
#new_atpos, new_eleList = cambiar_elementos_prop_2(atpos,dict_elementos)
wXYZ(new_atpos,name[:-4]+'_p.xyz')