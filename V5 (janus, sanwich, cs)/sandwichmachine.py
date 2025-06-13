import sys
import numpy as np
#################### DEFINITIONS #######################

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


def janus(atpos, z1, newel='Ni'):
    new_atpos = []
    for atom in atpos:
        if float(atom[3]) > z1:
            new_atpos.append([newel, atom[1], atom[2], atom[3]])
        else:
            new_atpos.append(atom)
    return new_atpos

def sandwich(atpos,z1,z2, newel='Ni'):
    if z2 > z1 or z1 == z2:
        print('wrong values, is necessary z1 > z2')
    new_atpos = []
    for atom in atpos:
        if float(atom[3]) < z1 and float(atom[3]) > z2:
            new_atpos.append([newel, atom[1], atom[2], atom[3]])
        else:
            new_atpos.append(atom)
    return new_atpos

def capas(atpos, r1, r2, newel='Ni'):
    if r2 > r1 or r1 == r2:
        print('wrong values, is necessary r1 > r2')
    new_atpos=[]
    for atom in atpos:
        r = np.sqrt(atom[1]**2 +atom[2]**2+atom[3]**2)
        if (r>r1 and r<r2):
            new_atpos.append([newel, atom[1], atom[2], atom[3]])
        else:
            new_atpos.append(atom)
    return new_atpos

def radcut(atpos, r1, r2):
    if r2>r1 or r1==r2:
        print('wrong values, is necessary r1 > r2')
    new_atpos=[]
    for atom in atpos:
        r = np.sqrt(atom[1]**2 +atom[2]**2+atom[3]**2)
        #print(r)
        if (r<r1 and r>r2):
            #print('b')
            new_atpos.append(atom)
    return new_atpos
          

def wXYZ(atpos,name_out):
        xyzfile = open(name_out,'w')
        n = len(atpos)
        xyzfile.write(str(n) +'\n\n')
        for ele,x,y,z in atpos:
                xyzfile.write('{0:2s}{1:12.5f}{2:12.5f}{3:12.5f}\n'.format(ele, x, y, z))
        xyzfile.close()

############################### PROGRAM ###############
#run: python sandwichmachine.py shell.xyz janus 0 0
# or: python sandwichmachine.py shell.pyz sandwich -1.13 1.13
        
name = sys.argv[1]
mode = sys.argv[2] #Mode = 'janus' or 'sandwich'
z1 = float(sys.argv[3]) #note: is necessary z1 > z2
z2 = float(sys.argv[4]) #if janus then z2 = z1
newele = ''

atpos, eleList = leer_xyz(name)

if mode == 'janus':
    z2 = z1
    atpos = janus(atpos,z1)
elif mode == 'sandwich':
    atpos = sandwich(atpos,z1,z2)
elif mode == 'capas':
    atpos = capas(atpos,r1=z1,r2=z2)
elif mode == 'radcut':
    atpos = radcut(atpos,r1=z1,r2=z2) #deja los atomos de r1>r>r2
else:
    print('no valid arguments')
    exit()

if 'Ni' in name:
    name = 'Ni-rad.xyz'
    print(name)
elif 'Pt' in name:
    name = 'Pt-rad.xyz'
    print(name)
else:
    print('no jala lo ultimo')
wXYZ(atpos,name)