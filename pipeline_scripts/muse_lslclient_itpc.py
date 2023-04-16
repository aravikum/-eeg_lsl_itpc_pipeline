import matplotlib.pyplot as plt
import numpy as np

from mne.datasets import sample
from mne.io import read_raw_fif
from mne import make_fixed_length_epochs
from mne_realtime import LSLClient, MockLSLStream

from scipy.fft import rfft, rfftfreq
from scipy import signal

host = '116' # host id that identifies your stream on LSL
wait_max = 1 # max wait time in seconds until client connection

num_channels = 5
# sec_per_epoch = 4.8 # divisible by ISI interval -- 4.8 was for diff stim
sec_per_epoch = 5
#epochs_per_group = 6
epochs_per_group = 12

#data_path = sample.data_path() # Load a file to stream raw data
#raw_fname = data_path  / 'MEG' / 'sample' / 'sample_audvis_filt-0-40_raw.fif'
#raw_fname = '/Users/jobrenn/Documents/Projects/honors-ar/mock_data_for_lsl.fif'
# raw_fname = 'mock_data_for_lsl.fif'
# raw = read_raw_fif(raw_fname).crop(0, 120).load_data().pick('eeg')
#ep = make_fixed_length_epochs(raw, duration=sec_per_epoch, preload=False)
#sfreq = int(raw.info['sfreq'])
#time_step = 1/sfreq
#data = ep.get_data()

#freqs = rfftfreq(data.shape[2], d=time_step)
#samples_per_epoch = sec_per_epoch * sfreq
#num_freqs = freqs.shape[0]
#coefs = np.zeros([epochs_per_group, num_channels, num_freqs], dtype=complex)

#for i in range(epochs_per_group):
#    coefs[i] = rfft(signal.detrend(data[i]))
        
def do_itpc(coefs):
    angles = np.angle(coefs)
    vals = np.abs(np.mean(np.exp(1.j * angles)))
    return vals

#itpc = np.zeros([num_channels, num_freqs])
#for c in range(num_channels):
#    for f in range(num_freqs):
#        itpc[c,f] = do_itpc(coefs[:, c, f])

#plt.plot(freqs, itpc.transpose())
#plt.xlim([0, 10])
#plt.show()

# main function is necessary here to enable script as own program
# in such way a child process can be started (primarily for Windows)
if __name__ == '__main__':
    # with MockLSLStream(host, raw, 'eeg'):
    with LSLClient(host=host, wait_max=wait_max) as client:
        client_info = client.get_measurement_info()
        sfreq       = int(client_info['sfreq'])
        time_step   = 1/sfreq
        samples_per_epoch = int(np.floor(sec_per_epoch * sfreq))
        samples_to_grab = int(np.floor(sfreq * sec_per_epoch))

        fig, ax = plt.subplots(figsize=(6, 3))
        ax.set_xlabel('frequency, Hz')
        ax.set_ylabel('ITPC')
        plt.draw()
        ii = 0 # data interval (sec)
        kk = 0 # group index
        while ii < 120:
            print('Getting data %d-%d sec' % (ii, ii+sec_per_epoch))
            print('Group index: %d' % kk)
            epoch = client.get_data_as_epoch(n_samples=samples_to_grab)
            print("great success")
            data  = epoch.get_data()
            if ii == 0:
                freqs = rfftfreq(data.shape[2], d=time_step)
                num_freqs = freqs.shape[0]
                coefs = np.zeros([epochs_per_group, 
                                    num_channels, 
                                    num_freqs], 
                                    dtype=complex)
                
            print(kk)
            coefs[kk] = rfft(signal.detrend(data[0]))
            print("here")
            # advance the group index or reset if at max
            if kk == epochs_per_group - 1:
                kk = 0
            else:
                kk = kk + 1
                    
            itpc = np.zeros([num_channels, num_freqs])
            print("here")
            for c in range(num_channels):
                for f in range(num_freqs):
                    itpc[c,f] = do_itpc(coefs[:, c, f])
            print("here")

            plt.cla()
            plt.plot(freqs, itpc.transpose())
            plt.title('ITPC %d-%d, window size: %d' % 
                        (ii, ii+sec_per_epoch, epochs_per_group * sec_per_epoch))
            plt.xlim([0, 20])
            plt.draw()
            plt.pause(1.)
            ii = ii+sec_per_epoch

print('Streams closed')

