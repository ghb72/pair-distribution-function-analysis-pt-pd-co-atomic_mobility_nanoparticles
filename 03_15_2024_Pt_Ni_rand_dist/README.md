# Pt-Ni Random Distribution Analysis (03_15_2024)

## Purpose

Investigation of random atomic distributions in Pt-Ni bimetallic nanoparticles. This work explores how different mixing ratios and distribution patterns affect the pair distribution function.

## Directory Structure

### Comparative Analysis
- **`comparision_NiPt.ipynb`**: Main comparison notebook for Pt-Ni systems
- **`comparision_NiPt copy.ipynb`**: Backup/alternative version

### Pure Systems (References)
- **`Ni_100/`**: Pure Ni nanoparticle (100% Ni)
- **`Pt_100/`**: Pure Pt nanoparticle (100% Pt)

### Random Distributions
- **`Pt_25_rand/`**: 25% Pt randomly distributed in Ni matrix
- **`Pt_50_rand/`**: 50% Pt-50% Ni random alloy
- **`Pt_75_rand/`**: 75% Pt with 25% Ni randomly distributed

### Radial Random Distributions
- **`Pt_25_radrand/`**: 25% Pt with radially-weighted random distribution
- **`Pt_50_radrand/`**: 50% Pt with radially-weighted distribution
- **`Pt_75_radrand/`**: 75% Pt with radially-weighted distribution

### Crystal Generation
- **`Crystal/`**: Scripts for generating FCC crystal structures

## Key Findings

The radial distribution strategies show different PDF patterns compared to uniform random mixing, particularly in the first coordination shell peaks. This work demonstrated the importance of atomic arrangement patterns beyond just composition.

## Data Files

Each subdirectory typically contains:
- `.xyz` files: Atomic coordinate files
- `.ini` files: LAMMPS initial configuration
- `.txt` files: RDF/PDF calculation results
- `.jpg`/`.png` files: Visualization outputs

## Methods

1. **Random Distribution**: Atoms assigned randomly with specified composition ratio
2. **Radial Random Distribution**: Probability of Pt vs Ni varies with distance from nanoparticle center

## Usage

Run notebooks in Jupyter:
```bash
jupyter notebook comparision_NiPt.ipynb
```

## Related Directories

- `04_19_2024_radial_distributions/`: Extended radial distribution models
- `04_26_2024_comparision_variables/`: Parameter sensitivity analysis
