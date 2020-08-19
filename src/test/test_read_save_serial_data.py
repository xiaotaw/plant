#encoding=utf8
import time
import serial 
from serial.tools import list_ports


def show_available_ports():
    port_list = list(list_ports.comports()) 
    if len(port_list) == 0:
        raise RuntimeError("No Avaiable Port!")
    else:
        print("Avaiable Port: %s" % len(port_list))
        for i, port in enumerate(port_list):
            print("%d: %s" % (i, str(port)))

def record(ser, n_seconds):
    t_list = []
    d_list = []
    t0 = time.time()
    assert (ser._timeout == 1), "timeout must be 1 second"
    for i in range(n_seconds):
        try:
            raw = ser.read(bps)
            d_list.append(raw)
            t1 = time.time()
            t_list.append(t1 - t0)
            t0 = t1
        except Exception as e:
            print("exception", e)
    return d_list, t_list

def save(d_list, filename):
    # check values
    d_valid = []
    for d in d_list:
        dl = []
        for dd in d.split(b"\n"):
            try:
                dd = dd.decode("utf8")
                dd = 0 if dd == "" else int(dd)
            except UnicodeDecodeError: 
                dd = 0
            except ValueError:
                dd = 0
            dl.append(dd)
        d_valid.append(dl)
    # save data
    f = open(filename, "w")
    for dl in d_valid:
        dl = [str(x) for x in dl]
        _ = f.write("\t".join(dl) + "\n")
    f.close()

if __name__ == "__main__":
    # 端口，GNU/linux上的 /dev/ttyUSB0 等或者windows上的 COM3 等
    #portx = "/dev/ttyS0"
    portx = "COM3"
    # 比特率，标准值之一：50,75,110,134,150,200,300,600,1200,1800,2400,4800,9600,19200,38400,57600,115200
    bps = 115200
    # 超时，None: 一直等待；0: 立即返回请求结果；其他：等待时间(单位为秒)
    timex = 1
    try:
        ser = serial.Serial(portx, bps, timeout=timex)
    except FileNotFoundError:
        print("Open Port Error: cannot open file %s" % portx)
        show_available_ports()
        exit()

    
    d_list, t_list = record(ser, 30)
    
    save(d_list, "src/assets/test_data.txt")


    assert len(t_list) == len(d_list)
    for t, d in zip(t_list, d_list):
        l = len(d.split(b"\n"))
        print(t, l, l/t)


        
    
