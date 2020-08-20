#!/usr/bin/env python
import sys
import numpy as np
from os import path
from scipy import io as sio
import matplotlib.pyplot as plt

pwd = path.split(path.realpath(__file__))[0]
p = path.split(pwd)[0]
sys.path.append(p)

from src.global_config import global_config
from src.core.decoder import Decoder

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
    

decoder = Decoder(languages = global_config.languages, 
                vocab_dir = global_config.vocab_dir, 
                sample_rate = 5000, 
                hop_size = 500, 
                window_size = 1000)


data = sio.loadmat(path.join(global_config.assets_dir, "TRAIN300.mat"))["data"]
x = data[1]

decoder.train(x)
y = decoder.decode(x)
for lang in decoder.languages:
    print(y[lang])
    
#draw_singal_freq_spec(decoder, data[1])
