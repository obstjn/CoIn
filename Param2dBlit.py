import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import glob

# ------------------------------------------ #
# config $$$$

# file name of 2D Scan
#file_name = "bandcount.tna"
file_name = "/home/obstjn/Dokumente/Chaos-HiWi/piecewise_linear/5-partitions/2D-Scan-5/Scans/9/bandcount.tna"
force_reload = False

# plotted points in x and y direction
dimensions = (2400,2400)

# Bounds of the 2D scan
L= -2
R= -0.99
D= 3.2  
U= 4.2  

xlabel = 'aM3'
ylabel = 'mM3'

# ------------------------------------------ #

class Cursor:
    """
    A cross hair cursor.
    """
    def get_data(self, reload_cache=force_reload):
        # search for cache
        npy_file_list = glob.glob('cache_2D_scan.npy')  

        # if force_reload or no cached *.npy file exists
        if reload_cache or not npy_file_list:
            # read from .tna file
            print("Loading .tna file, please wait...")
            # change 'b' to 'i' if max bandcount exceeds byte size of 127
            img = np.loadtxt(file_name, dtype=np.dtype('b'), usecols=2)  
            img = img.reshape(dimensions)
            np.save('cache_2D_scan.npy', img)  # cache the scan
            print("Success! Created new cache file.")
        else:
            img = np.load('cache_2D_scan.npy')  # load cache
        return img
        

    def __init__(self, x_init=None, y_init=None):
        self.fig, self.ax = plt.subplots(figsize=(10,10))
        #self.text = plt.text(0.76, 1.02, 'hallo', transform=self.ax.transAxes)
        self.background = None
        self._background_stale = False
        self._creating_background = False
        self.ax.set_title('2D-Scan')
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        self.horizontal_line = self.ax.axhline(color='k', lw=0.8, ls='--')
        self.vertical_line = self.ax.axvline(color='k', lw=0.8, ls='--')
        # text location in axes coordinates
        self.text = self.ax.text(0.76, 1.02, '', transform=self.ax.transAxes)
        self.ax.figure.canvas.mpl_connect('draw_event', self.on_draw)

        # initial parameters for the crosshair
        if x_init is not None and y_init is not None:
            self.set_cross_hair_visible(True)
            # update the line positions
            self.horizontal_line.set_ydata(y_init)
            self.vertical_line.set_xdata(x_init)
            self.text.set_text(f'{xlabel}={x_init:.3f}, {ylabel}={y_init:.3f}')
            self.ax.figure.canvas.draw()

        # load the 2D scan data
        img = self.get_data()
        
        # generate plot
        norm = plt.Normalize(0,18)
        cmap = matplotlib.colors.ListedColormap(['gray',
                                                 '#FFFFB3',
                                                 '#BEBADA',
                                                 '#FB8072',
                                                 '#80B1D3',
                                                 '#FDB462',
                                                 '#B3DE69',
                                                 '#FCCDE5',
                                                 '#E41A1C',
                                                 '#377EB8',
                                                 '#4DAF4A',
                                                 '#984EA3',
                                                 '#FF7F00',
                                                 '#FFFF33',
                                                 '#A65628',
                                                 '#F781BF',
                                                 'mediumseagreen',
                                                 'gold',
                                                 'steelblue',
                                                 'mediumorchid',
                                                 'aquamarine'])    

        plt.imshow(img, cmap=cmap, norm=norm, origin='lower', extent=[L,R,D,U], interpolation='none')
        plt.xlim(L,R)
        plt.ylim(D,U)
        plt.colorbar()  # $$$$ activate as needed

        self.fig.canvas.manager.set_window_title('2D Parameter selector')


    def set_cross_hair_visible(self, visible):
        need_redraw = self.horizontal_line.get_visible() != visible
        self.horizontal_line.set_visible(visible)
        self.vertical_line.set_visible(visible)
        self.text.set_visible(visible)
        return need_redraw


    def on_draw(self, event):
        print('draw')
        # ignore calls to draw if it is in the process of creating the background
        if self._creating_background:
            return
        # else the background needs a redraw upon clicking/cross hair usage
        self._background_stale = True


    def create_new_background(self):
        if self._creating_background:
            # discard calls triggered from within this function
            return
        self._creating_background = True
        # hide cross hair & text and draw anew
        self.set_cross_hair_visible(False)
        self.ax.figure.canvas.draw()
        self.ax.figure.canvas.flush_events()
        # save the background
        self.background = self.ax.figure.canvas.copy_from_bbox(self.ax.figure.bbox)
        self._background_stale = False  # fresh background created
        self.set_cross_hair_visible(True)
        self._creating_background = False


    def on_mouse_click(self, event):
        if self.background is None:
            self.create_new_background()
        active_tool = self.ax.get_figure().canvas.manager.toolbar.mode
        # do nothing if tool e.g. zoom is selected or the background isn't ready
        if active_tool != '' or self._creating_background:
            self._background_stale = True
            return
        # if out of axes, hide cross hair
        if not event.inaxes == self.ax:
            need_redraw = self.set_cross_hair_visible(False)
            if need_redraw:
                self.ax.figure.canvas.restore_region(self.background)
                self.ax.figure.canvas.blit(self.ax.figure.bbox)  # redraw entire figure
            return
        # update values
        else:
            if self._background_stale:
                self.create_new_background()
            self.set_cross_hair_visible(True)
            x, y = event.xdata, event.ydata
            # update the line positions
            self.horizontal_line.set_ydata(y)
            self.vertical_line.set_xdata(x)
            self.text.set_text(f'{xlabel}={x:.3f}, {ylabel}={y:.3f}')
            # clear background
            self.ax.figure.canvas.restore_region(self.background)
            # update main axes and text
            self.ax.draw_artist(self.horizontal_line)
            self.ax.draw_artist(self.vertical_line)
            self.ax.draw_artist(self.text)
            self.ax.figure.canvas.blit(self.ax.figure.bbox)
            # for max speed: activate below and change above to self.ax.bbox
            # can cause glitches when window looses focus
            #self.ax.figure.canvas.blit(self.text.get_window_extent())

            return x, y


#--------------------------------------------#
# main method for testing & debugging

if __name__=='__main__':
    # function called upon cursor action
    def update_cursor(event):
        position = cursor.on_mouse_click(event)
        if position is not None:
            print(position)

    cursor = Cursor()
    # motion_notify_event, button_press_event
    cursor.fig.canvas.mpl_connect('button_press_event', update_cursor)

    plt.show()
