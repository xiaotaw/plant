#!/usr/bin/env python
#encoding=utf8
import numpy as np
from src.core.plant import Plant
from src.core.virtual_ai import VirtualAI
from src.core.decoder import print_message
from src.global_config import global_config


from pythonosc import udp_client
client = udp_client.SimpleUDPClient(global_config.osc_ip, global_config.osc_port)

plant = Plant()
virtual_ai = VirtualAI()
plant.start()

while 1:
    x = plant.q.get()
    x = plant._parse_data(x)
    #print("%6d" % len(x), end="\t")
    # 植物文字
    message = plant.decoder.decode(x)
    print_message(message, end="\t")
    # 控制信号control signal
    plant_control_signal = plant.gen_signal(x, min_=global_config.plant_signal_min, max_=global_config.plant_signal_max)
    print(plant_control_signal)
    # 植物声音
    x = np.array(x)
    x_ = ((x - x.mean()) / (np.abs(x).max() + 1e-9)).astype(np.float32)
    #x_ = np.clip(x_, -0.8, 0.8)
    # 声音大小缩放系数
    plant_acoustic_scale_ = (global_config.plant_signal_max - plant_control_signal) / (global_config.plant_signal_max - global_config.plant_signal_min)
    plant_acoustic_scale = 10 ** (-plant_acoustic_scale_)
    print("plant: %.3f" % plant_acoustic_scale)
    # 播放声音
    plant.speaker.speak((plant_acoustic_scale * x_).astype(np.float32))
    # display
    plant.vis.draw(x_)

    # 植物文字信息message传递给虚拟AI，虚拟AI生成回复respond
    ai_respond = virtual_ai.respond(message)
    print_message(ai_respond, end="\t")
    # 虚拟AI的基于自身的respond，生成控制信号control_signal
    ai_control_signal = virtual_ai.gen_signal(ai_respond, min_=global_config.ai_signal_min, max_=global_config.ai_signal_max)
    print(ai_control_signal)
    # 生成虚拟AI的声音
    ai_acoustic_respond = virtual_ai.acoustic_respond(x_)
    # 声音大小缩放系数
    ai_acoustic_scale_ = (global_config.ai_signal_max - ai_control_signal) / (global_config.ai_signal_max - global_config.ai_signal_min)
    ai_acoustic_scale = 10 ** (-ai_acoustic_scale_)
    print("ai: %.3f\n\n" % ai_acoustic_scale)
    # 播放声音
    virtual_ai.speaker.speak((ai_acoustic_scale * ai_acoustic_respond).astype(np.float32))
    # 画出声音的波形图
    virtual_ai.vis.draw(ai_acoustic_respond)
    

    # 发送osc信号
    if (plant_acoustic_scale_ > ai_acoustic_scale_):
        control_signal = plant_control_signal
    else:
        control_signal = ai_control_signal
    client.send_message(global_config.osc_filter, control_signal)

