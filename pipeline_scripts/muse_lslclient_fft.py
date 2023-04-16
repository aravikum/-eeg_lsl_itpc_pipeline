import matplotlib.pyplot as plt
import numpy as np

from mne.datasets import sample
from mne.io import read_raw_fif
from mne_realtime import LSLClient, MockLSLStream

from scipy.fft import rfft, rfftfreq
from scipy import signal

host = '116' # host id that identifies your stream on LSL
wait_max = 5 # max wait time in seconds until client connection


#data_path = sample.data_path() # Load a file to stream raw data
#raw_fname = data_path  / 'MEG' / 'sample' / 'sample_audvis_filt-0-40_raw.fif'
# #raw_fname = '/Users/jobrenn/Documents/Projects/honors-ar/mock_data_for_lsl.fif'
# # raw_fname = 'mock_data_for_lsl.fif'
# raw = read_raw_fif(raw_fname).crop(0, 30).load_data().pick('eeg')
#data = raw.get_data()
#sfreq = int(raw.info['sfreq'])

channels = 5
sec_per_epoch = 5

#!!! window size !!!
epochs_per_group = 12
        
def to_fft(data, sfreq):
    time_step = 1/sfreq
    freqs = rfftfreq(data.shape[1], d=time_step)
    coefs = rfft(signal.detrend(data))
    return freqs, coefs

# main function is necessary here to enable script as own program
# in such way a child process can be started (primarily for Windows)
if __name__ == '__main__':
    #with MockLSLStream(host, raw, 'eeg'):
    with LSLClient(host=host, wait_max=wait_max) as client:
        client_info = client.get_measurement_info()
        sfreq = int(client_info['sfreq'])
        samples_to_grab = sfreq * sec_per_epoch

        # let's plot an epoch
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.set_xlabel('time, s')
        ax.set_ylabel('amplitude, muV')

        ii = 0
        #while ii < 30:
        while True:
            print('Getting data %d-%d sec' % (ii, ii+sec_per_epoch))
            epoch = client.get_data_as_epoch(n_samples=samples_to_grab)
            data = epoch.get_data()
            freqs, coefs = to_fft(data[0], sfreq)
            pwr = np.abs(coefs)
            plt.cla()
            plt.xlim([0, 10])
            plt.plot(freqs, pwr.transpose())
            plt.title(str(ii) + ' to ' + str(ii+sec_per_epoch) )
            plt.draw()
            plt.pause(1.)
            ii = ii+sec_per_epoch

print('Streams closed')

#for all scripts:
 # after plt.plot(), ax.setxlimits 0 -> 20 (meaningful window)

#window size: how many diff segments of data to group tg for itpc
# include window size as cl argument
