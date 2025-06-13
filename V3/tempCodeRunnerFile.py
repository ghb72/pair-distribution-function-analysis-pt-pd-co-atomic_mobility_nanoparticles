dump='lammps\dump'+ str(ni) +'-1.xyz'
quitlines(dump)

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
archivo = 'dump-'+str(ni)+'-pdf.dat'
carpeta_origen = 'lammps'
carpeta_destino = 'graphics'
origen = os.path.join(carpeta_origen, archivo)
destino = os.path.join(carpeta_destino, archivo)
shutil.move(origen, destino)
