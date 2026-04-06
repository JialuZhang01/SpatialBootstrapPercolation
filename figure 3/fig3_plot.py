import matplotlib.pyplot as plt
import numpy as np
import os

def mkdirectory(path):    
    """
    Create a directory at the specified path if it does not already exist.
    """
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

if __name__ == "__main__":        
    fig, axs = plt.subplots(
        nrows=3, ncols=3, 
        sharey='row', 
        sharex='col', 
        figsize=(10.5, 7.6)  
    )
    
    plt.subplots_adjust(
        wspace=-1,  
        hspace=0  
    )
    
    zetas=[3,12,1000]  # The list of zeta values
    z_pc = [0.25,0.229,0.243]   # Corresponding pc2
    text_l =['a','b','c','d','e','f','g','h','i']
    avg_k = 10   #  Average Degree
    T_active = 6  # The activation threshold (T)
    
    
    c_draw =['#77AE43','#1072BD','#EDB021','#D7592C','#7F318D']
    list_label =['$p_c^{(2)}$','$p_c^{(2)}+0.0005$','$p_c^{(2)}+0.001$','$p_c^{(2)}+0.005$']     
    
    for i0 in range(3):  
        for j0 in range(3): 
            ax = axs[i0, j0] 
            ax.margins(x=0, y=0) 
            ax.tick_params(axis='x', labelsize=11)
            ax.tick_params(axis='y', labelsize=11)
            
            source_pro = [] 
            source_pro.append(z_pc[j0])
            source_pro.append(z_pc[j0]+round(0.0005,4))
            source_pro.append(z_pc[j0]+round(0.001,3))
            source_pro.append(z_pc[j0]+round(0.005,3))
            
            if i0==0: # P∞
                ax.set_ylim(0, 1)
                ax.set_yticks([0,0.2,0.4,0.6,0.8,1.0])
                c0=0
                f1 = open('3_12_1000_cascade_dynamic/'+'T='+str(T_active) +'_avgk='+str(avg_k) +'_t_S(gc)_zeta'+str(zetas[j0])+'.txt','r', encoding='utf-8-sig')
                for line_f1 in f1:
                    x_average = []
                    y_average = []
                    line_f1 = line_f1.strip().split('\t')
                    if float(line_f1[0][1:]) in source_pro:
                        if float(line_f1[0][1:]) == 0.251:
                            for i in line_f1[1:-5]:
                                i = i.strip().split(',')
                                x_average.append(int(i[0][1:]))
                                y_average.append(float(i[1]))
                        else:
                            for i in line_f1[1:]:
                                i = i.strip().split(',')
                                x_average.append(int(i[0][1:]))
                                y_average.append(float(i[1]))
                        c0+=1
                        ax.plot(x_average, y_average,ls='-', lw=1, color=c_draw[c0-1], alpha = 1,label=list_label[c0-1])
                        ax.scatter(x_average, y_average, facecolors='none',edgecolors=c_draw[c0-1],alpha=0.5) 
                f1.close()
                ax.legend(ncol=2,fontsize=10.5,bbox_to_anchor=(1.025, -0.05),loc='lower right', 
                columnspacing=0.5,frameon=False) 
                ax.set_title('ζ='+str(zetas[j0]), fontsize=13)  
                if j0 == 0:
                    ax.set_ylabel('$P_\infty(t)$',fontsize=13)
            
            if i0==1: # S_t
                ax.set_ylim(0.0000066,0.28)         
                c0=0
                f1 = open('3_12_1000_cascade_dynamic/'+'T='+str(T_active) +'_avgk='+str(avg_k) +'_t_S(gc)_zeta'+str(zetas[j0])+'.txt','r', encoding='utf-8-sig')
                for line_f1 in f1:
                    x_average = []
                    y_average = []
                    line_f1 = line_f1.strip().split('\t')
                    if float(line_f1[0][1:]) in source_pro:
                        if float(line_f1[0][1:]) == 0.251:
                            for i in line_f1[1:-5]:
                                i = i.strip().split(',')
                                x_average.append(int(i[0][1:]))
                                y_average.append(float(i[1]))
                        else:
                            for i in line_f1[1:]:
                                i = i.strip().split(',')
                                x_average.append(int(i[0][1:]))
                                y_average.append(float(i[1]))
                        y = [0 for a in range(len(y_average))]
                        for j in range(1,len(y_average)):
                            y[j]=y_average[j]-y_average[j-1]
                           
                        c0+=1
                        ax.plot(x_average[1:], y[1:],ls='-', lw=1, color=c_draw[c0-1], alpha = 1,label=list_label[c0-1])
                        ax.scatter(x_average[1:], y[1:], facecolors='none',edgecolors=c_draw[c0-1],alpha=0.5)  
                f1.close()
                ax.set_yscale('log')
                if j0 == 0:
                    ax.set_ylabel('$S_t$',fontsize=13)
    
            if i0==2: # η_t
                ax.set_ylim(0.15,1.75)
                ax.set_yticks(np.arange(0.2, 1.76, 0.4))
                c0=0
                f1 = open('3_12_1000_cascade_dynamic/'+'T='+str(T_active) +'_avgk='+str(avg_k) +'_t_S(gc)_zeta'+str(zetas[j0])+'.txt','r', encoding='utf-8-sig')
                for line_f1 in f1:
                    x_average = []
                    y_average = []
                    line_f1 = line_f1.strip().split('\t')
                    if float(line_f1[0][1:]) in source_pro:
                        for i in line_f1[1:]:
                            i = i.strip().split(',')
                            x_average.append(int(i[0][1:]))
                            y_average.append(float(i[1]))
                        y = [0 for a in range(len(y_average))]
                     
                        for j in range(1,len(y_average)):
                            y[j]=y_average[j]-y_average[j-1] 
                        y1 = [0 for a in range(len(y_average))]
                        for j in range(2,len(y)):
                            y1[j]=y[j]/y[j-1]
                           
                        c0+=1
                        ax.plot(x_average[2:], y1[2:],ls='-', lw=1, color=c_draw[c0-1], alpha = 1,label=list_label[c0-1])
                        ax.scatter(x_average[2:], y1[2:], facecolors='none',edgecolors=c_draw[c0-1],alpha=0.5)  
                        
                ax.axhline(y=1, color='#73575c', linestyle='--', label='y=1',linewidth=1.6)
                
                f1.close()
                ax.set_xlabel('t',fontsize=13)
                if j0 == 0:
                    ax.set_ylabel('$η_t$',fontsize=13)
                    ax.set_xlim(-12, 261)  
                    ax.set_xticks(range(0, 261,100)) 
                    
                    
                if j0 == 2:
                    ax.set_xlim(-5, 100) 
                    ax.set_xticks(range(0, 101,50)) 
                   
                
                if j0 == 1:
                    ax.set_xlim(-12, 355)  
                    ax.set_xticks(range(0, 355,100))  
            
            ax.text(0.05, 0.98, text_l[i0*3+j0], 
                  transform=ax.transAxes, 
                  fontsize=24,   
                  # fontweight='bold',    
                  fontfamily='SimHei',    
                  ha='left', va='top')         
    
    
    plt.tight_layout()
    path_line = 'FIG3/' 
    mkdirectory(path_line)
    plt.savefig(path_line+'fig3.pdf')
    plt.show()


  
   
    


