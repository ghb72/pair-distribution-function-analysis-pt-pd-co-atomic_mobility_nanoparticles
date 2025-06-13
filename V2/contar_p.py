def contar_atomos(archivo):
    with open(archivo, 'r') as f:
        lines = f.readlines()[2:]  # Saltamos las dos primeras líneas

    atomos = {}
    total = 0

    for line in lines:
        tipo = line.split()[0]
        atomos[tipo] = atomos.get(tipo, 0) + 1
        total += 1

    proporciones = {tipo: count / total for tipo, count in atomos.items()}

    return atomos, proporciones

# Usamos la función en tu archivo .xyz
atomos, proporciones = contar_atomos('shellPd_22_c1_p.xyz')

print("Cantidad de átomos por tipo:", atomos)
print("Proporción de átomos por tipo:", proporciones)
