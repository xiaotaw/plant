#!/usr/bin/env python
import numpy as np
from os import path
from scipy import io as sio
import matplotlib.pyplot as plt

import sys
sys.path.append("/home/xt/Desktop/parttime_projects/plant/src")
from config import Config
from decoder import Decoder

def show_vocab_freq(decoder):
    n_lang = len(decoder.languages)
    fig = plt.figure(num="log_freq of vocab")
    for i, lang in enumerate(decoder.languages):
        plt.subplot(n_lang, 1, 1 + i)
        log_freqs = np.array(list(decoder.vocabs[lang].values()))
        plt.xlabel(lang)
        plt.ylabel("log_freq")
        plt.plot(log_freqs)
    plt.show()

def draw_singal_freq_spec(decoder, x):
    decoder.train(x)
    fig = plt.figure(num="log_sum of signal freq spec")
    plt.plot(decoder.log_average_abs_y)
    plt.xlabel("freq")
    plt.ylabel("log_sum of Amplitude")
    plt.show()
    
    plt.plot(sorted(list(decoder.log_average_abs_y), reverse=True))
    plt.show()
    

config = Config()
config.languages = ["zh", "en"]
decoder = Decoder(config)
show_vocab_freq(decoder)

data_dir = "/data/DATASETS/medical/ECG10002464/TRAIN/"
data = sio.loadmat(path.join(data_dir + "TRAIN300.mat"))["data"]
x = data[1]

decoder.train(x)
y = decoder.decode(x)
for lang in decoder.languages:
    if lang == "zh":
        sep = ""
    else:
        sep = " "
    print(sep.join(y[lang]))
    
#draw_singal_freq_spec(decoder, data[1])
