import sys
import wave
import math
import struct
import random
from itertools import *

# needs rewrite for python3

def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)


def ncycles(iterable, n):
    "Returns the sequence elements n times"
    return chain.from_iterable(repeat(tuple(iterable), n))


def sine_wave(frequency=440.0, framerate=44100, amplitude=0.5):
    '''
    Generate a sine wave at a given frequency of infinite length.
    '''
    period = int(framerate / frequency)
    if amplitude > 1.0: amplitude = 1.0
    if amplitude < 0.0: amplitude = 0.0
    lookup_table = [float(amplitude) * math.sin(2.0*math.pi*float(frequency)*(float(i%period)/float(framerate))) for i in range(period)]
    return (lookup_table[i%period] for i in count(0))


def square_wave(frequency=440.0, framerate=44100, amplitude=0.5):
    for s in sine_wave(frequency, framerate, amplitude):
        if s > 0:
            yield amplitude
        elif s < 0:
            yield -amplitude
        else:
            yield 0.0


def damped_wave(frequency=440.0, framerate=44100, amplitude=0.5, length=44100):
    if amplitude > 1.0: amplitude = 1.0
    if amplitude < 0.0: amplitude = 0.0
    return (math.exp(-(float(i%length)/float(framerate))) * s for i, s in enumerate(sine_wave(frequency, framerate, amplitude)))


def white_noise(amplitude=0.5):
    '''
    Generate random samples.
    '''
    return (float(amplitude) * random.uniform(-1, 1) for i in count(0))


def compute_samples(channels, nsamples=None):
    '''
    create a generator which computes the samples.

    essentially it creates a sequence of the sum of each function in the channel
    at each sample in the file for each channel.
    '''
    return islice(zip(*(map(sum, zip(*channel)) for channel in channels)), nsamples)


def write_wavefile(filename, samples, nframes=None, nchannels=2, sampwidth=2, framerate=44100, bufsize=2048):
    "Write samples to a wavefile."
    if nframes is None:
        nframes = -1

    w = wave.open(filename, 'w')
    w.setparams((nchannels, sampwidth, framerate, nframes, 'NONE', 'not compressed'))

    max_amplitude = float(int((2 ** (sampwidth * 8)) / 2) - 1)

    # split the samples into chunks (to reduce memory consumption and improve performance)
    for chunk in grouper(bufsize, samples):
        frames = "".join("".join(struct.pack("h", int(max_amplitude * sample)) for sample in channels) for channels in chunk if channels is not None)
        w.writeframesraw(frames)

    w.close()

    return filename


# def write_pcm(f, samples, sampwidth=2, framerate=44100, bufsize=2048):
#     "Write samples as raw PCM data."
#     max_amplitude = float(int((2 ** (sampwidth * 8)) / 2) - 1)
#     # split the samples into chunks (to reduce memory consumption and improve performance)
#     for chunk in grouper(bufsize, samples):
#         frames = ''.join(''.join(struct.pack('h', int(max_amplitude * sample)) for sample in channels) for channels in chunk if channels is not None)
#         f.write(frames)
#     f.close()
#     return filename


def wave_run(frequency, amplitude, filename="tmp.wav", channels=2, bits=16, rate=44100, time=60):
    """
        amplitude :: amplitude of the wave on a scale of 0.0-1.0.
        frequency :: frequency of the wave in Hz
        channels :: number of channels to produce
        bits :: number of bits in each sample
        rate :: sample rate in Hz
        time :: duration of the wave in seconds
        filename :: the file to generate
    """
    # Synth function 
    channels = ((sine_wave(frequency, rate, amplitude),) for i in range(channels))
    samples = compute_samples(channel, rate*time)
    # Write wav file
    write_wavefile(filename, samples, rate*time, channels, bits/8, rate)
    # Play wav file and delete it when done

