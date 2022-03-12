import numpy as np
import matplotlib.pyplot as plt
from Param2d import Cursor
from DataGen import DataGenerator


ant = DataGenerator()
#--------------------------------------------#
# plot config $$$$
L = -3  # plot boudries
R = 2.5
D = L
U = R

x_range = np.linspace(L-1, R+1, 750)

# critical points config
"""['tab:orange', 'magenta', 'k', 'tab:cyan', 'tab:green', 'b', 'darkviolet', 'darkgrey']"""
cp_colors = ['#ff7f0e', '#ff00ff', '#000000', '#17becf', '#2ca02c', '#0000ff', '#9400d2', '#a9a9a9']
# initial number of iterations: -1 hides critical point, 0 shows cp but not iterations
cp_initial = [0, 0, 0, 0, 0, 1, 1, 0]

#--------------------------------------------#
# update functions
""" change the places marked with $$$$ to configure 
the parameters that need to be changed """

def update_f():
    y = ant.f_data(x_range)
    f_plot.set_ydata(y)

def update_cobweb():
    px, py = ant.cobweb()
    c_plot.set_data(px, py)

def update_critical_points():
    cp_cobwebs = ant.criticalpoints_cobwebs()
    for i in range(len(cp_plots)):
        px, py = cp_cobwebs[i]
        cp_plots[i].set_data(px, py)

    
def update_cursor(event):  # trigger
    """ 
    Update the data depending on 2D parameter space
    Must contain cursor.on_mouse_click(event)
    """
    position = cursor.on_mouse_click(event)
    if position is None: 
        return
    x, y = position
    # set Parameters controlled by Param2d here
    ant.aM3 = x     # $$$$
    ant.mM3 = y     # $$$$

    update_f()
    update_cobweb()
    update_critical_points()

    fig.canvas.draw_idle()

#--------------------------------------------#
# function and cobweb plot

fig = plt.figure('Cobweb Plot',figsize=(10,10))
f_ax = plt.axes([0.1, 0.1, 0.8, 0.8])
f_ax.set_aspect('equal')
f_ax.set_xlim(L, R)
f_ax.set_ylim(D, U)
f_ax.set_xlabel(r'$x_n$')
f_ax.set_ylabel(r'$x_{n+1}$')
plt.grid(True, linestyle='--')

y = ant.f_data(x_range)  # function
px, py = ant.cobweb()    # cobweb
    
c_plot, = plt.plot(px, py, 'gold')
f_plot, = plt.plot(x_range, y, 'r.', markersize=4)
plt.plot(x_range, x_range, 'grey')  # diagonal

#--------------------------------------------#
# critical points

# initialize plots
cp_plots = [plt.plot(0, 0, '-s', color=col)[0] for col in cp_colors]  

cp_cobwebs = ant.criticalpoints_cobwebs(cp_initial)
for i in range(len(cp_plots)):
    px, py = cp_cobwebs[i]
    cp_plots[i].set_data(px, py)

#--------------------------------------------#
# interactive controls

cursor = Cursor(x_init=ant.aM3, y_init=ant.mM3)  # cursor with (optional) initial parameters 
cursor.fig.canvas.mpl_connect('button_press_event', update_cursor)

plt.show()

