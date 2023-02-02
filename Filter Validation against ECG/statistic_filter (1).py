import numpy as np
import pylab as p
import pandas as pd

def statistic_filt (x, k):
    """Apply a length-k median filter to a 1D array x.
    Boundaries are extended by repeating endpoints.
    """
    assert k % 2 == 1, "Median filter length must be odd."
    assert x.ndim == 1, "Input must be one-dimensional."
    k2 = (k - 1) // 2
    y = np.zeros ((len (x), k), dtype=x.dtype)
    y[:,k2] = x
    for i in range (k2):
        j = k2 - i
        y[j:,i] = x[:-j]
        y[:j,i] = x[0]
        y[:-j,-(i+1)] = x[j:]
        y[-j:,-(i+1)] = x[-1]
    return np.median (y, axis=1)


data = pd.read_excel('sampleoutput1.xlsx')
data = np.array(data)
f = open("ECG.csv",'a')
ECG = pd.read_csv('ECG.csv')
ECG = np.array(ECG)
f.close()
    
filterted_data = statistic_filt(data[:,1],15)
error = np.mean(np.sqrt((filterted_data[:-1] - ECG[:,1])**2))/np.mean(data[:,1])*100
print("absolute Error", error, "%")
p.plot (data[:,1])
p.plot (statistic_filt (data[:,1],3))
p.plot (statistic_filt (data[:,1],15))
p.show ()

    

