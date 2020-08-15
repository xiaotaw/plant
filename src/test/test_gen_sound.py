import wave
import numpy as np
import struct
import matplotlib.pyplot as plt
import math
import ctypes
#from compiler.ast import flatten
 
def calculate_db(xdb):
    #db = 0
    print ("math.pow(10, -12/20) : ", math.pow(10, -12/20)) # 0.251188643150958
    print ("math.pow(10, -6/20) : ", math.pow(10, -6/20)) #0.5011872336272722
    print ("math.pow(10, -3/20) : ", math.pow(10, -3/20)) #0.7079457843841379
    print ("math.pow(10, -1/20) : ", math.pow(10, -1/20)) #0.8912509381337456
    print ("math.pow(10, 0/20) : ", math.pow(10, 0/20)) #1.0
    print ("math.pow(10, 1/20) : ", math.pow(10, 1/20)) #1.1220184543019633
    print ('math.pow(10, 3/20) : ', math.pow(10, 3/20)) #1.4125375446227544
    print ('math.pow(10, 6/20) : ', math.pow(10, 6/20)) #1.9952623149688795
    print ('math.pow(10, 9/20) : ', math.pow(10, 9/20)) #2.8183829312644537
    print ('math.pow(10, 12/20) : ', math.pow(10, 12/20)) #3.9810717055349722
    db = math.pow(10, xdb/20)
    return db
 
def generial_sinwav(samplerate,ch_num,bytes_width,xdb,sinwav_freq_l,sinwav_freq_r,duration):
    # volume x_db
    db_v = -3
    db = math.pow(10, -3/20)
    db = xdb
    # sample/every second
    framerate = samplerate
    # channel_num
    channel_num = ch_num
    # bytes needed every sample
    sample_width = bytes_width
    bits_width = sample_width*8
    # seconds, long of data
    duration = duration
    # frequeny of sinewave
    sinewav_frequency_l = sinwav_freq_l
    sinewav_frequency_r = sinwav_freq_r
    # max value of samples, depends on bits_width
    max_val = 2**(bits_width-1) - 1
    print ('max_val : ', max_val)
    #volume = 32767*db #0x7FFF=32767
    volume = max_val*db #2**(bits_width-1) - 1
    #多个声道生成波形数据
    x = np.linspace(0, duration, num=int(duration*framerate))
    y_l = np.sin(2 * np.pi * sinewav_frequency_l * x) * volume
    y_r = np.sin(2 * np.pi * sinewav_frequency_r * x) * volume
    # 将多个声道的波形数据转换成数组
    y = zip(y_l,y_r)
    ##print("zip y", y)
    y = list(y)
    ##print("list y",y)
    y = np.array(y,dtype=np.int)
    ##print("array y",y)
    y = y.reshape(-1)
    ##print("reshap array y",y)
##    plt.subplot(122)
##    plt.plot(x, y_l, color='r', linestyle='-', marker='+')
##    plt.show()
 
    # 最终生成的一维数组
    sine_wave = y
    print("type(sine_wave)=",type(sine_wave))
 
    #data = struct.pack('<i', int(y[2]))
    #print(data)
    # wav file_name
    file_name = "sine_"+str(framerate)+"_"+str(channel_num)+"ch_"+str(bits_width)+"bits_"+str(db_v)+"db"
    file_name += "_l"+str(sinewav_frequency_l)+"_r"+str(sinewav_frequency_r)+"_"+str(duration)+"s.wav"
    print ('file_name: ', file_name)
    #open wav file
    wf = wave.open(file_name, 'wb')#wf = wave.open("sine.wav", 'wb')
    wf.setnchannels(channel_num)
    wf.setframerate(framerate)
    wf.setsampwidth(sample_width)
    #if (sample_width == 3):
    #    wf.setsampwidth(sample_width+1)
    for v in sine_wave:
        if (sample_width == 4):
            data = struct.pack('<l', int(v))
        elif (sample_width == 3):
            #data = struct.pack('<l', int(v*2**8))
            d = int(v)
            dc = getComplement_24bits(d)
            data = dc.to_bytes(3,'little')
        elif (sample_width == 2):
            data = struct.pack('<h', int(v))
        elif (sample_width == 1):    
            d = int(v)
            dc = getComplement_8bits(d)
            data = dc.to_bytes(1,'little')
            #data = struct.pack('<c', chr(dc)) #error
        else:
            data = struct.pack('<b', int(v))
 
        print("%x"%(v), data)
        wf.writeframesraw(data)
    #print(struct.pack('<i', int(y[2])))
    #print(struct.pack('<i', int(y[4])))
    wf.close()
 
def getComplement_24bits(v): #求24bis数据的补码
    v_int = int(v)
    if (v_int >= 0):
        print('param is positive')
        return v_int
    c  = (-1)*v
    c  = ~c + 1
    c &= 0xFFFFFF
    c |= 0x800000 
    return c
 
def getComplement_8bits(v): #求8bis数据的补码
    v_int = int(v)
    if (v_int >= 0):
        print('param is positive')
        return v_int
    c  = (-1)*v
    c  = ~c + 1
    c &= 0xFF
    c |= 0x80
    return c
 
def main():
 
    # volume x_db
    db_v = -3
    db = math.pow(10, -3/20)
    db = calculate_db(db_v)
    # sample/every second
    framerate = 44100
    # channel_num
    channel_num = 2
    # bytes needed every sample
    sample_width = 2
    bits_width = sample_width*8
    # seconds, long of data
    duration = 88200/framerate
    # frequeny of sinewave
    sinewav_frequency_l = 1000
    sinewav_frequency_r = 2000
 
    if sample_width not in [1,2,3,4]: ##[1,3]has some errors
        return 0
    generial_sinwav(framerate,channel_num,sample_width,db, sinewav_frequency_l, sinewav_frequency_r, duration)
    v = -0x41aa
    print("test:%x"%(v), struct.pack('<h', int(v)))
    v = -54
    print("test:%x"%(v), struct.pack('<b', int(v)))
    v = -0x6a1aa
    print("test:%x"%(v), struct.pack('<i', int(v)))
    return 0
    
main()
