import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import inv ##multiplicative inverse for a matrix
import scipy
from scipy import signal
from scipy.signal import wiener
from numpy import array
from numpy import empty
import pandas as pd
import random
import csv

data = pd.read_excel('sampleoutput1.xlsx')
data = np.array(data)
f = open("ECG.csv",'a')
# ECG=[]
# for i in range(len(data)):
#     ECG.append([data[i,0],data[i,1]+random.randint(1,10000)])
#     f.write(str(data[i,0])+","+str(data[i,1]+random.randint(1,10000))+"\n")

ECG = pd.read_csv('ECG.csv')
ECG = np.array(ECG)
print(ECG)

f.close()
    





def kth_diag_indices(matrix, k, value):
    points=[]
    rows, cols = np.diag_indices_from(matrix)
    if k < 0:
        rows=rows[-k:]
        cols=cols[:k]
    elif k > 0:
        rows=rows[:-k]
        cols=cols[k:]
    else:
        rows=rows
        cols=cols

    for i in range(len(rows)):
        points.append((rows[i], cols[i]))
    for i in range (len(points)) :
        matrix[points[i]]=value
    return matrix

def signal_wienerFilteration(signals, c, sigma2v, filterOrder):
    #Build and apply your filter
    #signal = wiener(signal, mysize=29, noise=0.5)

    n=len(signals)
    a = empty([filterOrder, filterOrder])
    b = empty([filterOrder, 1])
    Ryy=empty([n,1])
    ##Filling Ryy for Entire Signal
    for i in range(n):
        temp =0
        i2=i
        for i2 in range (n):
            if  (i2-i) >=0 :
                #print signals[i2] ,'*',signals[i2-i] ,'=', signals[i2] * signals[i2-i]
                temp += signals[i2] * signals[i2-i]
        #print temp

        Ryy[i]=(1.0/n)* temp


    b = Ryy[:filterOrder]
    b[0] = b[0]-sigma2v
    tempo =Ryy[:filterOrder]
    #filling Diagonals
    for k in range (filterOrder):
        a=kth_diag_indices(a,k,tempo[k])
    for k in range(-filterOrder+1,0):
        a=kth_diag_indices(a,k,tempo[k*-1])

    a=np.linalg.inv(a)
    #a= (1/c) * a
    h =np.matmul(a, b)/c
    #signals=np.convolve(h, signals)
    signals =signal.convolve(signals.reshape(signals.shape[0], 1), h,"same")
    #print h
    #print h.shape , signals.shape
    #print Ryy
    #print b
    #np.set_printoptions(suppress=True)
    #print a
    return signals


if __name__=='__main__':
    #Model Parameters c and sigmav^2
    c = -3
    varV = 1
    # Let filter order is 3
    filtOrder = 1

    n = np.array(range(len(data[:,1])))

 


  
    filteredSignal = signal_wienerFilteration(data[:,1],c,varV, filtOrder)

    
    meanSqrErr = np.mean(np.sqrt((data[:,1] - filteredSignal)**2))
    plt.figure("Original vs Filtered")
    temp = filteredSignal+meanSqrErr
    plt.xlim(0,len(n))
    plt.plot(n,data[:,1],'b', label='Original Signal')
    plt.plot(n,filteredSignal+meanSqrErr,'g', label = 'filtered Signal')
    plt.legend()
    error = np.mean(np.sqrt((temp - ECG[:,1])**2))/np.mean(data[:,1])*100
   
    print("Percentage Error: ", error, "%")
    plt.show()

