# -*- coding:utf-8 -*-
import pyaudio
import matplotlib.pyplot as plt
import numpy as np
import wave
import struct

p = pyaudio.PyAudio()
for index in range(0, p.get_device_count()):
    print(p.get_device_info_by_index(index))



def savewav(sig,sk):
    RATE = 44100 #サンプリング周波数
    #サイン波を-32768から32767の整数値に変換(signed 16bit pcmへ)
    swav = [(int(32767*x)) for x in sig] #32767
    #バイナリ化
    binwave = struct.pack("h" * len(swav), *swav)
    #サイン波をwavファイルとして書き出し
    w = wave.Wave_write("./record_data/"+str(sk)+".wav")
    params = (1, 2, RATE, len(binwave), 'NONE', 'not compressed')
    w.setparams(params)
    w.writeframes(binwave)
    w.close()
    
RATE=44100
p=pyaudio.PyAudio()
N=100
CHUNK=1024*N
stream=p.open(format = pyaudio.paInt16,
        channels = 1,
        rate = RATE,
        frames_per_buffer = CHUNK,
        input = True,
        output = True,
        input_device_index = 11
        ) # inputとoutputを同時にTrueにする

sk=0
while stream.is_active():
    input = stream.read(CHUNK, exception_on_overflow = False)
    print(len(input))
    sig =[]
    sig = np.frombuffer(input, dtype="int16") / 32768
    savewav(sig,sk)
    fig, (ax1,ax2) = plt.subplots(2,1,figsize=(1.6180 * 4, 4*2))
    lns1=ax1.plot(sig[0:1024] ,".-",color="red")
    ax1.set_xticks(np.linspace(0, 882, 3))
    ax1.set_ylabel("sig0")
    ax1.set_title('short plot')
    lns2=ax2.plot(sig[0:CHUNK], "-",color="blue")
    ax2.set_xticks(np.linspace(0, 44100*2, 5))
    ax2.set_ylabel("sig1")
    ax2.set_title('long plot')
    ax1.grid()
    ax2.grid()
    plt.pause(0.5)
    plt.savefig("./record_data/sound_{}.png".format(sk))
    plt.close()
    sk+=1
    output = stream.write(input)