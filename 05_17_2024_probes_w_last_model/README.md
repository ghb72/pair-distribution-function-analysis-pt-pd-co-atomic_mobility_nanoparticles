# Probes with Final Model (05_17_2024)

## Purpose

Testing and validation of the finalized nanoparticle model. This directory contains probe calculations using the optimized parameters and methodologies developed from earlier experiments.

## Context

After systematic parameter studies (04_26_2024) and radial distribution exploration (04_19_2024), this work applies the best-performing model to generate production-quality PDFs.

## Structure

### Probe Directories (p1/, p2/, p3/, ...)
Each probe directory represents:
- Different initial conditions
- Statistical replicates
- Variation tests
- Specific compositions or sizes

### LAMMPS Configuration
- **`M0-polrad_1.ini`**: LAMMPS input file for base configuration

## Purpose of Probes

Probes serve to:
1. **Validate model consistency**: Multiple runs should give similar PDFs
2. **Statistical analysis**: Ensemble averaging
3. **Error estimation**: Standard deviations across probes
4. **Reproducibility**: Confirm results are not artifacts

## Typical Probe Content

Each `p#/` directory likely contains:
- `.xyz` files: Atomic structures at different stages
- `.txt` files: RDF/PDF data
- `.ini` files: LAMMPS configurations
- Log files from simulations

## Workflow

1. Setup probe with specific initial configuration
2. Run LAMMPS MD simulation
3. Extract relaxed structure
4. Calculate PDF
5. Statistical aggregation across all probes

## Analysis

Results from multiple probes are:
- Averaged to reduce statistical noise
- Analyzed for variance
- Compared to ensure reproducibility

## Usage

```bash
# Run specific probe
cd p1/
# (Run LAMMPS and analysis)

# Compare all probes
# (Use comparison scripts from main src/)
```

## Model Validation

This work validates that the final model:
- Produces consistent results
- Matches experimental expectations
- Has acceptable statistical variance
- Is reproducible

## Next Steps

See `05_31_2024_probes_w_temp_vac/` for temperature and vacuum condition variations.
