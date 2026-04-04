import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

L_size = 500   # Lattice length
T_active = 6  # The activation threshold (T)
zetas = [z for z in range(3,51)]   # Range of zeta values
source_p_list = [x / 1000 for x in range(85, 266)]  
dic_zeta_p = {}

for zeta in zetas:
    dic_zeta_p[zeta] = {}
    f = open(f'deal_result/source_p_rc/zeta={zeta}_p_rc.txt', 'r', encoding='utf-8-sig')
    for line in f:
        line = line.strip().split('\t')
        p0 = float(line[0][1:])
        if p0 in source_p_list:
            dic_zeta_p[zeta][p0] = int(line[1])
    f.close()


row_labels = sorted(list(set(key for inner_dict in dic_zeta_p.values() for key in inner_dict.keys())), reverse=True)
col_labels = sorted(dic_zeta_p.keys())


matrix = np.zeros((len(row_labels), len(col_labels)))
for i, row in enumerate(row_labels):
    for j, col in enumerate(col_labels):
        if row in dic_zeta_p[col]:
            matrix[i, j] = dic_zeta_p[col][row]

plt.figure(figsize=(8, 6))

step = 30
y_tick_labels = [label if i % step == 0 else '' for i, label in enumerate(row_labels)]

# Use seaborn to create a heatmap
ax = sns.heatmap(
    matrix,
    annot=False,
    fmt=".0f",
    cmap="viridis",
    cbar_kws={"label": "$r_c$"},
    linewidths=0,
    cbar=True,
    square=False,
    xticklabels=col_labels,
    yticklabels=y_tick_labels
)


cbar = ax.collections[0].colorbar
cbar.ax.set_ylabel("$r^c_h$", fontsize=20)

for i, label in enumerate(ax.get_xticklabels()):
    if i % 15 != 1:
        label.set_visible(False)


plt.title(r"$L=500,\langle k \rangle=10,T=6$",fontsize=20)
plt.xlabel("ζ", fontsize=20)
plt.ylabel("p", fontsize=20)


plt.xticks(fontsize=18, rotation=0)
plt.yticks(fontsize=18, rotation=0)

plt.tight_layout()
plt.show()
