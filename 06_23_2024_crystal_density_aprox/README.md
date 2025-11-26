# Crystal Density Approximation (06_23_2024)

## Purpose

Theoretical study comparing atomic density ρ(r) with the pair distribution function G(r) for perfect crystals. This work provides fundamental understanding of the relationship between real-space density and the PDF.

## Theoretical Background

### Atomic Density ρ(r)
Number density of atoms as a function of radial distance from a central atom.

### Pair Distribution Function G(r)
Probability of finding an atom at distance r from a reference atom, normalized by bulk density:
```
G(r) = (1/4πr²ρ₀) * Σδ(r - r_ij)
```

### Relationship
For perfect crystals:
- ρ(r) shows shell structure
- G(r) emphasizes correlation over random distribution
- Peaks coincide but intensities differ

## Contents

### Main Script
- **`generar_cristal.py`**: Crystal structure generator
  - Creates simple cubic (SC), FCC, BCC, or HCP lattices
  - Calculates theoretical ρ(r) and G(r)
  - Generates comparison plots

## Crystal Structures

The script can generate:
1. **Simple Cubic (SC)**: Simplest lattice, 6-fold coordination
2. **FCC**: 12 nearest neighbors, close-packed
3. **BCC**: 8 nearest neighbors, less dense than FCC
4. **HCP**: 12 nearest neighbors, alternative close-packing

## Theoretical Predictions

For each structure, theoretical G(r) shows:
- **SC**: Peaks at a, a√2, a√3, 2a, ...
- **FCC**: Peaks at a/√2, a, a√(3/2), a√2, ...
- **BCC**: Peaks at a√3/2, a, a√2, a√(11/4), ...

## Usage

```bash
# Generate FCC crystal and calculate density/PDF
python generar_cristal.py

# Modify script for different lattice types
# Edit lattice parameter, crystal type, size
```

## Applications

This theoretical work:
1. Validates PDF calculation algorithms
2. Provides reference for perfect crystals
3. Highlights defect/disorder signatures (deviations from theory)
4. Guides interpretation of experimental PDFs

## Comparison to Simulations

Results here are compared to MD-simulated nanoparticles to identify:
- Surface effects (no bulk coordination)
- Strain (peak shifts)
- Disorder (peak broadening)
- Defects (missing/extra peaks)

## Mathematical Details

The code likely implements:
- Lattice point generation
- Radial binning of atomic pairs
- Normalization by ideal gas density
- Convolution with instrumental broadening (optional)

## Validation

Perfect crystal PDFs should exactly match crystallographic predictions, providing confidence in calculation methods before applying to complex nanoparticles.
