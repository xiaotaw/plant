import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import rcParams
from collections import deque


# global setting
plt.ion()
backend = mpl.get_backend()
#
MAX_LEN = 500
EPSILON = 1e-7

def move_figure(fig, backend, x=300, y=300):
    if backend == "Qt5Agg":
        fig.canvas.manager.window.move(x, y)
    elif backend == "WXAgg":
        fig.canvas.manager.window.SetPosition((x, y))
    elif backend == "TkAgg":
        fig.canvas.manager.window.wm_geometry('+%d+%d' % (x, y))
    else:
        print("Unsupported matplotlib backend: %s" % backend)

def top_most_figure(fig, backend):
    #print("\nbackend: %s\n" % backend)
    if backend == "Qt5Agg":
        fig.canvas.manager.window.activateWindow()
        fig.canvas.manager.window.raise_()
    elif backend == "TkAgg":
        # correct?
        fig.canvas.manager.window.attributes("-topmost", 1)
        #fig.canvas.manager.window.attributes("-topmost", 0)
    else:
        print("unsupported backend: %s" % backend)

def get_full_screen_size():
    mgr = plt.get_current_fig_manager()
    mgr.full_screen_toggle()
    px, py = mgr.canvas.width(), mgr.canvas.height()
    plt.close()
    return px, py

px, py = get_full_screen_size()

def consumer(data_list, chunk_size):
    b, e = 0, 0
    length = len(data_list)
    for b in range(0, length, chunk_size):
        e = b + chunk_size
        e = length if e > length else e
        yield data_list[b : e]


class Visualizer(object):
    def __init__(self, name, left_loc = 0, top_loc = 0, width=640, height=480, predefined_loc="None"):
        # config
        self.name = name
        self.left_loc = left_loc
        self.top_loc = top_loc 
        self.dpi = rcParams['figure.dpi']
        self.width = width
        self.height = height
        # figure and axes
        self.fig = plt.figure(self.name, figsize=(self.width / self.dpi, self.height / self.dpi))
        self.ax = self.fig.add_subplot()
        # deque of data
        self.q = deque(maxlen=MAX_LEN)
        # the chunk_size of data added into deque per update
        self.chunk_size = 150
        # window info
        self.px, self.py = px, py
        # left-top or right-top
        self.predefined_loc = predefined_loc
        
    def _set_loc(self, pos="left-top"):
        if pos == "left-top":
            move_figure(self.fig, backend, 0, 0)
        elif pos == "right-top":
            move_figure(self.fig, backend, self.px-self.width, 0)

    # make sure the figure displays at a specific position of the window
    def _reset_fig(self):
        if self.predefined_loc is None:
            move_figure(self.fig, backend, self.left_loc, self.top_loc)
        else:
            self._set_loc(self.predefined_loc)
        top_most_figure(self.fig, backend)
        #self.ax.set_ylim([0, 800])
        self.ax.set_xticks(())


    # draw 
    def draw(self, data):
        g  = consumer(data, self.chunk_size)
        for d in g:
            self.q.extend(d)
            self.ax.plot(self.q, '-r')
            self._reset_fig()
            plt.draw()
            plt.pause(EPSILON)
            if len(self.q) == MAX_LEN:
                self.ax.clear()

if __name__ == "__main__":

    # px, py = get_full_screen_size()
    # print("full screen size: %d, %d" % (px, py))
    # exit(0)

    f = open("src/assets/plant_dynamic_wind_1_signal.txt")
    s = f.readlines()
    f.close()
    s = [[int(x) for x in l.strip().split()] for l in s]


    vis = Visualizer("recorded plant signal")
    for i, data in enumerate(s):
        print(i)
        vis.draw(data)
