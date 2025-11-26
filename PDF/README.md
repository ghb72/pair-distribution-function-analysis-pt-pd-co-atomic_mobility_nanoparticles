# PDF Calculation Tools (PDF/)

## Purpose

Legacy directory containing Python implementations of pair distribution function (PDF) calculations. These scripts were used before migrating to Fortran implementations for better performance.

## Contents

### Main Scripts
- **`RDF.py`**: Python implementation of radial distribution function
- **`pdf.py`**: PDF calculation wrapper
- **`runner.py`**: Batch processing for multiple files

## Performance Note

**⚠️ For production work, use Fortran implementation:**
- Located in: `src/fortran/rdf.f90`
- Compile with: `gfortran -o rdf rdf.f90`
- 10-100x faster than Python version

Python version useful for:
- Debugging
- Small test calculations
- Understanding algorithm
- Prototyping modifications

## Usage

```bash
# Run Python RDF calculation
python RDF.py <structure>.xyz

# Batch process directory
python runner.py
```

## Algorithm

The RDF/PDF calculation:
1. Read atomic coordinates from XYZ file
2. Calculate all pairwise distances
3. Bin distances into histogram
4. Normalize by:
   - Number of atoms
   - Bin volume (4πr²Δr)
   - Bulk density
5. Output G(r) vs r

## Dependencies

- NumPy: Array operations
- Pandas: Data handling
- tools_f: XYZ file reading (from `src/my_functions/`)

## Migration

Modern, maintained versions in:
- `src/scripts/pdf.py`: Updated Python version
- `src/fortran/rdf.f90`: High-performance Fortran
- `src/scripts/rdf_runner.py`: Automated runner

## See Also

- Fortran version: `src/fortran/`
- Analysis notebooks: `notebooks/`
