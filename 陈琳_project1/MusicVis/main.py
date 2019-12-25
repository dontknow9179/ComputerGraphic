import pyaudio
import wave
import math
import numpy as np
import pygame
import time
from pygame.locals import *


CHUNK = 1024
wf = wave.open("ACCA13.wav", 'rb')
p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)
window_height = 450
window_width = 850

pygame.init()
pygame.display.set_caption('实时频域')
screen = pygame.display.set_mode((window_width, window_height), 0, 32)

data = wf.readframes(CHUNK)
while data != '':
    # 播放缓冲流的音频
    stream.write(data)
    # 清空屏幕
    screen.fill((0, 0, 0))
    # 防止程序无响应
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    # 把data由字符串以十六进制的方式转变为数组
    numpydata = np.fromstring(data, dtype=np.int16)
    # 傅里叶变换获取实数部分
    freqarray = np.real(np.fft.fft(numpydata))
    # 设置间隔区
    count = 5
    # 从频域中的2048个数据中每隔count个数据中选取一条
    for n in range(0, freqarray.size, count):
        height = abs(int(freqarray[n]/10000)) / 2
        R = abs(math.sin(time.time())) * 255
        G = abs(math.sin(3*time.time())) * 255
        B = abs(math.sin(2*time.time())) * 255
        pygame.draw.rect(screen, (R, G, B), Rect((20*n/count, window_height/2), (15, -height)))  # 画矩形
        pygame.draw.rect(screen, (R, G, B), Rect((20*n/count, window_height/2), (15, height)))
    pygame.display.update()
    data = wf.readframes(CHUNK)


stream.stop_stream()
stream.close()
p.terminate()
