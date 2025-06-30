import pandas as pd
import matplotlib.pyplot as plt
plt.close("all")

df_FCC= pd.read_csv('Ni-FCC.txt', sep='\s+')
df_FCCb=pd.read_csv('Ni-FCCb.txt',sep='\s+')

fig, ax =plt.subplots(figsize=(10,5), layout='constrained')
ax.plot(df_FCC['#r(A)'], df_FCC['G(r)'], label='Ni (reescale)')
ax.plot(df_FCCb['#r(A)'], df_FCCb['G(r)'], label='Ni (berendsen)')


ax.set_xlabel('r [A]')
ax.set_xlim([0,25])
ax.set_ylabel('G(r)')
ax.set_title('Comparación G(r) Ni')
#ax.grid('True')
ax.legend()
plt.show()