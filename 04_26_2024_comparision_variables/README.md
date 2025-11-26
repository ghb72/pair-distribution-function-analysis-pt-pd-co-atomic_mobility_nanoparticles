# Parameter Comparison Study (04_26_2024)

## Purpose

Systematic exploration of how different parameters affect nanoparticle structure and PDF:
- Temperature variations
- Composition ratios
- Particle size
- Relaxation time
- Potential parameters

## Directory Structure

### Main Subdirectory: `Probe_wM/`
Contains probes with method M (likely referring to a specific model or methodology):
- **`plot.py`**: Visualization script for results
- **`Probes_chi_square.ipynb`**: Statistical analysis using χ² goodness-of-fit tests

## Statistical Analysis

The χ² (chi-square) analysis compares:
- Simulated PDFs vs experimental data
- Different model parameters vs reference
- Sensitivity of PDF to parameter variations

## Key Variables Tested

Based on the directory name and context, likely parameters include:
1. **Temperature** (T): MD simulation temperature
2. **Composition** (x): Element ratios (e.g., Pt:Ni:Co)
3. **Size** (N): Number of atoms
4. **Relaxation protocol**: Equilibration strategy

## Workflow

1. Generate nanoparticle with specific parameters
2. Run MD simulation
3. Calculate PDF
4. Compare against reference/experimental data
5. Statistical analysis (χ² test)
6. Identify optimal parameter ranges

## Usage

```bash
# Navigate to probe directory
cd Probe_wM/

# Run statistical analysis
jupyter notebook Probes_chi_square.ipynb

# Generate plots
python plot.py
```

## Statistical Methods

The χ² test quantifies goodness of fit:
```
χ² = Σ[(O_i - E_i)² / E_i]
```
Where:
- O_i: Observed PDF values
- E_i: Expected/reference PDF values

Lower χ² values indicate better agreement.

## Output

- Comparison plots showing parameter sensitivity
- χ² values for each parameter set
- Optimal parameter recommendations

## Related Work

- Earlier parameter exploration: `05_17_2024_probes_w_last_model/`
- Temperature/vacuum effects: `05_31_2024_probes_w_temp_vac/`
