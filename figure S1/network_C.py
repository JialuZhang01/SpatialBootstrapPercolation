
import pickle as pk
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

networkpath = 'network/'
zetas = [3, 6, 12, 1000]
avg_k = 10
num_net = 3

C_mean = []
C_std = []
num0=0
for z in zetas:
    num0+=1
    print(num0)
    values = []

    for i in range(num_net):
        filename = (
            networkpath
            + f'NetID{i}_avgk{avg_k}_zeta{z}_spatialNet.pkl'
        )

        with open(filename, 'rb') as f:
            G = pk.load(f)

        values.append(nx.average_clustering(G))

    C_mean.append(np.mean(values))
    C_std.append(np.std(values, ddof=1))

C_mean = np.array(C_mean)
C_std = np.array(C_std)

fig, ax = plt.subplots(figsize=(5.6, 4.8))


ax.errorbar(
    zetas, C_mean,
    yerr=C_std,
    fmt='o',
    linestyle='-',
    color='#918072',
    ecolor='#918072',
    markerfacecolor='none',
    markeredgecolor='#918072',
    linewidth=1.5,
    capsize=4
)

ax.set_xscale('log')
ax.set_xlabel(r'$\zeta$', fontsize=18)
ax.set_ylabel(r'$\langle C\rangle$', fontsize=18)

ax.tick_params(axis='both', labelsize=16)
ax.set_xticks(zetas)
ax.set_xticklabels([str(z) for z in zetas])

plt.tight_layout()
plt.savefig('average_clustering.pdf', bbox_inches='tight')
plt.show()

print('zeta, mean clustering, standard deviation')
for z, m, s in zip(zetas, C_mean, C_std):
    print(f'{z:4d}  {m:.8f}  {s:.8f}')