import sys, os
import random as ran
import numpy as np
#import subprocess
#from operator import itemgetter
import shutil

def cambiar_etiquetas_xyz(atpos, eleList, dict_etiquetas):
    new_atpos=[]
    print(f'Cambia etiquetas a {name}')
    for atom in atpos:
        if int(atom[0]) in dict_etiquetas:
            elemento = dict_etiquetas[int(atom[0])]
        else:
            print(f"Advertencia: No se encontró la etiqueta {atom[0]} en el diccionario de etiquetas. Se usará la etiqueta original.")
            elemento = str(atom[0])
        new_atpos.append([elemento, atom[1], atom[2], atom[3]])
    return new_atpos, eleList

def spherical_cut(atpos, eleList, radius):
    print(f'Corta esfericamente a {name}')
    new_atpos = [atom for atom in atpos if np.sqrt(atom[1]**2 + atom[2]**2 + atom[3]**2) <= radius]
    return new_atpos, eleList


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
    print(f'Cambia elementos prob a {name}')
    new_atpos = []
    new_eleList = []
    for atom in atpos:
        nuevo_elemento = ran.choices(list(dict_elementos.keys()), weights=list(dict_elementos.values()), k=1)[0]
        if ran.random() < dict_elementos[nuevo_elemento]:
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


def mover_archivo(carpeta_origen, carpeta_destino, archivo_buscado):
    origen = os.path.join(carpeta_origen, archivo_buscado)
    destino = os.path.join(carpeta_destino, archivo_buscado)
    shutil.move(origen, destino)

def modify_md9(t_relax):
    with open('lammps/md9-temp.in', 'r') as file:
        lines = file.readlines()
    for i, line in enumerate(lines):
        if line.startswith('fix         3'):
            words = line.split()
            words[5] = str(t_relax) + '.0'
            lines[i] = ' '.join(words) + '\n'
        if line.startswith('fix         4'):
            words = line.split()
            words[5] = str(t_relax) + '.0'
            words[6] = str(t_relax) + '.0'
            lines[i] = ' '.join(words) + '\n'
    with open('lammps/md9-temp.in', 'w') as file:
        file.writelines(lines)

def modify_dump(dump_number):
    with open('lammps/md9-temp.in', 'r') as file:
        lines = file.readlines()
    for i, line in enumerate(lines):
        if ('dump.xyz') in line:
            lines[i] = line.replace('dump.xyz', 'dump'+str(dump_number) + '.xyz')
        elif ('dump-1.xyz') in line:
            lines[i] = line.replace('dump-1.xyz', 'dump'+ str(dump_number) + '-1.xyz')
    with open('lammps/md9-temp.in', 'w') as file:
        # Escribe todas las líneas de nuevo en el archivo
        file.writelines(lines)

def modify_str_coords(nf):
    with open('lammps/md9-temp.in', 'r') as file:
        lines = file.readlines()
    for i, line in enumerate(lines):
        if 'coords.ini' in line:
            lines[i] = line.replace('coords.ini', 'coords' + str(nf) + '.ini')
    with open('lammps/md9-temp.in', 'w') as file:
        file.writelines(lines)


#####################################################################################################################
###################### PROGRAMA ############################################3
###################################################################################################################3

name = sys.argv[1]
atpos, eleList = leer_xyz(name)

etiquetas = {1: 'Ni', 2: 'Pt'}
atpos,eleList = cambiar_etiquetas_xyz(atpos,eleList,etiquetas)

wXYZ(atpos,name)


