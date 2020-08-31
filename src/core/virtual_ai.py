#encoding=utf8
import time
import numpy as np

from src.core.nn import MLP
from src.core.decoder import LinearMapper, read_vocab, print_message
from src.core.visualizer import Visualizer, get_full_screen_size
from src.core.speaker import Speaker
from src.global_config import global_config

class VirtualAI(object):
    def __init__(self, vocab_dir=global_config.vocab_dir, languages=global_config.languages):
        self.vocab_dir = vocab_dir
        self.languages = languages
        
        # 声音
        self.acoustic_size = 2500
        self.acoustic_model = MLP(hidden_layer_sizes=self.acoustic_size, activation="identity")
        self.init_acoustic_model()
        # 文字
        self.vocabs, self.vocab_lsts = read_vocab(self.vocab_dir, self.languages)

        self.train()
        
        self.vis = Visualizer(name="AI", left_loc=0, top_loc=0, width=320, height=240, predefined_loc="right-top")

        self.speaker = Speaker(5000, global_config.ai_acoustic_out_device)

        
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
            y = self._generator_respond(x, lang)
            ys[lang] = y
        return ys
            
    """
    Desc: generate ai's acoustic respond
    Params:
        x: np.ndarray
    Return:
        y: np.ndarray
    """ 
    def acoustic_respond(self, x):
        assert x.ndim == 1
        input_size = x.shape[0]
        if input_size < self.acoustic_size:
            x = np.pad(x, (0, self.acoustic_size - input_size), mode="constant")
        elif input_size > self.acoustic_size:
            x = x[:self.acoustic_size]
        
        x = x.reshape([1, -1])
        y = self.acoustic_model.predict(x)
        y = y.reshape([-1])
        
        if input_size < self.acoustic_size:
            y = y[:input_size]

        return y
        
    """
    Desc: Given string, generator a signal 
    Params:
        responds: 
    Return:
        z: int
    """
    def gen_signal(self, responds, min_, max_):
        signal = 0
        for lang, sentence in responds.items():
            for word in sentence:
                signal += sum([ord(y) for y in word])
        
        # scale z
        signal = min_ + signal % (max_ - min_)
        return signal
        
        
    
    """
    Desc: train a virtual AI by simple shift vocab
    """
    def train(self):
        self.mapper = {}
        for lang in self.languages:
            vocab = list(self.vocabs[lang].keys())
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
        
    def init_acoustic_model(self):
        X = np.random.rand(1, 2500)
        Y = np.random.rand(1, 2500)
        self.acoustic_model.fit(X, Y)

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

if __name__ == "__main__":
    virtual_ai = VirtualAI()