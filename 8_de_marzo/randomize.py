import random as ran
import numpy as np
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

def cambiar_elementos_prob(atpos, dict_elementos):
    print(f'Cambia elementos prob a {name}')
    new_atpos = []
    new_eleList = []
    for atom in atpos:
        nuevo_elemento = ran.choices(list(dict_elementos.keys()), weights=list(dict_elementos.values()), k=1)[0]
        if ran.random() < 100*dict_elementos[nuevo_elemento]:
            new_atpos.append([nuevo_elemento, atom[1], atom[2], atom[3]])
            if nuevo_elemento not in new_eleList:
                new_eleList.append(nuevo_elemento)
        else:
            new_atpos.append(atom)
            if atom[0] not in new_eleList:
                new_eleList.append(atom[0])
    return new_atpos, new_eleList, 'rand'

def eliminar_at(atpos,percent):
    print(f'Elimina aleatoriament el {percent}% de {name}')
    new_atpos = []
    for atom in atpos:
        if ran.random() < percent:
            new_atpos.append(atom)
    return new_atpos

def pow_rad_ch(atpos,eleList,percentes,Diam):
    maxrad = Diam/2
    print(f'Cambia en potencia el porcentaje radial de átomos en {percentes}')
    new_atpos=[]
    per = percentes[eleList[0]]
    p = (1/per)-1
    new_element=('Pt' if eleList[0]=='Ni' else 'Ni')
    for atom in atpos:
        r = np.sqrt(atom[1]**2+atom[2]**2+atom[3]**2)
        x = pow(r/maxrad,3)
        y = pow(x,p)
        #print(y,x,2*p)
        if ran.random() >= y:
            new_atpos.append([new_element,atom[1],atom[2],atom[3]])
            if new_element not in eleList:
                eleList.append(new_element)
        else:
            new_atpos.append(atom)
    return new_atpos,eleList,'pow'

def root_rad_ch(atpos,eleList,percentes,Diam):
    maxrad = Diam/2
    print(f'Cambia en potencia el porcentaje radial de átomos en {percentes}')
    new_atpos=[]
    maxi = max(percentes)
    print(maxi)
    per = percentes[maxi]
    p = (1/per)-1
    new_element=('Pt' if eleList[0]=='Ni' else 'Ni')
    for atom in atpos:
        r = np.sqrt(atom[1]**2+atom[2]**2+atom[3]**2)
        x = pow(r/maxrad,3)
        y = pow(x,1/p)
        #print(y,x,2*p)
        if ran.random() >= y:
            new_atpos.append([new_element,atom[1],atom[2],atom[3]])
            if new_element not in eleList:
                eleList.append(new_element)
        else:
            new_atpos.append(atom)
    return new_atpos,eleList,'root'

def hyper_rad_ch(atpos,eleList,percentes,Diam):
    maxrad = Diam/2
    print(f'Cambia hipergeometricamente el porcentaje radial de átomos en {percentes}')
    new_atpos=[]
    per = percentes[mayoria]
    new_element='Pt'
    for atom in atpos:
        r = np.sqrt(atom[1]**2+atom[2]**2+atom[3]**2)
        A = 2*(r/maxrad)**2
        if ran.random() <= A*2*r:
            new_atpos.append([new_element,atom[1],atom[2],atom[3]])
            if new_element not in eleList:
                eleList.append(new_element)
        else:
            new_atpos.append(atom)
    return new_atpos,eleList,'hyp'

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


def wXYZ(atpos,name_out):

        xyzfile = open(name_out,'w')
        n = len(atpos)
        xyzfile.write(str(n) +'\n\n')
        for ele,x,y,z in atpos:
                xyzfile.write('{0:2s}{1:12.5f}{2:12.5f}{3:12.5f}\n'.format(ele, x, y, z))
        xyzfile.close()


# Usamos la función con el archivo 'dump-5.xyz' y un porcentaje del 10%
name='Pt-FCC.xyz'
percentes = {'Pt':0.25,'Ni':0.75}
mayoria = ('Ni' if percentes['Ni']>percentes['Pt'] else 'Pt')
atpos,eleList=leer_xyz(name)

#atpos,eleList,mode = root_rad_ch(atpos,eleList,percentes,30.1)
atpos, eleList, mode = cambiar_elementos_prob(atpos,percentes)
percent(atpos,eleList)

print(mode)
yes = input("It's ok the model? [Y/N]:\n")
if yes =='N' or yes =='n':
    print('ok')
    pass
elif yes =='Y' or yes =='y':
    name = f'{mayoria}-{percentes[mayoria]}-rad{mode}.xyz'
    print(name)
    wXYZ(atpos,name)
else:
    print('Incorrect response')



