import subprocess
import sys
import os

def main():
    # Locate tools.py relative to this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    tools_path = os.path.abspath(os.path.join(current_dir, '..', 'utils', 'tools.py'))
    
    if not os.path.exists(tools_path):
        print(f"Error: tools.py not found at {tools_path}")
        return

    for ni in range(6,7):
        print(f"Running tools.py with argument {ni}")
        subprocess.run([sys.executable, '-u', tools_path, str(ni)])

if __name__ == "__main__":
    main()