#encoding=utf8
import time
import numpy as np
from src.core.decoder import LinearMapper, read_vocab


class VirtualAI(object):
    def __init__(self, vocab_dir, languages):
        self.vocab_dir = vocab_dir
        self.languages = languages
        
        self.vocabs, self.vocab_lsts = read_vocab(self.vocab_dir, self.languages)
        
        self.train()
        
    """
    Desc: Given input message, respond a message
    Params:
        x: dict of list of string 
    Return:
        y: dict of list of string
    """
    def respond(self, xs):
        ys = {}
        for lang, x in xs.items():
            y = self._generator_respond(x)
            ys[lang] = y
        return ys
            
    """
    Desc: Given string, convert to a sound array
    Params:
        y: list of string
    Return:
        y: np.ndarray
    """ 
    def speak(self, y):
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
        
        
    
    """
    Desc: train a virtual AI by simple shift vocab
    """
    def train(self):
        self.mapper = {}
        for lang in self.languages:
            vocab = self.vocabs[lang]
            length = len(vocab)
            
            # fixed basic shift
            index_x = np.arange(length)
            np.random.seed(0)
            shift_ratio = np.random.rand(length) 
            shift = (shift_ratio * length).astype(int)
            
            # random gaussion shift with mean = 0, std = 10
            np.random.seed(int(time.time()))
            g_shift = np.random.normal(scale=10, size=length).astype(int)
            
            # shift index
            index_y = (index_x + shift + g_shift) % length
            
            m = dict([(vocab[index_x[i]], vocab[index_y[i]]) for i in range(length)])
            self.mapper[lang] = m
    
    """
    Desc: given x, generator a respond for a language
    Params:
        x: list of string
    Return:
        y: list of string
    """
    def _generator_respond(self, x, lang):
        y = [self.mapper[lang][xx] for xx in x]
        return y
    