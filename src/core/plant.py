#encoding=utf8
import os
import time
import threading
import serial 
from serial.tools import list_ports
from queue import Queue
from scipy import io as sio

from global_config import global_config
from core.decoder import Decoder

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
    
    # window_ratio： window_size / sample_rate, usually should be a float in (0,1], 
    # hop_ratio: hot_size / sample_rate, usually should be a float in (0,1]
    
    # train_offline: 
    #   if True, use saved data to train the decoder,
    #   if False, collect data online from serial port to train the decoder
    # offline_x: the saved data to train the decoder during offline training 
    
    def __init__(self, portx="COM3", bps=115200, timeout=1, window_ratio=1.0, hop_ratio=0.5, 
                 train_online=False):
        # configuration
        self.portx = portx
        self.bps = bps
        self.timeout = timeout
        
        # build and listen to serial port
        try:
            self.ser = serial.Serial(self.portx, self.bps, timeout=self.timeout)
        except serial.serialutil.SerialException:
            print("[Error]: cannot open serial port %s" % portx)
            show_available_ports()
            exit()
        
        # stablize plant sensor
        self._stableize_sensor()
        
        # get sample rate
        self.sample_rate = self._get_sample_rate()
        
        # window_size and hot_size
        assert hop_ratio <= window_ratio, "hop_size should not be greater than window_size"
        self.window_size = int(window_ratio * self.sample_rate)
        self.hop_size = int(hop_ratio * self.sample_rate)
            
        # queue to store data recieved from serial port
        self.q = Queue(maxsize=30 * bps)
        
        # create decoder for plant 
        self.decoder = self._create_decoder()
        
        if train_online:
            print("[Error] online train is not implemented yet")
        else:
            data = sio.loadmat(os.path.join(global_config.assets_dir, "TRAIN300.mat"))["data"]
            self.decoder.train(data[1])
            

    # speak 
    def speak(self, x):
        pass

    # decode 
    def message(self, x):
        return self.decoder.decode(x)
        
    def display(self, x):
        pass

    """
    Desc: Given string, generator a signal 
    Params:
        y: list of string
    Return:
        z: int
    """
    def gen_signal(self, y, min_, max_):
        zz = [yyy for yyy in yy.encode("utf8") for yy in y]
        z = sum(zz)
        # scale z
        z = min_ + z % (max_ - min_)
        return z

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
    
    def _stableize_sensor(self, n_step_1 = 10, n_step_2 = 10):
        print("[Info] start to stablize sensor, please wait")
        n_valid = 0
        for i in range(n_step_1):
            self.ser.readline();
            
        for i in range(n_step_2):
            raw = self.ser.readline();
            raw = raw.strip()
            if raw.isdigit():
                n_valid += 1
                
        if n_valid == n_step_2:
            print("[Info] stablize sensor succeed")
        else:
            print("[Warning] stablize sensor with %d/%d (valid/total)" % (n_valid, n_step_2))
    
    def _get_sample_rate(self, n_second=10):
        total_time = 0.0
        total_samples = 0 
        for _ in range(n_second):
            t0 = time.time()
            raw = self.ser.read(self.bps)
            if len(raw) >= self.bps:
                print("[Warning] too many bytes(exceed bps: %d) send from Arduino UNO!" % self.bps)
            t1 = time.time()
            total_time += (t1 - t0)
            total_samples += len(raw.split(b"\r\n"))

        sample_rate = int(total_samples / total_time)
        return sample_rate
        
    def _create_decoder(self):
        decoder = Decoder(languages = global_config.languages, 
                vocab_dir = global_config.vocab_dir, 
                sample_rate = self.sample_rate, 
                hop_size = self.hop_size, 
                window_size = self.window_size)
        
        
        
    
    def start(self):
        # start a background thread to recieve data from sensor
        self.recieve_thread = threading.Thread(target=Plant._recieve_data, args=(self,))
        self.recieve_thread.start()