import subprocess

for ni in range(6,7):
    subprocess.run(['python', '-u', 'tools.py', str(ni)])