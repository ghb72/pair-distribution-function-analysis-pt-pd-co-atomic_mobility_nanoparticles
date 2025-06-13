import os
import subprocess
import shutil

input_file='rdf.f90'
output_file='temp_rdf.f90'
new_filename='shellPd_20.xyz'
new_nhis=1000
with open(input_file, 'r') as f:
    lines = f.readlines()

with open(output_file, 'w') as f:
    for line in lines:
        if "file='shell.xyz'" in line:
            line = line.replace("file='shell.xyz'", f"file='{new_filename}'")
        if "nhis=2600" in line:
            line = line.replace("nhis=2600", f"nhis={new_nhis}")
            if "file='rdf.txt'" in line:
                line = line.replace("file='rdf.txt'", f"file='{new_filename[:-4]+'.txt'}'")
        f.write(line)

#subprocess.run(['gfortran','temp_rdf.f90', '-o', 'rdf'])
#subprocess.run(['.\\rdf'])

#os.remove('temp_rdf.f90')
#shutil.move(new_filename[:-4]+'.txt', 'graphics\\'+new_filename[:-4]+'.txt')