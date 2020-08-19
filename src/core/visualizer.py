import matplotlib as mpl
import matplotlib.pyplot as plt
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


def consumer(data_list, chunk_size):
    b, e = 0, 0
    length = len(data_list)
    for b in range(0, length, chunk_size):
        e = b + chunk_size
        e = length if e > length else e
        yield data_list[b : e]


class Visualizer(object):
    def __init__(self):
        self.fig = plt.figure("plant")
        # deque of data
        self.q = deque(maxlen=MAX_LEN)
        # the chunk_size of data added into deque per update
        self.chunk_size = 150
        
    # make sure the figure displays at left-top corner
    def _reset_fig(self):
        move_figure(plt.gcf(), backend, 0, 0)
        plt.ylim([0, 800])
        plt.xticks(())

    # draw 
    def draw(self, data):
        g  = consumer(data, self.chunk_size)
        for d in g:
            self.q.extend(d)
            plt.plot(self.q, '-r')
            self._reset_fig()
            plt.draw()
            plt.pause(EPSILON)
            if len(self.q) == MAX_LEN:
                plt.cla()

if __name__ == "__main__":

    f = open("src/assets/plant_dynamic_wind_1_signal.txt")
    s = f.readlines()
    f.close()
    s = [[int(x) for x in l.strip().split()] for l in s]


    vis = Visualizer()
    for i, data in enumerate(s):
        print(i)
        vis.draw(data)
