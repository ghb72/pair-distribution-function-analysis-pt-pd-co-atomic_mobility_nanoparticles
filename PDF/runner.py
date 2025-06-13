#import sys
import os
import subprocess
from os import scandir, getcwd

def file_list(path=getcwd()) -> list:
    """
    Devuelve una lista con los nombres de todos los archivos en el directorio especificado.

    Parámetros:
    path (str): Ruta del directorio donde buscar archivos. Por defecto, se utiliza el directorio de trabajo actual.

    Retorno:
    list: Lista de nombres de archivos en el directorio especificado.
    """
    return [arch.name for arch in scandir(path) if arch.is_file()]


def getpath() -> None:
    """
    Imprime la ruta del directorio de trabajo actual.

    Parámetros:
    Ninguno.

    Retorno:
    Ninguno.
    """
    print(os.getcwd())


def run_pdf(name: str, path: str, nhis: int, dr: float) -> None:
    """
    Modifica un archivo Fortran, compila y ejecuta el archivo modificado.

    Parámetros:
    name (str): Nombre del archivo que se va a procesar.
    path (str): Ruta donde se encuentra el archivo.
    nhis (int): Número de histogramas a utilizar.
    dr (float): Incremento de distancia radial.

    Retorno:
    Ninguno. La función imprime la salida de los comandos de compilación y ejecución.
    """
    new_filename = path + '\\' + name
    print(os.getcwd())
    with open('..\\..\\PDF\\rdf.f90', 'r') as f:  # rdf.f90 for dump and rdf1.f90 for shell (no MD)
        lines = f.readlines()
    with open('temp_rdf.f90', 'w') as f:
        for line in lines:
            if "file='shell.xyz'" in line:
                line = line.replace("file='shell.xyz'", f"file='{new_filename}'")
            if "nhis=2600" in line:
                line = line.replace("nhis=2600", f"nhis={nhis}")
            if "file='rdf.txt'" in line:
                line = line.replace("file='rdf.txt'", f"file='{name[:-4] + '.txt'}'")
            if "delr = 0.02" in line:
                line = line.replace("delr = 0.02", f"delr = {dr}")
            f.write(line)
    resultado = subprocess.run(['gfortran', 'temp_rdf.f90', '-o', 'rdf'], capture_output=True)
    print(resultado.stdout.decode())
    resultado2 = subprocess.run(['./rdf.exe'], capture_output=True)
    print(resultado2.stdout.decode())
    # os.remove('temp_rdf.f90')
    # os.remove('rdf.exe')

def run_pdf_noMD(name: str, path: str, nhis: int, dr: float, smooth1: float, smooth2: float) -> None:
    """
    Modifica un archivo Fortran, compila y ejecuta el archivo modificado con parámetros específicos para el suavizado.

    Parámetros:
    name (str): Nombre del archivo que se va a procesar.
    path (str): Ruta donde se encuentra el archivo.
    nhis (int): Número de histogramas a utilizar.
    dr (float): Incremento de distancia radial.
    smooth1 (float): Primer parámetro de suavizado.
    smooth2 (float): Segundo parámetro de suavizado.

    Retorno:
    Ninguno. La función imprime la salida de los comandos de compilación y ejecución.
    """
    new_filename = path + '\\' + name
    print(os.getcwd())
    with open('..\\..\\PDF\\rdf_noMD.f90', 'r') as f:  # rdf.f90 for dump and rdf1.f90 for shell (no MD)
        lines = f.readlines()
    with open('temp_rdf.f90', 'w') as f:
        for line in lines:
            if "file='shell.xyz'" in line:
                line = line.replace("file='shell.xyz'", f"file='{new_filename}'")
            if "nhis=2600" in line:
                line = line.replace("nhis=2600", f"nhis={nhis}")
            if 'call smooth(hs1,5,hs2)' in line:
                line = line.replace('call smooth(hs1,5,hs2)', f'call smooth(hs1,{smooth1},hs2)')
            if 'call smooth(hs2,5,hs1)' in line:
                line = line.replace('call smooth(hs2,5,hs1)', f'call smooth(hs2,{smooth2},hs1)')
            if "file='rdf.txt'" in line:
                line = line.replace("file='rdf.txt'", f"file='{name[:-4] + '.txt'}'")
            if "delr = 0.02" in line:
                line = line.replace("delr = 0.02", f"delr = {dr}")
            f.write(line)
    resultado = subprocess.run(['gfortran', 'temp_rdf.f90', '-o', 'rdf'], capture_output=True)
    print(resultado.stdout.decode())
    resultado2 = subprocess.run(['./rdf.exe'], capture_output=True)
    print(resultado2.stdout.decode())
    # os.remove('temp_rdf.f90')
    # os.remove('rdf.exe')

def proccess_all_files_in_folder(folder:str) -> None:
    """
    Procesa todos los archivos en una carpeta especificada utilizando la función `run_pdf`.

    Parámetros:
    folder (str): Ruta de la carpeta que contiene los archivos a procesar.

    Retorno:
    Ninguno. La función imprime los nombres de los archivos procesados.
    """
    f_list = file_list(folder)
    for file in f_list:
        print(file)
        run_pdf(file, folder)
        print('\n')


def filter_xyz(input_filename:str, output_filename:str, elements:list) -> None:
    """
    Filtra un archivo .xyz eliminando las líneas que no contienen elementos específicos y guarda el resultado en un archivo temporal.

    Parámetros:
    input_filename (str): Nombre del archivo de entrada .xyz.
    output_filename (str): Nombre del archivo de salida filtrado.
    elements (list): Lista de elementos a mantener en el archivo filtrado.

    Retorno:
    Ninguno. La función guarda el archivo filtrado con los elementos especificados.
    """
    # Leer el archivo de entrada
    with open(input_filename, 'r') as infile:
        lines = infile.readlines()
    
    # La cabecera contiene el número de átomos
    header = lines[:2]
    atom_lines = lines[2:]
    
    # Filtrar líneas según los elementos deseados
    filtered_lines = [line for line in atom_lines if line.split()[0] in elements]
    
    # Actualizar el conteo de átomos en la cabecera
    header[0] = str(len(filtered_lines)) + '\n'
    
    # Escribir el archivo temporal con solo los elementos deseados
    with open(output_filename, 'w') as outfile:
        outfile.writelines(header + filtered_lines)
    print(f"El archivo temporal {output_filename} ha sido creado con los elementos deseados {elements}.")

