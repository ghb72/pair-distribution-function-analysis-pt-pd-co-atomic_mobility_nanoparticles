"""
Sandwich Machine: Create various atomic arrangements (Janus, sandwich, core-shell) in nanoparticles.

This script modifies atomic structures to create different configurations:
- Janus: Two hemispheric regions with different elements
- Sandwich: Layered structure along z-axis
- Core-shell (cs): Spherical shell of one element around a core
- Radial cut: Select atoms within a radial range
- Make small: Cut nanoparticle to specified radius

Usage:
    python sandwichmachine.py <input.xyz> <mode> <param1> <param2>
    
Examples:
    python sandwichmachine.py Ni-FCC.xyz janus 0 0
    python sandwichmachine.py Pt-FCC.xyz sandwich -1.13 1.13
    python sandwichmachine.py Ni-FCC.xyz cs 8.0 10.0
"""

import sys
import numpy as np

#################### DEFINITIONS #######################

def leer_xyz(nombre_archivo):
    """
    Read XYZ atomic coordinate file.
    
    Args:
        nombre_archivo: Path to XYZ file
        
    Returns:
        Tuple of (atpos, eleList)
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


def janus(atpos, z1, newel):
    """
    Create Janus structure: atoms on one side of plane x=z1 become newel.
    
    Args:
        atpos: Atomic positions
        z1: Position of dividing plane
        newel: New element symbol
        
    Returns:
        Modified atomic positions
    """
    new_atpos = []
    for atom in atpos:
        if atom[1]<z1:
            new_atpos.append([newel, atom[1], atom[2], atom[3]])
        else:
            new_atpos.append(atom)
    return new_atpos

def sandwich(atpos, z1, z2, newel):
    """
    Create sandwich structure: atoms between z2 and z1 become newel.
    
    Args:
        atpos: Atomic positions
        z1: Upper z boundary (must be > z2)
        z2: Lower z boundary
        newel: New element symbol
        
    Returns:
        Modified atomic positions
    """
    if z2 > z1 or z1 == z2:
        print('wrong values, is necessary z1 > z2')
    new_atpos = []
    for atom in atpos:
        if float(atom[3]) < z1 and float(atom[3]) > z2:
            new_atpos.append([newel, atom[1], atom[2], atom[3]])
        else:
            new_atpos.append(atom)
    return new_atpos

def capas(atpos, r1, r2, newel):
    """
    Create core-shell structure: atoms between radii r1 and r2 become newel.
    
    Args:
        atpos: Atomic positions
        r1: Inner radius
        r2: Outer radius (must be > r1)
        newel: New element symbol
        
    Returns:
        Modified atomic positions
    """
    if r1 > r2 or r1 == r2:
        print('wrong values, is necessary r1 < r2')
        exit()
    new_atpos=[]
    for atom in atpos:
        r = np.sqrt(atom[1]**2 +atom[2]**2+atom[3]**2)
        if (r>r1 and r<=r2):
            new_atpos.append([newel, atom[1], atom[2], atom[3]])
        else:
            new_atpos.append(atom)
    return new_atpos

def radcut(atpos, r1, r2):
    """
    Select atoms within radial range r2 <= r < r1.
    
    Args:
        atpos: Atomic positions
        r1: Outer radius (must be > r2)
        r2: Inner radius
        
    Returns:
        Filtered atomic positions
    """
    if r2>r1 or r1==r2:
        print('wrong values, is necessary r1 > r2')
    new_atpos=[]
    for atom in atpos:
        r = np.sqrt(atom[1]**2 +atom[2]**2+atom[3]**2)
        #print(r)
        if (r<r1 and r>=r2):
            #print('b')
            new_atpos.append(atom)
    return new_atpos

def makesmall(atpos,r1):
    if r1 <= 0: 
        print('wrong value of radius')
        exit()
    new_atpos = []
    for atom in atpos:
        r = np.sqrt(atom[1]**2 +atom[2]**2+atom[3]**2)
        #print(r)
        if (r<=r1):
            new_atpos.append(atom)
    return new_atpos
    
          

def wXYZ(atpos,name_out):
        xyzfile = open(name_out,'w')
        n = len(atpos)
        xyzfile.write(str(n) +'\n\n')
        for ele,x,y,z in atpos:
                xyzfile.write('{0:2s}{1:12.5f}{2:12.5f}{3:12.5f}\n'.format(ele, x, y, z))
        xyzfile.close()

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
############################### PROGRAM ###############
#run: python sandwichmachine.py shell.xyz janus 0 0
# or: python sandwichmachine.py shell.pyz sandwich -1.13 1.13
        
if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python sandwichmachine.py <filename> <mode> <z1> <z2>")
        sys.exit(1)

    name = sys.argv[1]
    mode = sys.argv[2] #Mode = 'janus' or 'sandwich' or 'radcut' or 'makesmall'
    z1 = float(sys.argv[3]) #note: is necessary z1 > z2
    z2 = float(sys.argv[4]) #if janus then z2 = z1

    atpos, eleList = leer_xyz(name)
    if 'Ni' in name: 
        newele='Pt'
        name = f'Ni-{mode}-{z2}-{z1}.xyz'
        print(name)
    elif 'Pt' in name:
        newele='Ni'
        name = f'Pt-{mode}-{z2}-{z1}.xyz'
        print(name)
    else: print('algo ha ocurrido')

    if mode == 'janus':
        z2 = z1
        atpos = janus(atpos,z1,newele)
    elif mode == 'sandwich':
        atpos = sandwich(atpos,z1,z2,newele)
    elif mode == 'cs':
        r1,r2 = z1,z2
        atpos = capas(atpos,r1,r2,newele)
    elif mode == 'radcut':
        atpos = radcut(atpos,r1=z1,r2=z2) #deja los atomos de r1>r>r2
    elif mode == 'makesmall':
        z2 = z1
        atpos = makesmall(atpos,z1)
    else:
        print('no valid arguments')
        exit()

    if not (mode == 'makesmall'):
        percent(atpos,['Ni','Pt'])

    yes = input("It's ok the model? [Y/N]:\n")
    if yes =='N' or yes =='n':
        exit()
    elif yes =='Y' or yes =='y':
        wXYZ(atpos,name)
    else:
        print('Incorrect response')
        exit()