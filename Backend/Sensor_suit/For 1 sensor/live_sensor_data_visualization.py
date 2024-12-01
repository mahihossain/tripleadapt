import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

style.use('fivethirtyeight')
fig, axs = plt.subplots(2, 3)

def animate(i):
    c = 0
    graph_data = open('data.txt', 'r').read()
    lines = graph_data.split('\n')
    ax_lst = []
    ay_lst = []
    az_lst = []
    gx_lst = []
    gy_lst = []
    gz_lst = []
    counter_lst = []
    for line in lines:
        if len(line) > 1:
            pos_start = line.find("b'")
            pos_end = line.find("\n")
            values = (line[pos_start+2:pos_end]).split(";")
            (ax,ay,az,gx,gy,gz) = tuple(values)
            ax_lst.append(float(ax))
            ay_lst.append(float(ay))
            az_lst.append(float(az))
            gx_lst.append(float(gx))
            gy_lst.append(float(gy))
            gz_lst.append(float(gz))
            counter_lst.append(c)
        c = c + 0.5
        

#    axs.set_xlim(min(min(gx),min(ax),min(ay),min(az),min(gy),min(gz)), max(max(ax),max(ay),max(az),max(gx),max(gy),max(gz)))    
    axs[0,0].plot(counter_lst, ax_lst)
    axs[0,0].set_title('ax')
    axs[0,1].plot(counter_lst, ay_lst)
    axs[0,1].set_title('ay')
    axs[0,2].plot(counter_lst, az_lst)
    axs[0,2].set_title('az')
    axs[1,0].plot(counter_lst, gx_lst)
    axs[1,0].set_title('gx')
    axs[1,1].plot(counter_lst, gy_lst)
    axs[1,1].set_title('gy')
    axs[1,2].plot(counter_lst, gz_lst)
    axs[1,2].set_title('gz')


ani = animation.FuncAnimation(fig, animate, blit=False, interval=500, frames=500)    
plt.show()