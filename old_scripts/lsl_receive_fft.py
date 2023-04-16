import argparse

import pylsl

import numpy as np
import time

from scipy import fftpack, signal


from matplotlib import pylab as pl

def to_fft(sec):
    sample_num = sec * 128
    mat = [[]]
    while len(mat[0]) < sample_num:
        sample, timestamp = inlet.pull_sample()
        for x in range(5):
            mat[x].append(sample[x])
            mat.append([])

    for x in range(5):
        print("fft", fft(np.array(mat[x])))
    print(len(mat[0]))
        
        
        
def fft(data):
    #N =  len(data)
    # Those can be precomputed for several data lengths
    time_step = 1/128.0

    sampling_freqs = fftpack.fftfreq(data.size, d=time_step)
    positive_freqs = np.where(sampling_freqs > 0)
    freqs = sampling_freqs[positive_freqs]
   
    # fourier = fftpack.fft(data)
    # psd = 2.0/N * np.abs(fourier[:N//2])

    # Here's the computation part
    power = np.abs(fftpack.fft(signal.detrend(data)))[positive_freqs]
    return freqs, power


parser = argparse.ArgumentParser()
parser.add_argument('-n', '--stream_name', type=str, required=True,
                    default='PetalStream_eeg', help='the name of the LSL stream')
args = parser.parse_args()

# first resolve an EEG stream
print(f'looking for a stream with name {args.stream_name}...')
streams = pylsl.resolve_stream('name', args.stream_name)
print("I got here")
# create a new inlet to read from the stream
if len(streams) == 0:
    raise RuntimeError(f'Found no LSL streams with name {args.stream_name}')
inlet = pylsl.StreamInlet(streams[0])

print("I got here")
count = 0
# while True:
#     to_fft(5)

while count < 5:
    to_fft(5)
    count +=1




