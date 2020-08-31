import os

class GlobalConfig(object):
    def __init__(self):
        self.src_dir = os.path.split(os.path.realpath(__file__))[0]
        self.assets_dir = os.path.join(self.src_dir, "assets")
        self.vocab_dir = self.assets_dir 
        self.languages = ["zh"]

global_config = GlobalConfig()

# 信号范围
global_config.plant_signal_min = 1
global_config.plant_signal_max = 5
global_config.ai_signal_min = 6
global_config.ai_signal_max = 10

# 音频输出设备(-1表示不进行指定，使用系统默认音频输出设备)
global_config.plant_acoustic_out_device = -1
global_config.ai_acoustic_out_device = -1

# osc 地址端口
global_config.osc_ip = "127.0.0.1"
global_config.osc_port = 10000
global_config.osc_filter = "/*"
