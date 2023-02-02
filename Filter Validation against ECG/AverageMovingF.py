import numpy as np
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_excel('sampleoutput1.xlsx')
data = np.array(data)

ECG = pd.read_csv('ECG.csv')
ECG = np.array(ECG)




order = 6
fs =300.0       # sample rate, Hz
cutoff = 2.667  # desired cutoff frequency of the filter, Hz

def average_moving(cutoff, fs, order=5):
    return butter(order, cutoff, fs=fs, btype='low', analog=False)

def average_moving_lowpass_filter(data, cutoff, fs, order=5):
    b, a = average_moving(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

b, a = average_moving(cutoff, fs, order)

# Plot the frequency response.
w, h = freqz(b, a, fs=fs, worN=8000)
plt.subplot(2, 1, 1)
plt.plot(w, np.abs(h), 'b')
plt.plot(cutoff, 0.5*np.sqrt(2), 'ko')
plt.axvline(cutoff, color='k')
plt.xlim(0, 0.5*fs)
plt.title("average Moving Lowpass Filter Frequency Response")
plt.xlabel('Frequency [Hz]')
plt.grid()


T = 5.0         # seconds
n = int(T * fs) # total number of samples
t = np.array(range(len(data[:,1])))

# "Noisy" data.  We want to recover the 1.2 Hz signal from this.

# Filter the data, and plot both the original and filtered signals.
y = average_moving_lowpass_filter(data[:,1], cutoff, fs, order)

plt.subplot(2, 1, 2)
plt.plot(t[400:], data[400:,1], 'b-', label='data')
plt.plot(t[400:], y[400:], 'g-', linewidth=2, label='filtered data')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()
error = np.mean(np.sqrt((data[:-1,1] - ECG[:,1])**2))
print("error", error/np.mean(data[:,1])*100, "%")
plt.subplots_adjust(hspace=0.35)
plt.show()