#!/usr/bin/env python
#encoding=utf8
import os

class Config(object):
    def __init__(self):
        # language
        self.languages = ["en", "zh"]
        # TODO: 替换成相对文件的路径
        self.vocab_dir = "/home/xt/Desktop/parttime_projects/plant/src" 
        # singal 
        self.sample_rate = 500
        self.hop_size = 250
        self.window_size = self.sample_rate * 1