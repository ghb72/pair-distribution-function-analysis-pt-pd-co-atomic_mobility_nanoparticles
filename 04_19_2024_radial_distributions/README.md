# Radial Distribution Models (04_19_2024)

## Purpose

Systematic exploration of radial atomic distribution patterns in Pt-Pd-Co ternary nanoparticles. This work investigates how different radial concentration profiles affect the pair distribution function.

## Models (M0-M8)

Each model (M0 through M8) represents a different radial distribution strategy:

- **M0**: Base model or reference structure
- **M1-M8**: Variations in radial concentration profiles
  - Polynomial distributions: P(r) ∝ r^n
  - Root distributions: P(r) ∝ √r
  - Exponential distributions
  - Step functions

Each model directory contains:
- `.xyz` files: Atomic coordinates
- `.ini` files: LAMMPS configurations
- `.txt` files: RDF calculation results
- `.jpg`/`.png` files: Visualization plots
- `.ipynb` files: Analysis notebooks (if present)

## Special Distributions

- **`randrad1_co/`**: Random radial distribution for cobalt

## Comparative Analysis

- **`comparision.ipynb`**: Main comparison of all models
- **`comparision_cartelplots.ipynb`**: Grid comparison plots for presentations

## Key Findings

The shape of the radial concentration profile significantly affects:
- First neighbor peak intensities in G(r)
- Medium-range ordering
- Surface vs bulk atomic environment signatures

Polynomial and root functions provided smoother transitions compared to step functions, better matching experimental observations.

## Workflow

1. Generate radial distribution profile function
2. Apply distribution to base nanoparticle structure
3. Run MD simulation for equilibration
4. Calculate PDF
5. Compare against other models

## Usage

```bash
# Navigate to specific model
cd M1/

# Run analysis notebook
jupyter notebook <model_analysis>.ipynb

# Or compare all models
cd ..
jupyter notebook comparision.ipynb
```

## Mathematical Background

Radial distributions tested:
- **Linear**: P(r) = ar + b
- **Quadratic**: P(r) = ar² + br + c
- **Power**: P(r) = r^n
- **Root**: P(r) = r^(1/n)
- **Gaussian**: P(r) = exp(-(r-μ)²/2σ²)

## Related Work

- Previous: `03_15_2024_Pt_Ni_rand_dist/` (binary systems)
- Next: `04_26_2024_comparision_variables/` (parameter sensitivity)
