# -*- coding:utf-8 -*-
import pyaudio
import matplotlib.pyplot as plt
import numpy as np
import wave
import struct

p = pyaudio.PyAudio()
for index in range(0, p.get_device_count()):
    print(p.get_device_info_by_index(index))



def savewav(sig,sk,mic_no):
    RATE = 44100 #サンプリング周波数
    #サイン波を-32768から32767の整数値に変換(signed 16bit pcmへ)
    swav = [(int(32767*x)) for x in sig] #32767
    #バイナリ化
    binwave = struct.pack("h" * len(swav), *swav)
    #サイン波をwavファイルとして書き出し
    w = wave.Wave_write("./record_data/mic"+str(mic_no)+"_"+str(sk)+".wav")
    params = (1, 2, RATE, len(binwave), 'NONE', 'not compressed')
    w.setparams(params)
    w.writeframes(binwave)
    w.close()
    
RATE=44100
p=pyaudio.PyAudio()
N=100
CHUNK=1024*N  # CHUNK / RATE (sec)
stream_1=p.open(format = pyaudio.paInt16,
        channels = 1,
        rate = RATE,
        frames_per_buffer = CHUNK,
        input = True,
        output = True,
        input_device_index = 10
        ) # inputとoutputを同時にTrueにする

stream_2=p.open(format = pyaudio.paInt16,
        channels = 1,
        rate = RATE,
        frames_per_buffer = CHUNK,
        input = True,
        output = True,
        input_device_index = 11
        ) # inputとoutputを同時にTrueにする

sk=0
while stream_1.is_active() and stream_2.is_active():
    input_1 = stream_1.read(CHUNK, exception_on_overflow = False)
    input_2 = stream_2.read(CHUNK, exception_on_overflow = False)
    # print(len(input_1))
    sig_1 = []
    sig_2 = []
    sig_1 = np.frombuffer(input_1, dtype="int16") / 32768
    sig_2 = np.frombuffer(input_2, dtype="int16") / 32768
    savewav(sig_1,sk, mic_no=1)
    savewav(sig_2,sk, mic_no=2)
    fig, (ax1,ax2) = plt.subplots(2,1,figsize=(1.6180 * 4, 4*2))
    lns1=ax1.plot(sig_1[0:CHUNK] ,"-",color="red")
    ax1.set_xticks(np.linspace(0, 44100*2, 5))
    ax1.set_ylabel("sig1")
    ax1.set_title('mic 1')
    lns2=ax2.plot(sig_2[0:CHUNK], "-",color="blue")
    ax2.set_xticks(np.linspace(0, 44100*2, 5))
    ax2.set_ylabel("sig2")
    ax2.set_title('mic 2')
    ax1.grid()
    ax2.grid()
    plt.pause(0.5)
    plt.savefig("./record_data/sound_{}.png".format(sk))
    plt.close()
    sk+=1
    print(sig_1[0:10])
    # output = stream_1.write(input_1)