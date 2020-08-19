#
import time
import matplotlib as mpl
import matplotlib.pyplot as plt

from collections import deque

backend = mpl.get_backend()


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



if __name__ == "__main__":
    plt.ion()
    fig = plt.figure()
    #move_figure(fig, backend, 0, 0)

    f = open("src/assets/plant_dynamic_wind_1_signal.txt")
    s = f.readlines()
    f.close()


    a = list(range(10))
    b = [x * 10 for x in a]

    MAX_LEN = 500

    q = deque(maxlen=MAX_LEN)
    for i, l in enumerate(s):
        print(i)
        data = [int(x) for x in l.strip().split("\t")]
        g = consumer(data, 150)
        for d in g:
            q.extend(d)
            plt.plot(q, '-r')
            plt.ylim([0, 800])
            plt.xticks(())
            plt.draw()
            plt.pause(0.000000001)
            if len(q) == MAX_LEN:
                plt.cla()