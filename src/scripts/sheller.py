import numpy as np

def read_xyz_file(file_path):
    """
    Lee un archivo .xyz y devuelve las coordenadas de los átomos.
    """
    atoms = []
    with open(file_path, 'r') as xyz_file:
        lines = xyz_file.readlines()[2:]  # Saltamos las primeras dos líneas
        for line in lines:
            symbol, x, y, z = line.split()
            atoms.append((symbol, float(x), float(y), float(z)))
    return atoms

def distance(atom1, atom2):
    """
    Calcula la distancia entre dos átomos en 3D.
    """
    return np.linalg.norm(np.array(atom1[1:]) - np.array(atom2[1:]))

def change_atoms_within_radii(atoms, r1, r2, new_element='Ni'):
    """
    Cambia los átomos dentro de los radios r1 y r2 al nuevo elemento.
    """
    changed_atoms = []
    for i, atom1 in enumerate(atoms):
        for j, atom2 in enumerate(atoms):
            if i != j:  # Evitamos comparar un átomo consigo mismo
                dist = distance(atom1, atom2)
                if r1 <= dist <= r2:
                    changed_atoms.append((atom1[0], new_element, *atom1[1:]))
                else:
                    changed_atoms.append(atom1)
    return changed_atoms

if __name__ == "__main__":
    xyz_file_path = "shells\\shellPt-FCC-cs1.xyz"
    r1 = 6.0  # Radio mínimo
    r2 = 16.0  # Radio máximo

    atoms = read_xyz_file(xyz_file_path)
    new_atoms = change_atoms_within_radii(atoms, r1, r2, new_element='Ni')

    # Guardamos los nuevos átomos en un nuevo archivo .xyz
    with open("shells\\shell-FCC-cs1.xyz", 'w') as new_xyz_file:
        new_xyz_file.write(f"{len(new_atoms)}\n\n")
        for atom in new_atoms:
            new_xyz_file.write(f"{atom[0]} {atom[1]:.6f} {atom[2]:.6f} {atom[3]:.6f}\n")

    print(f"Se han cambiado los átomos dentro de los radios {r1} y {r2} a '{new_element}'.")
