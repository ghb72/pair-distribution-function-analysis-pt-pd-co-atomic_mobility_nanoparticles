import pandas as pd
import matplotlib.pyplot as plt
plt.close('all')

df_cs50 = pd.read_csv('graphics\\Ni-cs-50b.txt', sep='\s+')
df_cs60 = pd.read_csv('graphics\\Ni-cs-60b.txt', sep='\s+')
df_ni = pd.read_csv('graphics\\Ni-FCCb.txt', sep='\s+')

fig, ax = plt.subplots(figsize=(10,5), layout='constrained')
ax.plot(df_ni['#r(A)'],df_ni['G(r)'], label='Ni (Referencia)')
ax.plot(df_cs50['#r(A)'],df_cs50['G(r)'], label='50% Ni')
ax.plot(df_cs60['#r(A)'],df_cs60['G(r)'], label='60% Ni')

ax.set_xlim([0,25])
ax.set_xlabel('r [A]')
ax.set_ylabel('G(r)')
ax.set_title('Comparación CS aleatorio (berendsen)')
ax.legend()

plt.show()