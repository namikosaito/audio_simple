# -*- coding:utf-8 -*-
import pyaudio
import matplotlib.pyplot as plt
import numpy as np
import wave
import struct
import cv2

p = pyaudio.PyAudio()
for index in range(0, p.get_device_count()):
    print(p.get_device_info_by_index(index))


RATE=44100
p=pyaudio.PyAudio()
# CHUNK=1024*N  # CHUNK / RATE (sec)
CHUNK = 882
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

def image_drawing(sensor_value):
    image = np.full((300, 600, 3), 255, dtype=np.uint8)
    # plot
    cv2.circle(image, (200,150), 2, (255, 0, 0), 3)
    cv2.circle(image, (400,150), 2, (255, 0, 0), 3)
    cv2.circle(image, (200,150), 2, (255, 0, 0), int(sensor_value[0]*20))
    cv2.circle(image, (400,150), 2, (255, 0, 0), int(sensor_value[1]*20))
    cv2.imshow("Image", image)
    cv2.waitKey(10) 

sk=0
while stream_1.is_active() and stream_2.is_active():
    input_1 = stream_1.read(CHUNK, exception_on_overflow = False)
    input_2 = stream_2.read(CHUNK, exception_on_overflow = False)
    # print(len(input_1))
    sig_1 = []
    sig_2 = []
    sig_1 = np.frombuffer(input_1, dtype="int16") / 32768
    sig_2 = np.frombuffer(input_2, dtype="int16") / 32768
    sk+=1
    print(sum(sig_1[0:CHUNK]), sum(sig_2[0:CHUNK]))
    image_drawing([sum(sig_1[0:CHUNK]), sum(sig_2[0:CHUNK])])
    # output = stream_1.write(input_1)