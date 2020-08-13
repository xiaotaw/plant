#!/usr/bin/env python
# encoding=utf8
# try to read ECG10002464 data
import os.path as path
import numpy as np
from numpy import fft
from scipy import io as sio
import matplotlib.pyplot as plt


data_dir = "/data/DATASETS/medical/ECG10002464/TRAIN/"
data = sio.loadmat(path.join(data_dir + "TRAIN300.mat"))["data"]

fig = plt.figure()
for i in range(data.shape[0]):
    plt.subplot(3, 4, 1 + i)
    plt.hist(data[i, :], bins=50)
    
    sample_rate = 500         # 采样频率
    window_size = sample_rate * 1  # 每次分析步骤所需的sample数，设置为2秒的采样数
    hop_size = int(window_size / 2)   # 两个相邻窗口之间错开的sanple数

    total_length = data.shape[1]

    for offset in range(0, total_length, hop_size):
        x = data[i][offset: offset + window_size]
        print(len(x))
        fft_y = fft.fft(x, window_size)
        abs_y = np.abs(fft_y)
        angle_y = np.angle(fft_y)

        fig3 = plt.figure(figsize=(10,8))
        # draw x
        plt.subplot(3, 1, 1)
        plt.plot(x)
        # draw freq spectrum
        plt.subplot(3, 1, 2)
        plt.plot(abs_y)
        # draw phase
        plt.subplot(3, 1, 3)
        plt.plot(angle_y)

        plt.show()
    break