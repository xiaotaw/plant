#encoding=utf8
import serial 
from serial.tools import list_ports
from queue import Queue
import threading

def show_available_ports():
    port_list = list(list_ports.comports()) 
    if len(port_list) == 0:
        raise RuntimeError("No Avaiable Port!")
    else:
        print("Avaiable Port: %s" % len(port_list))
        for i, port in enumerate(port_list):
            print("%d: %s" % (i, str(port)))


class Plant(object):
    
    # portx: 端口，GNU/linux上的 /dev/ttyUSB0 等或者windows上的 COM3 等
    # bps: 比特率，标准值之一：50,75,110,134,150,200,300,600,1200,1800,2400,4800,9600,19200,38400,57600,115200
    # timeout: 超时，None: 一直等待；0: 立即返回请求结果；其他：等待时间(单位为秒)
    def __init__(self, portx="COM3", bps=115200, timeout=5, window_size=1.0, hop_size=0.5):
        # configuration
        self.portx = portx
        self.bps = bps
        self.timeout = timeout
        if isinstance(window_size, float):
            assert 0 < window_size <= 1,  "window_size should be a integer or a float in (0,1]"
            window_size = int(window_size * bps)
        else:
            assert isinstance(window_size, int), "window_size should be a integer or a float in (0,1]"
        self.window_size = window_size

        if isinstance(hop_size, float):
            assert 0 < hop_size <= 1,  "window_size should be a integer or a float in (0,1]"
            hop_size = int(hop_size * bps)
        else:
            assert isinstance(hop_size, int), "window_size should be a integer or a float in (0,1]"
        self.hop_size = hop_size

        assert hop_size <= window_size, "hop_size should not be greater than window_size"
            
        # build and listen to serial port
        try:
            self.ser = serial.Serial(self.portx, self.bps, timeout=self.timeout)
        except serial.serialutil.SerialException:
            print("Open Port Error: cannot open file %s" % portx)
            show_available_ports()
            exit()
        # queue to store data recieved from serial port
        self.q = Queue(maxsize=30 * bps)


    def _recieve_data(self):
        while True:
            # if queue is full, pop out some old data
            if self.q.full():
                print("[Warning] recieved too many data from plant sensor! ")
                for _ in range(self.hop_size):
                    _ = self.q.get()
            try:
                raw = self.ser.readline().decode("utf8").strip()
                if raw != "":
                    data = int(raw)
                    self.q.put(data)
            except Exception as e:
                print("exception:", e)
        
    def start(self):
        # start a background thread to recieve data from sensor
        self.recieve_thread = threading.Thread(target=Plant._recieve_data, args=(self,))
        self.recieve_thread.start()