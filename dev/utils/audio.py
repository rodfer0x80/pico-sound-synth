import sys
import wave
import math
import struct
import random
import argparse
from itertools import *


# src :: https://zach.se/generate-audio-with-python/

def sine_wave(frequency=440.0, framerate=44100, amplitude=0.5):
    period = int(framerate / frequency)
    if amplitude > 1.0: amplitude = 1.0
    if amplitude < 0.0: amplitude = 0.0
    lookup_table = [float(amplitude) * math.sin(2.0*math.pi*float(frequency)*(float(i%period)/float(framerate))) for i in xrange(period)]
    return (lookup_table[i%period] for i in count(0))


def white_noise(amplitude=0.5):
    return (float(amplitude) * random.uniform(-1, 1) for _ in count(0))


# Binaural beat and background white noise :: https://en.wikipedia.org/wiki/Beat_(acoustics)#Binaural_beats
# white noise example :: create a period and cycle it to save computation since they will forever repeat
noise = cycle(islice(white_noise(), 44100))
# balanced melody
# channels = ((sine_wave(440.0),),
#             (sine_wave(440.0),))
# location control example :: (ch1,ch2)
# channels = ((sine_wave(440.0, amplitude=0.5),),
#             (sine_wave(440.0, amplitude=0.2),))
# location control example with white noise in the background
nchannels = 2
channels = ((sine_wave(200.0, amplitude=0.1), white_noise(amplitude=0.001)),
            (sine_wave(205.0, amplitude=0.1), white_noise(amplitude=0.001)))


def compute_samples(channels, nsamples=None):
    return islice(zip(*(map(sum, zip(*channel)) for channel in channels)), nsamples)


def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)


def write_wavefile(filename, samples, nframes=None, nchannels=2, sampwidth=2, framerate=44100, bufsize=2048):
    if nframes is None:
        nframes = -1

    w = wave.open(filename, 'w')
    w.setparams((nchannels, sampwidth, framerate, nframes, 'NONE', 'not compressed'))

    max_amplitude = float(int((2 ** (sampwidth * 8)) / 2) - 1)

    # split the samples into chunks (to reduce memory consumption and improve performance)
    for chunk in grouper(bufsize, samples):
        frames = ''.join(''.join(struct.pack('h', int(max_amplitude * sample)) for sample in channels) for channels in chunk if channels is not None)
        w.writeframesraw(frames)

    w.close()

    return filename


# filename = "tmp.wav"
# w = wave.open(filename, 'w')
# sampwidth = 2 # 16bit sound :: 2 bytes
# framerate = 44100 # number of samples per second :: 44100 ~ CD quality
# nframes = 1 # number of samples to write
# w.setparams((nchannels, sampwidth, framerate, nframes, 'NONE', 'not compressed'))
#
#
# max_amplitude = 32767.0 # audio encoded in bit integers
# samples = (int(sample * max_amplitude) for sample in samples)
#
#
# struct.pack('h', 1000) # f string for signed short
