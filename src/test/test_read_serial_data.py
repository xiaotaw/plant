#encoding=utf8
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




if __name__ == "__main__":
    # 端口，GNU/linux上的 /dev/ttyUSB0 等或者windows上的 COM3 等
    #portx = "/dev/ttyS0"
    portx = "COM3"
    # 比特率，标准值之一：50,75,110,134,150,200,300,600,1200,1800,2400,4800,9600,19200,38400,57600,115200
    bps = 115200
    # 超时，None: 一直等待；0: 立即返回请求结果；其他：等待时间(单位为秒)
    timex = 5
    try:
        ser = serial.Serial(portx, bps, timeout=timex)
    except FileNotFoundError:
        print("Open Port Error: cannot open file %s" % portx)
        show_available_ports()
        exit()

    i = 0
    while True:
        try:
            raw = ser.readline()
            print(i, raw)
            i += 1
        except Exception as e:
            print("exception:", e)

        
    
