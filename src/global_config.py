import os

class GlobalConfig(object):
    def __init__(self):
        self.src_dir = os.path.split(os.path.realpath(__file__))[0]
        self.assets_dir = os.path.join(self.src_dir, "assets")
        self.vocab_dir = self.assets_dir 
        self.languages = ["zh"]

global_config = GlobalConfig()