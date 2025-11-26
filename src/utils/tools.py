"""
Utility functions for XYZ file manipulation and atomic structure processing.

This module provides tools for:
- Reading and writing XYZ atomic coordinate files
- Modifying atomic labels and compositions
- Spherical cutting and spatial filtering
- LAMMPS template file manipulation
"""

import sys, os
import random as ran
import numpy as np
import shutil

def cambiar_etiquetas_xyz(atpos, eleList, dict_etiquetas):
    """
    Change atomic labels according to a mapping dictionary.
    
    Args:
        atpos: List of atoms [element, x, y, z]
        eleList: List of unique elements
        dict_etiquetas: Dictionary mapping old labels to new element symbols
        
    Returns:
        Tuple of (new_atpos, eleList)
    """
    new_atpos=[]
    print(f'Cambia etiquetas a {name}')
    for atom in atpos:
        if int(atom[0]) in dict_etiquetas:
            elemento = dict_etiquetas[int(atom[0])]
        else:
            print(f"Warning: Label {atom[0]} not found in label dictionary. Using original label.")
            elemento = str(atom[0])
        new_atpos.append([elemento, atom[1], atom[2], atom[3]])
    return new_atpos, eleList

def spherical_cut(atpos, eleList, radius):
    """
    Cut a spherical region from atomic positions.
    
    Args:
        atpos: List of atoms [element, x, y, z]
        eleList: List of unique elements
        radius: Cutoff radius in Angstroms
        
    Returns:
        Tuple of (new_atpos, eleList) with only atoms within radius
    """
    print(f'Corta esfericamente a {name}')
    new_atpos = [atom for atom in atpos if np.sqrt(atom[1]**2 + atom[2]**2 + atom[3]**2) <= radius]
    return new_atpos, eleList


def leer_xyz(nombre_archivo):
    """
    Read XYZ atomic coordinate file.
    
    Args:
        nombre_archivo: Path to XYZ file
        
    Returns:
        Tuple of (atpos, eleList) where atpos is list of [element, x, y, z]
        and eleList contains unique element symbols
    """
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
    """
    Change atomic elements probabilistically according to weights.
    
    Args:
        atpos: List of atoms [element, x, y, z]
        dict_elementos: Dictionary with element symbols as keys and probabilities as values
        
    Returns:
        Tuple of (new_atpos, new_eleList)
    """
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


def wXYZ(atpos, name_out):
    """
    Write atomic positions to XYZ file.
    
    Args:
        atpos: List of atoms [element, x, y, z]
        name_out: Output filename
    """
    with open(name_out, 'w') as xyzfile:
        n = len(atpos)
        xyzfile.write(str(n) +'\n\n')
        for ele, x, y, z in atpos:
            xyzfile.write('{0:2s}{1:12.5f}{2:12.5f}{3:12.5f}\n'.format(ele, x, y, z))


def mover_archivo(carpeta_origen, carpeta_destino, archivo_buscado):
    """
    Move a file from one directory to another.
    
    Args:
        carpeta_origen: Source directory
        carpeta_destino: Destination directory
        archivo_buscado: Filename to move
    """
    origen = os.path.join(carpeta_origen, archivo_buscado)
    destino = os.path.join(carpeta_destino, archivo_buscado)
    shutil.move(origen, destino)

def modify_md9(t_relax):
    # Define paths relative to this file
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', '..'))
    LAMMPS_TEMPLATE_PATH = os.path.join(PROJECT_ROOT, 'data', 'lammps_resources', 'templates', 'md9-temp.in')
    
    with open(LAMMPS_TEMPLATE_PATH, 'r') as file:
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
    with open(LAMMPS_TEMPLATE_PATH, 'w') as file:
        file.writelines(lines)

def modify_dump(dump_number):
    # Define paths relative to this file
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', '..'))
    LAMMPS_TEMPLATE_PATH = os.path.join(PROJECT_ROOT, 'data', 'lammps_resources', 'templates', 'md9-temp.in')

    with open(LAMMPS_TEMPLATE_PATH, 'r') as file:
        lines = file.readlines()
    for i, line in enumerate(lines):
        if ('dump.xyz') in line:
            lines[i] = line.replace('dump.xyz', 'dump'+str(dump_number) + '.xyz')
        elif ('dump-1.xyz') in line:
            lines[i] = line.replace('dump-1.xyz', 'dump'+ str(dump_number) + '-1.xyz')
    with open(LAMMPS_TEMPLATE_PATH, 'w') as file:
        # Escribe todas las líneas de nuevo en el archivo
        file.writelines(lines)

def modify_str_coords(nf):
    # Define paths relative to this file
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', '..'))
    LAMMPS_TEMPLATE_PATH = os.path.join(PROJECT_ROOT, 'data', 'lammps_resources', 'templates', 'md9-temp.in')

    with open(LAMMPS_TEMPLATE_PATH, 'r') as file:
        lines = file.readlines()
    for i, line in enumerate(lines):
        if 'coords.ini' in line:
            lines[i] = line.replace('coords.ini', 'coords' + str(nf) + '.ini')
    with open(LAMMPS_TEMPLATE_PATH, 'w') as file:
        file.writelines(lines)


#####################################################################################################################
###################### PROGRAMA ############################################3
###################################################################################################################3

def main(name):
    atpos, eleList = leer_xyz(name)

    etiquetas = {1: 'Ni', 2: 'Pt'}
    atpos,eleList = cambiar_etiquetas_xyz(atpos,eleList,etiquetas)

    wXYZ(atpos,name)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Usage: python tools.py <filename>")


