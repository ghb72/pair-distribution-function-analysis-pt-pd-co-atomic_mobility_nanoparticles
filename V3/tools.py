import sys, os
import random as ran
import numpy as np
import subprocess
from operator import itemgetter
import shutil

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


def wlammpin(atpos,eleList,NL_out):

    lin = open(NL_out,'w')
    n = len(atpos)
    m = len(eleList)

    w = []
    for atom in atpos:
        ele, x, y, z = atom
        w += [x,y,z]
    low = min(w) - 10.0
    high = max(w) + 10.0 

    lin.write('LAMMPS DATA FOR MEAM SIMULATION\n\n')
    lin.write('{0:7d}   atoms\n'.format(n))
    lin.write('{0:7d}   atom types\n\n'.format(m))
    lin.write('{0:8.2f}{1:8.2f}   xlo xhi\n'.format(low,high))
    lin.write('{0:8.2f}{1:8.2f}   ylo yhi\n'.format(low,high))
    lin.write('{0:8.2f}{1:8.2f}   zlo zhi\n\n'.format(low,high))
    lin.write(' Atoms\n\n')
    for i in range(n):
        ele, x, y, z = atpos[i]
        if ele == 'Pt':
            j = 1
        elif ele == 'Pd':
            j = 2
        elif ele == 'Co':
            j = 3
        lin.write('{0:6d}{1:4d}{2:12.5f}{3:12.5f}{4:12.5f}\n'.format(i+1, j, x, y, z))
    lin.close()


def spherical_cut(atpos, radius, file_out):
    # Crear una nueva lista de posiciones atómicas que estén dentro del radio dado
    new_atpos = [atom for atom in atpos if np.sqrt(atom[1]**2 + atom[2]**2 + atom[3]**2) <= radius]

    # Escribir las nuevas posiciones atómicas en un archivo .xyz
    with open(file_out , 'w') as f:
        f.write(str(len(new_atpos)) + '\n\n')
        for atom in new_atpos:
            f.write('{0:2s}{1:12.5f}{2:12.5f}{3:12.5f}\n'.format(atom[0], atom[1], atom[2], atom[3]))

# Uso de la función
# atpos, eleList = getStr(name)  # Obtener las posiciones atómicas del archivo de entrada
# spherical_cut(atpos, radius)  # Realizar el corte esférico y escribir el nuevo archivo .xyz

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

def calcular_rdf(atomos, nhis=6000, delr=0.01):
    npart = len(atomos)
    box = nhis * delr
    g = np.zeros(nhis)
    h = np.zeros(nhis)

    m = npart * (npart - 1) // 2
    rmin = 10.0
    rmax = 0.0
    rmed = 0.0
    hint = 0.0

    for i in range(npart - 1):
        for j in range(i + 1, npart):
            dx = atomos[i][1] - atomos[j][1]
            dy = atomos[i][2] - atomos[j][2]
            dz = atomos[i][3] - atomos[j][3]
            r = np.sqrt(dx**2 + dy**2 + dz**2)

            if r < box:
                ig = int(r / delr - 0.5)
                g[ig] += 2
                h[ig] += 2.0 / (r * delr)
                hint += 1 / r
                rmed += r
                rmin = min(rmin, r)
                rmax = max(rmax, r)

    rmed /= m
    h /= hint

    return rmin, rmax, rmed, hint, h

def suavizar(h, nh):
    k = nh // 2
    nhis = len(h)
    f = np.zeros(nhis)

    for i in range(nhis):
        x = 0.0
        for j in range(i - k, i + k + 1):
            if j >= 0 and j < nhis:
                x += h[j]
        f[i] = x / (2 * k + 1)

    return f

def escribir_rdf(h, fileout, delr=0.01):
    with open( fileout , 'w') as f:
        f.write('# r           PDF\n')
        for i in range(len(h)):
            r = i * delr
            f.write(f'{r} {h[i]}\n')

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


def wXYZ(atpos,name_out):

        xyzfile = open(name_out,'w')
        n = len(atpos)
        xyzfile.write(str(n) +'\n\n')
        for ele,x,y,z in atpos:
                xyzfile.write('{0:2s}{1:12.5f}{2:12.5f}{3:12.5f}\n'.format(ele, x, y, z))
        xyzfile.close()

def quitestepsxyz(filein):
    with open(filein) as fi:
        lineas = fi.readlines()

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

def quitlines(file):
    with open(file, 'r') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if '5017\n Atoms. Timestep: 6000' in line:
            lines = lines[i:]
            break

    with open(file, 'w') as f:
        f.writelines(lines)


def mover_archivo(carpeta_origen, carpeta_destino, archivo_buscado):
    """
    Mueve un archivo específico de la carpeta de origen a la carpeta de destino.

    Parámetros:
    carpeta_origen (str): La ruta de la carpeta de origen.
    carpeta_destino (str): La ruta de la carpeta de destino.
    archivo_buscado (str): El nombre del archivo que se desea mover.
    """

    # Crea las rutas completas de origen y destino para el archivo
    origen = os.path.join(carpeta_origen, archivo_buscado)
    destino = os.path.join(carpeta_destino, archivo_buscado)

    # Mueve el archivo de la carpeta de origen a la de destino
    shutil.move(origen, destino)

def modify_md9(t_relax):
    # Abre el archivo en modo de lectura
    with open('lammps/md9-temp.in', 'r') as file:
        # Lee todas las líneas del archivo
        lines = file.readlines()

    # Recorre todas las líneas
    for i, line in enumerate(lines):
        # Si la línea comienza con 'fix		3', la modifica
        if line.startswith('fix         3'):
            # Divide la línea en palabras
            words = line.split()
            # Cambia la palabra en la posición 5 por t_relax
            words[5] = str(t_relax) + '.0'
            # Une las palabras de nuevo en una línea
            lines[i] = ' '.join(words) + '\n'
        if line.startswith('fix         4'):
            words = line.split()
            words[5] = str(t_relax) + '.0'
            words[6] = str(t_relax) + '.0'
            lines[i] = ' '.join(words) + '\n'


    # Abre el archivo en modo de escritura
    with open('lammps/md9-temp.in', 'w') as file:
        # Escribe todas las líneas de nuevo en el archivo
        file.writelines(lines)

def modify_dump(dump_number):
    # Abre el archivo en modo de lectura
    with open('lammps/md9-temp.in', 'r') as file:
        # Lee todas las líneas del archivo
        lines = file.readlines()

    # Recorre todas las líneas
    for i, line in enumerate(lines):
        # Si la línea contiene 'dump.xyz', la modifica
        if ('dump.xyz') in line:
            lines[i] = line.replace('dump.xyz', 'dump'+str(dump_number) + '.xyz')
        # Si la línea contiene 'dump-1.xyz', la modifica
        elif ('dump-1.xyz') in line:
            lines[i] = line.replace('dump-1.xyz', 'dump'+ str(dump_number) + '-1.xyz')

    # Abre el archivo en modo de escritura
    with open('lammps/md9-temp.in', 'w') as file:
        # Escribe todas las líneas de nuevo en el archivo
        file.writelines(lines)

def modify_str_coords(nf):
    # Abre el archivo en modo de lectura
    with open('lammps/md9-temp.in', 'r') as file:
        # Lee todas las líneas del archivo
        lines = file.readlines()

    # Recorre todas las líneas
    for i, line in enumerate(lines):
        # Si la línea contiene 'coords.ini', la modifica
        if 'coords.ini' in line:
            lines[i] = line.replace('coords.ini', 'coords' + str(nf) + '.ini')

    # Abre el archivo en modo de escritura
    with open('lammps/md9-temp.in', 'w') as file:
        # Escribe todas las líneas de nuevo en el archivo
        file.writelines(lines)


#####################################################################################################################
###################### PROGRAMA ############################################3
###################################################################################################################3


################################################################3
######## next three functions doesnt work, dont try to fix it  ##########

#rmin, rmax, rmed, hint, h = calcular_rdf(atpos) 
#h = suavizar(h, 5)
#escribir_rdf(h,name_out)


############################################
# escribe el shell


###############################33
# cambia elementos con probabilidad#################
name = 'shells\shellPd.xyz' #archivo de entrada

ni = int(sys.argv[1]) #3 #numero de prueba - relacionada con la temperatura final ni=3->300k con ni>3
dict_elementos = {'Pt': 0.22, 'Pd': 0.43, 'Co': 0.35}  # Diccionario de nuevos elementos y sus probabilidades
atpos, eleList = leer_xyz(name) #lee el xyz

######################################################
#corta esféricamente
spherical_cut(atpos, 25, name)  # Realizar el corte esférico y escribir el nuevo archivo .xyz
new_atpos,new_eleList = cambiar_elementos_prob(atpos, dict_elementos)

##########################################################
#random removal at %
percent = 12
subprocess.run(['python','-u','randomremoval.py', name, str(percent)])


###############################################33
# escribe coords.ini
coord_lmp_out='lammps\coords'+str(ni)+'.ini'
wlammpin(new_atpos,new_eleList,coord_lmp_out)
# escribe nuevo shell con las nuevas coordenadas despues de dinamica molecular
name_out = 'ShellPd-'+str(ni)+'.xyz'
wXYZ(new_atpos,name_out)

##############################333
#ejecutar m9d.in con la variable de temperatura final t_relax en formato t_relax=500.0
t_relax=ni*100.0
# Copia el archivo para trabajar con la copia
shutil.copy('lammps/md9.in', 'lammps/md9-temp.in')
#modify_md9(t_relax)
modify_str_coords(ni) #lee el archivo coords.ini según el numero de prueba
modify_dump(ni) #sigue modificando md9, vuelca el archivo dump segun el numero de prueba
# Guarda el directorio de trabajo actual
dir_actual = os.getcwd()
# Cambia al directorio donde quieres ejecutar el comando
os.chdir('lammps')
# Ejecuta tu comando
subprocess.run(['lmp', '-in', 'md9-temp.in'])
os.remove('md9-temp.in')
# Vuelve al directorio de trabajo original
os.chdir(dir_actual)
##### funicionaba hasta aquí#######

################################## no es necesario
# quitar lineas del archivo dump
dump='lammps\dump'+ str(ni) +'-1.xyz'
#quitlines(dump)

##################################################
#cambiar etiquetas del archivo dump
dict_etiquetas = {1: 'Pt', 2: 'Pd', 3: 'Co'}  # Diccionario de etiquetas
cambiar_etiquetas_xyz(dump, dict_etiquetas, dump)

###########################################
#crea la pdf
pdfdump = dump
pdfdump.replace('lammps\\', '')
print(pdfdump)
comando = ['python', '-u', 'pdf.py', pdfdump]
subprocess.run(comando)

#######################################33

# mueve la pdf a la carpeta Graphics
archivo = 'dump-'+str(ni)+'-1-pdf.dat'
carpeta_origen = 'lammps'
carpeta_destino = 'graphics'
origen = os.path.join(carpeta_origen, archivo)
destino = os.path.join(carpeta_destino, archivo)
shutil.move(origen, destino)
