import matplotlib.pyplot as plt
from sys import argv
from collections import defaultdict
import numpy as np

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


def graficar_atomos_por_radio(nombre_archivo, elemento_interes):
    atpos, eleList = leer_xyz(nombre_archivo)
    radios = defaultdict(int)
    rad_tot = defaultdict(int)
    for atomo in atpos:
        r = np.sqrt(atomo[1]**2 + atomo[2]**2 + atomo[3]**2)
        rad_tot[r] += 1
        if atomo[0] == elemento_interes:
            radios[r] += 1
        else: radios[r] += 0
    rad_tot_o = sorted(rad_tot.items())
    radios_ordenados = sorted(radios.items())
    rad_tot, conteo_tot = zip(*rad_tot_o)
    radios, conteo = zip(*radios_ordenados)
    return rad_tot, conteo_tot, radios, conteo


def graficar_proporcion_atomos_por_radio(nombre_archivo, elemento_interes):
    atpos, eleList = leer_xyz(nombre_archivo)
    conteo_atomos = defaultdict(int)
    conteo_total = defaultdict(int)
    radios = []
    for atomo in atpos:
        conteo_total[np.sqrt(atomo[1]**2+atomo[2]**2+atomo[3]**2)] += 1
        if atomo[0] == elemento_interes:
            conteo_atomos[np.sqrt(atomo[1]**2+atomo[2]**2+atomo[3]**2)] += 1
    radios_ordenados = sorted(conteo_total.items())
    radios, conteo_total = zip(*radios_ordenados)
    proporciones = [conteo_atomos[radio] / total for radio, total in zip(radios, conteo_total)]
    return radios, proporciones


name = argv[1]
elemento_interes='Ni'
rad_tot, conteo_tot, radios, conteo=graficar_atomos_por_radio(name,elemento_interes)
rads, proporciones = graficar_proporcion_atomos_por_radio(name, elemento_interes)


fig, ax =plt.subplots(2,1,figsize=(10,5), layout='constrained')
ax[0].plot(rad_tot, conteo_tot, label=('Total'), color = 'black')
ax[0].plot(radios, conteo, label=('Átomos de ' + elemento_interes), color='red')
ax[0].set_xlabel('Radio [$\\AA$]')
ax[0].set_xlim([0,16])
ax[0].set_ylabel('Átomos por capa')
#ax[0].set_title('Cantidad de Átomos de ' + elemento_interes + ' por Radio')
ax[0].legend()

ax[1].plot(rads, proporciones, color='black')
ax[1].set_xlabel('Radio[$\\AA$]')
ax[1].set_ylabel('Fracción de Átomos de '+ elemento_interes)

fig.suptitle('Fracción y Átomos por radio')
plt.show()
