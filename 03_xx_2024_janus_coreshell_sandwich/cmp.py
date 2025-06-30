import numpy as np
import pandas as pd
import sys

# Leer los nombres de los archivos .txt
name1 = sys.argv[1]
name2 = sys.argv[2]

# Leer los archivos .txt
df_exp = pd.read_csv(name1, sep="\\s+", skiprows=1, names=["x", "y_exp"])
df_mod = pd.read_csv(name2, sep="\\s+", skiprows=1, names=["x", "y_mod"])

# Hace la resta de cuadrados
df = pd.to_numeric(df_exp["y_exp"], errors='coerce') - pd.to_numeric(df_mod["y_mod"], errors='coerce')
ssr = np.sum(df**2)

# Imprimir el resultado
print('Para los archivos', name1, 'y', name2)
print(f"La suma de los cuadrados de los residuos es: {ssr:.4f}")