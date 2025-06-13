import subprocess

for ni in range(20,36,2):
    subprocess.run(['python', '-u', 'tools.py', str(ni)])