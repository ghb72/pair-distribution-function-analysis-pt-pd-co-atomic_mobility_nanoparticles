import pandas as pd
import matplotlib.pyplot as plt
plt.close("all")

df_FCC= pd.read_csv('graphics\\Pt-FCC.txt', sep='\s+')
df_50=pd.read_csv('graphics\\Pt-0.5-radrand.txt',sep='\s+')
df_75=pd.read_csv('graphics\\Pt-0.75-radrand.txt', sep='\s+')

fig, ax =plt.subplots(figsize=(10,5), layout='constrained')
ax.plot(df_FCC['#r(A)'], df_FCC['G(r)'], label='Pt (reescale)')
ax.plot(df_50['#r(A)'], df_50['G(r)'], label='Pt 50%')
ax.plot(df_75['#r(A)'], df_75['G(r)'], label='Pt 75%')


ax.set_xlabel('r [$\\AA$]')
ax.set_xlim([0,25])
ax.set_ylabel('G(r)')
ax.set_title('Comparación G(r) Pt aleatoria')
ax.grid('True', linestyle='-')
ax.legend()
plt.show()