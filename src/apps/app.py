#!/usr/bin/env python
#encoding=utf8
import numpy as np
from src.core.plant import Plant
from src.core.virtual_ai import VirtualAI
from src.core.decoder import print_message


plant = Plant()
virtual_ai = VirtualAI()

plant.start()

while 1:
    x = plant.q.get()
    x = plant._parse_data(x)
    print("%6d" % len(x), end="\t")
    # speak
    x_ = ((np.array(x) - 300) / 600.0).astype(np.float32)
    x_ = np.clip(x_, -0.8, 0.8)
    plant.speaker.speak(x_)
    # message
    message = plant.decoder.decode(x)
    print_message(message, end="\t")
    # display
    plant.vis.draw(x)
    # control signal
    control_signal = plant.gen_signal(x, min_=0, max_=5)
    print(control_signal)

    # 植物文字信息message传递给虚拟AI，虚拟AI生成回复respond
    ai_respond = virtual_ai.respond(message)
    print_message(ai_respond, end="\t")
    #
    ai_acoustic = virtual_ai.speak(x_)
    plant.speaker.speak(ai_acoustic.astype(np.float32))
    virtual_ai.vis.draw(ai_acoustic)
    # 虚拟AI的基于自身的respond，生成控制信号control_signal
    ai_control_signal = virtual_ai.gen_signal(ai_respond, min_=0, max_=5)
    
    print(ai_control_signal)

