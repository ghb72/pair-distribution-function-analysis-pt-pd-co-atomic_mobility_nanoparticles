# Janus, Core-Shell, and Sandwich Structures (03_xx_2024)

## Purpose

Comprehensive study of three distinct atomic arrangement strategies in bimetallic nanoparticles:
- **Core-Shell**: One element forms a spherical shell around a core of another element
- **Janus**: Hemispheric separation of two elements
- **Sandwich**: Layered structures along one axis

This directory contains the scripts and data for generating these structures and analyzing their PDFs.

## Key Scripts

### Structure Generation
- **`sandwichmachine.py`**: Generate Janus, sandwich, and core-shell structures
  - Usage: `python sandwichmachine.py <input.xyz> <mode> <param1> <param2>`
  - Modes: `janus`, `sandwich`, `cs` (core-shell), `radcut`, `makesmall`
- **`core-shell-o.py`**: Ordered core-shell structure generator
- **`core-shell-u.py`**: Unordered/uniform core-shell generator
- **`sheller.py`**: Shell analysis tool

### Analysis Tools
- **`tools.py`**: Utility functions for XYZ file manipulation
- **`lammpin1.py`**: LAMMPS input file generator
- **`pdf.py`**: PDF calculation wrapper
- **`rdf_runner.py`**: Automated RDF calculation runner
- **`compare.py`** / **`cmp.py`**: PDF comparison tools

### Utilities
- **`runner.py`**: Batch processing script
- **`checklines.py`**: File integrity checker
- **`count_at.py`**: Atom counter by element
- **`sumxyz.py`**: XYZ file combiner
- **`randomremoval.py`**: Random atom removal tool

## Typical Workflow

1. **Generate base structure** (FCC nanoparticle)
2. **Create desired arrangement**:
   ```bash
   # Core-shell: 50% Ni core, 50% Pt shell
   python sandwichmachine.py Ni-FCC.xyz cs 0 8.5
   
   # Janus: hemispherical division
   python sandwichmachine.py Pt-FCC.xyz janus 0 0
   
   # Sandwich: layers between z1 and z2
   python sandwichmachine.py Ni-FCC.xyz sandwich -1.13 1.13
   ```
3. **Run LAMMPS simulation** for structural relaxation
4. **Calculate RDF/PDF**:
   ```bash
   python rdf_runner.py
   ```
5. **Compare results**:
   ```bash
   python compare.py structure1.txt structure2.txt
   ```

## Directory Organization

Files are typically organized by structure type and composition percentage:
- `Ni-cs-50.xyz`: Ni nanoparticle with 50% core-shell structure
- `Pt-janus-75.xyz`: Pt nanoparticle with 75% Janus configuration
- `Ni-sandwich-60.xyz`: Ni with 60% sandwich arrangement

## Important Notes

- Scripts assume FCC starting structures
- Coordinate files use Angstrom units
- LAMMPS files require MEAM potentials (see `data/lammps_resources/`)

## See Also

- Main notebooks: `notebooks/comparision/` for visual comparisons
- Modernized scripts: `src/scripts/` (updated versions)
- Results: `results/shells_latest/`, `results/graphics_latest/`
