
import matplotlib
import matplotlib.pyplot as plt

from mne.datasets import sample
from mne.io import read_raw_fif

from mne_realtime import LSLClient, MockLSLStream


# this is the host id that identifies your stream on LSL
host = 'mne_stream'
# this is the max wait time in seconds until client connection
wait_max = 5

# Load a file to stream raw data
#data_path = sample.data_path()
#raw_fname = data_path  / 'MEG' / 'sample' / 'sample_audvis_filt-0-40_raw.fif'
#raw_fname = '/Users/jobrenn/Documents/Projects/honors-ar/mock_data_for_lsl.fif'
raw_fname = 'mock_data_for_lsl.fif'
raw = read_raw_fif(raw_fname).crop(0, 30).load_data().pick('eeg')

#data = raw.get_data()
#times = raw.times
#fig, ax = plt.subplots()
#for i in range(4):
#    plt.cla()
#    plt.plot(times, data[i])
#    ax.set_xlabel('time, s')
#    ax.set_ylabel('amplitude, muV')
#    plt.draw()
#    plt.pause(1.)

# For this example, let's use the mock LSL stream.
sec_per_epoch = 5
epochs_per_group = 6

# main function is necessary here to enable script as own program
# in such way a child process can be started (primarily for Windows)
if __name__ == '__main__':
    with MockLSLStream(host, raw, 'eeg'):
        with LSLClient(info=raw.info, host=host, wait_max=wait_max) as client:
            client_info = client.get_measurement_info()
            sfreq = int(client_info['sfreq'])
            samples_to_grab = sfreq * sec_per_epoch

            # let's observe some data
            #for ii in range(samples_to_grab):
            #    print('Got sample %d/%d' % (ii + 1, samples_to_grab))
            #    epoch = client.get_data_as_epoch(n_samples=1)
            #    print(epoch.get_data())

            # let's plot an epoch
            fig, ax = plt.subplots(figsize=(6, 3))
            ax.set_xlabel('time, s')
            ax.set_ylabel('amplitude, muV')
            ii = 0
            while ii < 30:
                print('Getting data %d-%d sec' % (ii, ii+sec_per_epoch))
                epoch = client.get_data_as_epoch(n_samples=samples_to_grab)
                data = epoch.get_data()
                times = epoch.times
                plt.cla()
                plt.plot(times, data[0].transpose())
                plt.title(str(ii) + ' to ' + str(ii+sec_per_epoch) )
                ax.set_xlabel('time, s')
                ax.set_ylabel('amplitude, muV')
                plt.draw()
                plt.pause(1.)
                ii = ii+sec_per_epoch

print('Streams closed')


