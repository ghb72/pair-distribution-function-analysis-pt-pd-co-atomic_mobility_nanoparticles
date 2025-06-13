import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


blue = '#233652'
brown = '#33260D'
lightblue = '#B6C1D1'

M = pd.DataFrame()

df_exp = pd.read_csv('..\\Post-PtPdCo-PDF.csv', sep = '\s+', header=None, names=['r','G(r)'])
df_exp = df_exp.replace('--',np.nan).dropna()
rest_df_exp = df_exp["G(r)"].iloc[1::2].astype(float)
rest_df_exp = rest_df_exp.reset_index(drop=True)
rest_df_exp.index += 1
M['exp'] = rest_df_exp

dx = 0.02

#M.index = M0['#r(A)']

M.index = (M.index + 1)*dx

F = M.iloc[::15]
equis = np.arange(0,15)
z_array = F['exp'].to_numpy()
y_array = F.index.to_numpy()
equis, ye = np.meshgrid(y_array, equis)
zeta = np.empty(shape=(15,len(z_array)))
for i in range (15):
    zeta[i] = z_array

ax = plt.figure(figsize=(8,8)).add_subplot(projection='3d')

surf = ax.plot_surface(equis, ye, zeta, antialiased=True, lw=3, color = blue)
#ax.set_facecolor('#D1C8B6')
#print(np.shape(equis), np.shape(ye), np.shape(zeta))

ax.tick_params(labelcolor=blue)
for axis in ['top', 'bottom', 'left', 'right']:
    ax.spines[axis].set_color(blue)
    ax.spines[axis].set(linewidth = 4)

ax.set_xlabel('r[$\\AA$]', color=blue, weight='bold')
ax.set_ylabel('Time',color=blue, weight='bold')
ax.set_facecolor('#D1C8B6')
ax.grid(False)


plt.rc('font', size=16, weight='bold')

#fpath = Path(mpl.get_data_path(), "C:/Users/guill/Downloads/Fira_Sans/FiraSans-Medium.ttf")

plt.rcParams['font.family'] = 'sans-serif'
plt.show()
