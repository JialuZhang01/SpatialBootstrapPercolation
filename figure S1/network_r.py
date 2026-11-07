
import pickle as pk
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

networkpath = 'network/'
zetas = [3, 6, 12, 1000]
avg_k = 10
num_net = 3

r_mean = []
r_std = []
num=0
for z in zetas:
    num+=1
    print(z,num)
    values = []

    for i in range(num_net):
        filename = (
            networkpath
            + f'NetID{i}_avgk{avg_k}_zeta{z}_spatialNet.pkl'
        )

        with open(filename, 'rb') as f:
            G = pk.load(f)

        values.append(nx.degree_assortativity_coefficient(G))

    r_mean.append(np.mean(values))
    r_std.append(np.std(values, ddof=1))

r_mean = np.array(r_mean)
r_std = np.array(r_std)

fig, ax = plt.subplots(figsize=(5.6, 4.8))

# 浅灰色连接线、空心圆点和误差棒
ax.errorbar(
    zetas, r_mean,
    yerr=r_std,
    fmt='o',
    linestyle='-',
    color='#918072',
    ecolor='#918072',
    markerfacecolor='none',
    markeredgecolor='#918072',
    linewidth=1.5,
    capsize=4
)

# r = 0 参考线
ax.axhline(
    0,
    color='gray',
    linestyle='--',
    linewidth=1
)

ax.set_xscale('log')
ax.set_xlabel(r'$\zeta$', fontsize=18)
ax.set_ylabel(r'$r$', fontsize=18)

ax.tick_params(axis='both', labelsize=16)
ax.set_xticks(zetas)
ax.set_xticklabels([str(z) for z in zetas])

plt.tight_layout()
plt.savefig('degree_assortativity.pdf', bbox_inches='tight')

plt.show()

print('zeta, mean assortativity, standard deviation')
for z, m, s in zip(zetas, r_mean, r_std):
    print(f'{z:4d}  {m:.8f}  {s:.8f}')