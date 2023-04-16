'''
This script receives a Petal formatted LSL stream and prints it to the console.
Usage: python lsl_receive.py -n PetalStream_eeg
valid LSL stream names for use with petal streaming apps:
    * PetalStream_gyroscope
    * PetalStream_ppg
    * PetalStream_telemetry
    * PetalStream_eeg
    * PetalStream_acceleration
    * PetalStream_connection_status
-- see PetalDocs
'''
import argparse

import pylsl
import time
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import argparse


import numpy as np

from scipy import fftpack, signal

from matplotlib import pylab as pl

def to_fft(inlet, sec):
    sample_num = sec * 128
    mat = [[]]
    while len(mat[0]) < sample_num:
        print("about to pull")
        sample, timestamp = inlet.pull_sample()
        print("pulled")
        for x in range(5):
            mat[x].append(sample[x])
            mat.append([])

    # for x in range(5):
    #     print("fft", fft(np.array(mat[x])))
    print("about to fft")
    return fft(np.array(mat[x]))
        
def fft_coeff(data):
    time_step = 1/128.0

    sampling_freqs = fftpack.fftfreq(data.size, d=time_step)
    positive_freqs = np.where(sampling_freqs > 0)
    freqs = sampling_freqs[positive_freqs] 
    coeff = fftpack.fft(signal.detrend(data))
    return freqs, coeff
def fft(data):
    # Those can be precomputed for several data lengths
    time_step = 1/128.0

    sampling_freqs = fftpack.fftfreq(data.size, d=time_step)
    positive_freqs = np.where(sampling_freqs > 0)
    freqs = sampling_freqs[positive_freqs]

    # Here's the computation part
    power = np.abs(fftpack.fft(signal.detrend(data)))[positive_freqs] ** 2
    return freqs, power



# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []


def animate(i, xs, ys):

    
    print("animate")
    freq,power = to_fft(5)
    print(freq, power)
    xs.append(freq[i])
    ys.append(10*np.log10(power[i]))
     # Limit x and y lists to 20 items
    xs = xs[-20:]
    ys = ys[-20:]

   # Draw x and y listsn
    ax.clear()
    ax.plot(xs, ys)
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('LSL Client Real-Time')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('PSD [dB]')


    #freq
    #xs.append(freq)
    #power


 
    ##
    # plt.figurefigsize = (8, 4)
    # plt.plot(freq[i], 10*np.log10(power[i]))
    #plt.xlim(0, 100);
    # plt.xlabel('Frequency [Hz]')
    # plt.ylabel('PSD [dB]')
    #plt.show()
    #ys.append(power)

    # # Limit x and y lists to 20 items
    # xs = xs[-20:]
    # ys = ys[-20:]

    # Draw x and y listsn
    # ax.clear()
    # ax.plot(xs, ys)

    # # Format plot
    # plt.xticks(rotation=45, ha='right')
    # plt.subplots_adjust(bottom=0.30)
    # plt.title('LSL Client Real-Time')
    # plt.ylabel('Power')

# Set up plot to call animate() function periodically


# t_end = time.time() + 5


parser = argparse.ArgumentParser()
parser.add_argument('-n', '--stream_name', type=str, required=True,
                    default='PetalStream_eeg', help='the name of the LSL stream')
args = parser.parse_args()

# first resolve an EEG stream
print(f'looking for a stream with name {args.stream_name}...')
streams = pylsl.resolve_stream('name', args.stream_name)

# create a new inlet to read from the stream
if len(streams) == 0:
    raise RuntimeError(f'Found no LSL streams with name {args.stream_name}')
inlet = pylsl.StreamInlet(streams[0])
print("here")

streams = pylsl.resolve_stream('name', "Petal_Stream_eeg")


while True: 
    #mat = to_fft(5)
    ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)
    plt.show()

# while True:
#     sample, timestamp = inlet.pull_sample()
#     print(timestamp, sample)

# while time.time() < t_end:
#     sample, timestamp = inlet.pull_sample()
#     print(timestamp, sample)