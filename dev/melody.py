from lib.wave import *

def waves():
    l = int(44100*0.4) # each note lasts 0.4 seconds

    return cycle(chain(ncycles(chain(islice(damped_wave(frequency=440.0, amplitude=0.1, length=int(l/4)), l),
                                     islice(damped_wave(frequency=261.63, amplitude=0.1, length=int(l/4)), l),
                                     islice(damped_wave(frequency=329.63, amplitude=0.1, length=int(l/4)), l)), 3),
                       islice(damped_wave(frequency=440.0, amplitude=0.1, length=3*l), 3*l),

                       ncycles(chain(islice(damped_wave(frequency=293.66, amplitude=0.1, length=int(l/4)), l),
                                     islice(damped_wave(frequency=261.63, amplitude=0.1, length=int(l/4)), l),
                                     islice(damped_wave(frequency=293.66, amplitude=0.1, length=int(l/4)), l)), 2),
                       chain(islice(damped_wave(frequency=293.66, amplitude=0.1, length=int(l/4)), l),
                             islice(damped_wave(frequency=329.63, amplitude=0.1, length=int(l/4)), l),
                             islice(damped_wave(frequency=293.66, amplitude=0.1, length=int(l/4)), l)),
                       islice(damped_wave(frequency=261.63, amplitude=0.1, length=3*l), 3*l)))

def play():
    channels = ((waves(),), (waves(), white_noise(amplitude=0.001),))
    samples = compute_samples(channels, None)
    write_wavefile("tmp.wav", samples, None)


if __name__ == "__main__":
    play()