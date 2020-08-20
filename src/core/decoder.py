#!/usr/bin/env python
# encoding=utf8
import re
import codecs
import numpy as np

from os import path
from numpy import fft
from collections import OrderedDict
from collections import defaultdict


""" Desc: read vocabulary
"""
def read_vocab(vocab_dir, languages):
    vocabs = {}
    vocab_lsts = {}
    vocab_res = {"zh": re.compile("[^A-Za-z]")}
    vocab_filter = dict([(lang, lambda x: len(vocab_res[lang].findall(x)) != 0) for lang in vocab_res])
    for lang in languages:
        vocab_filename = path.join(vocab_dir, lang + "_vocab.txt")
        with codecs.open(vocab_filename, "r", encoding="utf8") as f:
            vocab = OrderedDict()
            for l in f:
                word, freq = l.strip().split()
                if lang in vocab_filter:
                    if vocab_filter[lang](word):
                        vocab[word] = np.log(1 + int(freq))
                    else:
                        #print(word + " not used")
                        pass
                else:
                    vocab[word] = np.log(1 + int(freq))
            vocabs[lang] = vocab
            vocab_lsts[lang] = list(vocab.keys())
    return vocabs, vocab_lsts

class LinearMapper(object):
    """ x_y should be sorted in decreaseing order by y
    """
    def __init__(self, x_y_1, x_y_2):
        ys_1 = np.array([y1 for x1, y1 in x_y_1])
        ys_2 = np.array([y2 for x2, y2 in x_y_2])
        self.y1_min = ys_1.min()
        self.y1_max = ys_1.max()
        self.y2_min = ys_2.min()
        self.y2_max = ys_2.max()
        self.scale = (self.y2_max - self.y2_min) / (self.y1_max - self.y1_min + 1e-7)
        self.build_mapper(ys_1, ys_2)
        #
        self.length_1 = len(ys_1)
        self.length_2 = len(ys_2)
    
    
    """ Given the mapper from y1 to y2, find the map from x1 to x2. 
       i.e. y1 = f(x1), y2 = g(x2); find h with repect to x2 = h(x1), s.t. y1 = y2
    """
    def build_mapper(self, ys_1, ys_2):
        b_idx, m_idx, e_idx = 0, 0, 0
        b_value, e_value = 0.0, 0.0
        idx_lst = []
        epsilon = 1e-6
        for i, y1 in enumerate(ys_1):
            # Given y1, predict the corresponding y2_hat
            y2_hat = (y1 - self.y1_min) * self.scale + self.y2_min
            for idx in range(b_idx, len(ys_2)):
                if y2_hat - ys_2[idx] > epsilon:
                    e_idx = idx 
                    b_value, e_value = ys_2[b_idx], ys_2[e_idx]
                    assert (e_idx == b_idx + 1)
                    # linear interpolation
                    m_idx = b_idx + (y2_hat - b_value) / (e_value - b_value + 1e-7)
                    break
                elif np.abs(y2_hat - ys_2[idx]) <= epsilon:
                    b_idx = m_idx = e_idx = idx 
                    b_value = e_value = ys_2[idx]
                    break
                else:
                    assert (y2_hat - ys_2[idx] < -epsilon)
                    b_idx = idx
            idx_lst.append(m_idx)
            if m_idx == 0:
                print("m_idx == 0")
            if idx == len(ys_2):
                print("meet end!")
        # 由于ys_2中长尾效应中的小数值(np.log(2))均相等，可能导致长尾均未被覆盖，
        # 解决方案：手动添加一个额外的idx，并在map函数中添加perturbation，对idx映射进行扰动
        idx_lst.append(len(ys_2))
        self.idx_lst = idx_lst

    """ Given index x1, and perturbation p, compute x2
    """
    def map(self, x1, p):
        assert (0 <= x1 < self.length_1), "invalid index: %d" % x1
        assert (0 <= p <= 1), "invalid perturbation: %f" % p
        x2_hat, x2_next = self.idx_lst[x1], self.idx_lst[x1 + 1]
        
        # perturbate
        x2_hat = x2_hat + p * (x2_next - x2_hat)
        x2_hat = int(x2_hat)
        # make sure that x2_hat is a valid index
        x2_hat = x2_hat % self.length_2
        return x2_hat
        

def print_message(message):
    for lang, words in message.items():
        if lang == "zh":
            sep = ""
        else:
            sep = " "
        words = sep.join(words)
        print("%s: %s" % (lang, words))

class Decoder(object):
    # 
    def __init__(self, languages, vocab_dir, sample_rate, hop_size, window_size):
        # language 
        self.languages = languages
        self.vocab_dir = vocab_dir
        
        self.vocabs, self.vocab_lsts = read_vocab(self.vocab_dir, self.languages)
        # singal 
        self.sample_rate = sample_rate
        self.hop_size = hop_size
        self.window_size = window_size
        
    
    """ Desc: unsupervised training a decoder of a specifical kind of input signal `x`
        Params:
            x: input signal
            languages: the target languages which we want decode `x` into 
    """
    def train(self, x):
        # stats of x
        average_abs_ys = []
        for offset in range(0, len(x), self.hop_size):
            fft_x = x[offset: offset + self.window_size]
            fft_y = fft.fft(fft_x, self.window_size)
            average_abs_ys.append(np.abs(fft_y))
        average_abs_y = np.stack(average_abs_ys, axis=0).mean(axis=0)
        self.log_average_abs_y = np.log(1 + average_abs_y)
        
        # sort freq by Amplitude
        self.log_freqs = list(enumerate(self.log_average_abs_y))
        self.log_freqs.sort(key=lambda x: x[1], reverse=True)
        self.reverse_index = {}
        for i, (freq, amp) in enumerate(self.log_freqs):
            self.reverse_index[freq] = i
            
        # mapping from x to vocab
        self.mappers = {}
        for lang in self.languages:
            vocab = list(self.vocabs[lang].items())
            self.mappers[lang] = LinearMapper(self.log_freqs, vocab)
                    
                
                
    
    def decode(self, x, languages=None, max_length=3000):
        words = defaultdict(list)
        for offset in range(0, len(x), self.hop_size):
            fft_x = x[offset: offset + self.window_size]
            fft_y = fft.fft(fft_x, self.window_size)
            abs_y = np.abs(fft_y)
            angle_y = np.angle(fft_y)
            # decode时，需生成随机数(0,1)，小于rate，才进行一次采样，类似于蒙特卡罗模拟
            norm_y = abs_y / self.window_size
            rates = norm_y / np.sqrt(self.window_size + norm_y.sum())
            #print("\nrate: max: %d, sum: %d, size: %d, rate mean: %f\n" % (max(norm_y), norm_y.sum(), len(rates), rates.mean()))
            
            if languages is None:
                languages = self.languages
            for lang in languages:
                if lang not in self.languages:
                    print("[Warning]: %s is not trained, but try to decode" % lang)
                    continue
                for i, (amp, phase, rate) in enumerate(zip(abs_y, angle_y, rates)):
                    # 类似于蒙特卡罗模拟
                    if np.random.random() > rate:
                        continue
                    x1 = self.reverse_index[i]
                    p = (phase + np.pi) / (2 * np.pi)
                    x2 = self.mappers[lang].map(x1, p)
                    word = self.vocab_lsts[lang][x2]
                    words[lang].append(word)
        for lang in languages:
            # truncate too long sentences
            if len(words[lang]) > max_length:
                words[lang] = words[lang][:max_length]
        return words
    

    