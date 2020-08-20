#encoding=utf8
import time
import threading
import numpy as np
import sounddevice as sd

from queue import Queue

DATA_TYPE=np.float32
din, dout = sd.default.device



class Speaker(object):
    def __init__(self, sample_rate=2500):
        # config
        self.sample_rate = sample_rate
        self.blocking = True
        # input queue
        self.q = Queue(maxsize=30)
        # output 
        self.sd_output_stream = sd.OutputStream(self.sample_rate, channels=1, device=dout, dtype=DATA_TYPE)
        self.sd_output_stream.start()
        # background
        self._create_background()
        # speak thread
        self.speak_thread = threading.Thread(target=Speaker._speak, args=(self,))
        self.speak_thread.start()
        

    # 外部API
    def speak(self, x):
        if isinstance(x, list):
            x = np.array(x)
        if isinstance(x, np.ndarray):
            x = x.astype(DATA_TYPE)
        # 如果输入长度超过1秒钟的样本数，裁掉后面的
        if len(x.shape) == 1:
            if x.shape[0] > self.sample_rate:
                x = x[:self.sample_rate]
        #print(x.shape)
        self.q.put(x)

    # the real speak
    def _speak(self):
        while 1:
            if self.q.empty():
                #time.sleep(0.1)
                # if no signal input, then play 0.1 second background
                x = next(self.bg_generator)
            else:
                x = self.q.get()
            self.sd_output_stream.write(x)
    
    def _create_background(self, duration=0.1):
        fs = 44100 # Hz
        f = 440 # Hz
        length = 5 #s
        myarray = np.arange(fs * length)
        self.bg_amp = 0.005
        self.bg =  self.bg_amp * np.sin(2 * np.pi * f / fs * myarray).astype(DATA_TYPE)
        def _bg_generator():
            chunk_size = int(duration * fs)
            assert chunk_size < len(self.bg)
            b, e = 0, 0
            while 1:
                e = b + chunk_size
                if e > len(self.bg):
                    b, e = 0, chunk_size
                yield self.bg[b:e]
        self.bg_generator = _bg_generator()


def simple_test_speaker():
    fs = 44100 # Hz
    f = 440 # Hz
    length = 5 #s
    myarray = np.arange(fs * length)
    myarray = 0.005 * np.sin(2 * np.pi * f / fs * myarray).astype(DATA_TYPE)
    speaker = Speaker(sample_rate=fs)
    for _ in range(5):
        speaker.speak(myarray)
    speaker.speak_thread.join()

def test_plant_speak():
    speaker = Speaker(sample_rate=2500)
    import os
    import numpy as np
    from src.global_config import global_config
    fn = "plant_no_wind_signal.txt"
    f = open(os.path.join(global_config.assets_dir, fn))
    s  = f.readlines()
    f.close()
    s = [[int(x) for x in l.strip().split()] for l in s]
    for l in s:

        l = (np.array(l) - 300) / 660.0
        l = l.astype(DATA_TYPE)
        speaker.speak(l)
    speaker.speak_thread.join()

if __name__ == "__main__":
    #test_plant_speak()
    simple_test_speaker()
