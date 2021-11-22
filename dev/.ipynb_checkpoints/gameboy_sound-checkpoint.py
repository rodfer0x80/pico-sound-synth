# run locally (dev system)

from matplotlib.pylab import *
import re
import winsound

def play_melody(melody, sample_freq=10.e3, bpm=50):
    duration = re.compile("^[0-9]+")
    pitch = re.compile("[\D]+[\d]*") 
    measure_duration = 4 * 60. / bpm #usually it's 4/4 measures
    output = zeros((0,))
    for note in melody.split(','):
        # regexp matching
        duration_match = duration.findall(note)
        pitch_match = pitch.findall(note)
        
        # duration 
        if len(duration_match) == 0:
            t_max = 1/4.
        else:
            t_max = 1/float(duration_match[0])
        if "." in pitch_match[0]:
            t_max *= 1.5
            pitch_match[0] = "".join(pitch_match[0].split("."))
        t_max = t_max * measure_duration
        
        # pitch
        if pitch_match[0] == 'p':
            freq = 0
        else:
            if pitch_match[0][-1] in ["4", "5", "6", "7"]: # octave is known
                octave = ["4", "5", "6", "7"].index(pitch_match[0][-1]) + 4 
                height = pitch_match[0][:-1]
            else: # octave is not known
                octave = 5
                height = pitch_match[0]
            freq = 261.626 * 2 ** ((["c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b"].index(height) / 12. + octave - 4))  
            
        # generate sound
        t = arange(0, t_max, 1/sample_freq)
        wave = square(2 * pi * freq * t)
        
        # append to output
        output = hstack((output, wave))
    
    print(f"{output} - {sample_freq}") 
    

def main():
    sample = "16e6,16e6,32p,8e6,16c6,8e6,8g6,8p,8g,8p,8c6,16p,8g,16p,8e,16p,8a,8b,16a#,8a,16g.,16e6,16g6,8a6,16f6,8g6,8e6,16c6,16d6,8b,16p,8c6,16p,8g,16p,8e,16p,8a,8b,16a#,8a,16g.,16e6,16g6,8a6,16f6,8g6,8e6,16c6,16d6,8b,8p,16g6,16f#6,16f6,16d#6,16p,16e6,16p,16g#,16a,16c6,16p,16a,16c6,16d6,8p,16g6,16f#6,16f6,16d#6,16p,16e6,16p,16c7,16p,16c7,16c7,p,16g6,16f#6,16f6,16d#6,16p,16e6,16p,16g#,16a,16c6,16p,16a,16c6,16d6,8p,16d#6,8p,16d6,8p,16c6"
    sample_t = 100
    play_melody(sample, sample_t)
    winsound.Beep(17000, 100)


if __name__ == '__main__':
    main()
