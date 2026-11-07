import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(5.6, 4.8))

c_draw = ['#7F318D','#1072BD', '#EDB021', '#D7592C']
xingzhuang = ['s', 'o', '*', '^']

lmin = 1
lmax = 500

zetas=[3,6,12,1000]

for idx, z in enumerate(zetas):

    with open(f'zeta{z}_l_num.txt', 'r', encoding='utf-8-sig') as f0:
        dic_l = {}

        for line in f0:
            line = line.strip().split('\t')
            num_net = int(line[0][-1])

            for item in line[1:]:
                item = item.strip().split(',')
                l = float(item[0])
                count = int(item[1])

                dic_l[l] = count / num_net

  
    x_dis = np.array(sorted(dic_l.keys()))
    y_pro = np.array([
        dic_l[l] / (num_net * 500000)
        for l in x_dis
    ])

    
    mask = (
        (x_dis >= lmin) &
        (x_dis <= lmax) &
        (y_pro > 0) &
        np.isfinite(y_pro)
    )

    x_fit = x_dis[mask]
    y_fit = y_pro[mask]

   
    slope, intercept = np.polyfit(x_fit, np.log(y_fit), 1)
    x_new = []
    y_new = []
    for xi, yi in zip(x_dis, y_pro):
        if xi==int(xi):   
            x_new.append(xi)
            y_new.append(yi)

    if z==1000:
        plt.scatter(
            x_new, y_new,
            marker=xingzhuang[idx],
            facecolors='none',
            edgecolors=c_draw[idx],
            alpha=0.5,
            label=fr'$\zeta={z}$, slope={slope:.3g}'
        )
    else:
        plt.scatter(
            x_new, y_new,
            marker=xingzhuang[idx],
            facecolors='none',
            edgecolors=c_draw[idx],
            alpha=0.6,
            label=fr'$\zeta={z}$, slope={slope:.4g}'
        )

    x_line = np.linspace(x_fit.min(), x_fit.max(), 300)
    y_line = np.exp(intercept + slope * x_line)

    plt.plot(
        x_line, y_line,
        '--',
        color=c_draw[idx],
        linewidth=1.5
    )
  

plt.yscale('log')
plt.minorticks_on()
plt.xlabel(r'Link length, $l$', fontsize=18)
plt.ylabel(r'$p(l)$', fontsize=18)
plt.tick_params(labelsize=16)
plt.legend(frameon=False, fontsize=15)
plt.ylim(bottom=2e-8)


plt.savefig('链路长度分布_slope.pdf')
plt.show()