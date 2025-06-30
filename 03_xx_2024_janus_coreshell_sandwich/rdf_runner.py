#import sys
import os
import subprocess
#import shutil
from os import scandir, getcwd

def file_list(path=getcwd()):
    return [arch.name for arch in scandir(path) if arch.is_file()]

def run_pdf(name,path):
    new_filename=path+'\\'+name
    new_nhis=1550
    with open('rdf1.f90', 'r') as f:
        lines = f.readlines()
    with open('temp_rdf.f90', 'w') as f:
        for line in lines:
            if "file='shell.xyz'" in line:
                line = line.replace("file='shell.xyz'", f"file='{new_filename}'")
            if "nhis=2600" in line:
                line = line.replace("nhis=2600", f"nhis={new_nhis}")
            if "file='rdf.txt'" in line:
                line = line.replace("file='rdf.txt'", f"file='{'graphics/'+name[:-4]+'.txt'}'")
            f.write(line)
    subprocess.run(['gfortran','temp_rdf.f90', '-o', 'rdf'])
    subprocess.run(['./rdf.exe'])
    os.remove('temp_rdf.f90')
    os.remove('rdf.exe')

def proccess_all_files_in_folder(folder):
    f_list = file_list(folder)
    for file in f_list:
        print(file)
        run_pdf(file,folder)
        print('\n')

#proccess_all_files_in_folder('shells_original')
#run_pdf('shellPt-FCCv2.xyz','shells_original')
run_pdf('shellPt-BCC.xyz','shells_original')
run_pdf('shellPt-ico.xyz','shells_original')
#shutil.move(new_filename[:-4]+'.txt', 'graphics\\'+new_filename[:-4]+'.txt')