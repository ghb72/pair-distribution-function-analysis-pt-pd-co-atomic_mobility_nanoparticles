import numpy as np
import math

# --- Parámetros de la simulación ---

ELEMENTO = 'Pt'
# Parámetro de red para el Níquel (FCC) en Angstroms
LADO_CELDA = 3.93
# Número de átomos deseado
ATOMOS_OBJETIVO = 27000
# Desplazamiento aleatorio máximo desde la posición ideal en Angstroms
MAX_DESPLAZAMIENTO = 0.5
# Nombre del archivo de salida
ARCHIVO_SALIDA = 'shell.xyz'


def generar_cristal_fcc():
    """
    Genera una estructura cristalina FCC de Níquel, centrada en el origen,
    con desplazamientos aleatorios y la guarda en un archivo .xyz.
    """
    print("Iniciando la generación del cristal de Níquel (FCC)...")

    # 1. Calcular el tamaño de la supercelda
    # La celda unitaria FCC tiene 4 átomos.
    atomos_por_celda = 4
    celdas_necesarias = ATOMOS_OBJETIVO / atomos_por_celda
    # Calculamos la dimensión de la red de celdas (n x n x n)
    # Usamos la raíz cúbica y redondeamos hacia arriba para asegurar el número de átomos
    dim_red = math.ceil(celdas_necesarias**(1/3))
    
    print(f"Se usará una red de {dim_red}x{dim_red}x{dim_red} celdas unitarias.")

    # 2. Generar las posiciones ideales de los átomos
    # Posiciones de la base FCC en coordenadas fraccionales (relativas a la celda)
    base_fcc = np.array([
        [0.0, 0.0, 0.0],
        [0.5, 0.5, 0.0],
        [0.5, 0.0, 0.5],
        [0.0, 0.5, 0.5]
    ])

    posiciones = []
    # Iteramos sobre cada celda unitaria en nuestra red
    for i in range(dim_red):
        for j in range(dim_red):
            for k in range(dim_red):
                # Origen de la celda unitaria actual
                origen_celda = np.array([i, j, k]) * LADO_CELDA
                # Colocamos los 4 átomos de la base en esta celda
                for pos_base in base_fcc:
                    pos_atom = origen_celda + pos_base * LADO_CELDA
                    posiciones.append(pos_atom)

    posiciones = np.array(posiciones)
    num_atomos_real = len(posiciones)
    print(f"Se han generado {num_atomos_real} posiciones de átomos ideales.")

    # 3. Centrar la estructura en el origen (0,0,0)
    centro_de_masa = np.mean(posiciones, axis=0)
    posiciones_centradas = posiciones - centro_de_masa
    print("La estructura ha sido centrada en el origen.")

    # 4. Añadir desplazamientos aleatorios
    posiciones_finales = []
    for pos in posiciones_centradas:
        # Generamos un vector de desplazamiento aleatorio dentro de una esfera
        # de radio MAX_DESPLAZAMIENTO para que la magnitud sea correcta.
        while True:
            # Generar un punto aleatorio en un cubo
            dx, dy, dz = np.random.uniform(-MAX_DESPLAZAMIENTO, MAX_DESPLAZAMIENTO, 3)
            # Comprobar si está dentro de la esfera
            if np.sqrt(dx**2 + dy**2 + dz**2) < MAX_DESPLAZAMIENTO:
                desplazamiento = np.array([dx, dy, dz])
                break # Si está dentro, es válido
        
        posiciones_finales.append(pos + desplazamiento)
        
    print("Se han añadido desplazamientos aleatorios a cada átomo.")

    # 5. Escribir el archivo de salida en formato .xyz
    with open(ARCHIVO_SALIDA, 'w') as f:
        # Escribir el número total de átomos
        f.write(f"{num_atomos_real}\n")
        # Escribir una línea de comentario (requerido por el formato)
        f.write(f"Cristal de Niquel (FCC) de {num_atomos_real} atomos, centrado y con vibraciones.\n")
        
        # Escribir las coordenadas de cada átomo
        for pos in posiciones_finales:
            f.write(f"{ELEMENTO:<2s} {pos[0]:12.6f} {pos[1]:12.6f} {pos[2]:12.6f}\n")

    print(f"\n¡Éxito! Se ha creado el archivo '{ARCHIVO_SALIDA}' con {num_atomos_real} átomos.")


# --- Ejecutar el programa ---
if __name__ == "__main__":
    generar_cristal_fcc()