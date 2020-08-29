# encoding:utf-8
import wave
import numpy as np
import sounddevice as sd



fs = 44100 # Hz
f = 440 # Hz
length = 5 #s
myarray = np.arange(fs * length)
myarray = np.sin(2 * np.pi * f / fs * myarray).astype(np.float32)

sd.play(myarray, blocking=True)

out = sd.OutputStream(fs,channels=1, device=3, dtype=np.float32)
out.start()
out.write(myarray)


import time
time.sleep(5)