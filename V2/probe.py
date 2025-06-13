import numpy as np
import pandas as pd
import sys

# Leer los archivos .csv y .dat
name = sys.argv[1] #"graphics\\dump_Pd_22_p_10_600_l.dat"
df_exp = pd.read_csv("graphics\\Post-PtPdCo_PDF.csv", sep=",", header=None, names=["x", "y_exp"])
df_mod = pd.read_table(name, sep="\\s+", skiprows=1, usecols=[0, 3], names=["x", "y_mod"])

# Hace la resta de cuadrados
df = df_exp["y_exp"] - df_mod["y_mod"]
ssr = np.sum(df**2)

# Imprimir el resultado
print('Para el archivo', name)
print(f"La suma de los cuadrados de los residuos es: {ssr:.4f}")
