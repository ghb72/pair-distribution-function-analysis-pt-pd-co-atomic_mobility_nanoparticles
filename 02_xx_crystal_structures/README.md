# Crystal Structures Analysis (02_xx_crystal_structures)

## Purpose

This directory contains early research work on analyzing different crystal structures of nanoparticles using pair distribution function (PDF) analysis. The focus is on understanding how different lattice arrangements (FCC, BCC, HCP, ICO) manifest in the radial distribution function.

## Contents

- **`rdf.f90`**: Fortran implementation of radial distribution function calculator
- **`lammps/`**: LAMMPS molecular dynamics input files and configurations
- **`shells/`**: Shell-by-shell analysis output files
- **`shells_original/`**: Original shell structures before MD relaxation
- **`graphics/`**: Generated plots and visualizations
- **`log.lammps`**: LAMMPS simulation log file

## Structure Types Studied

This work examines crystalline structures common in metal nanoparticles:
- **FCC (Face-Centered Cubic)**: Most stable for Pt, Ni, Au
- **BCC (Body-Centered Cubic)**: Common in Fe, Cr
- **HCP (Hexagonal Close-Packed)**: Observed in Co, Mg
- **ICO (Icosahedral)**: Dominant in small clusters

## Workflow

1. Generate initial crystal structures
2. Run LAMMPS molecular dynamics simulations for structural relaxation
3. Calculate RDF using `rdf.f90` (compile with `gfortran`)
4. Analyze shell-by-shell atomic distributions
5. Compare PDF signatures of different structures

## Usage

```bash
# Compile Fortran RDF calculator
gfortran -o rdf rdf.f90

# Run RDF calculation
./rdf <structure>.xyz
```

## Related Work

This early crystal structure work informed later studies on:
- Core-shell configurations
- Janus particles
- Radial atomic distributions

See notebooks in `notebooks/crystal_structures/` for comparative analysis.
