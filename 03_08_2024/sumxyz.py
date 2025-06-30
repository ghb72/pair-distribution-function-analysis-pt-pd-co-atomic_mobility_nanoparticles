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

def wXYZ(atpos,name_out):
        xyzfile = open(name_out,'w')
        n = len(atpos)
        xyzfile.write(str(n) +'\n\n')
        for ele,x,y,z in atpos:
                xyzfile.write('{0:2s}{1:12.5f}{2:12.5f}{3:12.5f}\n'.format(ele, x, y, z))
        xyzfile.close()


name1 = sys.argv[1]
name2 = sys.argv[2]

atpos1, eleList1 = leer_xyz(name1)
atpos2, eleList2 = leer_xyz(name2)

atpos = atpos1 + atpos2
wXYZ(atpos, 'CSPtNi.xyz')


    