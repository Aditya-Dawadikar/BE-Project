import numpy as np
from numpy import array 
import scipy.io
from scipy import signal
from scipy.signal import butter, sosfilt, sosfreqz
from skimage.restoration import denoise_wavelet
import librosa as lb

class FilterBank:
    
    def __init__(self):
        self.bandpass_lowcut=100
        self.bandpass_highcut=1000
        self.bandpass_order=15
        self.wavelet_level=5

    def butter_bandpass(self,lowcut, highcut, fs, order=5):
        # helper function describing the IIR filter
        # returns second order filter coefficients (sos)
        #nyquos frequency = 1/2 * sampling rate
        nyq = 0.5 * fs  
        low = lowcut / nyq
        high = highcut / nyq
        sos = butter(order, [low, high], analog=False, btype='band', output='sos')
        return sos

    def butter_bandpass_filter(self,data, lowcut, highcut, fs, order=5):
        # returns bandpass output using second order filter coefficients
        # filter order=5
        sos = self.butter_bandpass(lowcut, highcut, fs, order=order)
        y = sosfilt(sos, data)
        return y
    
    def wavelet_denoise_visu_shrink(self,data):
        # wavelet denoise filter
        # method=Visu Shrink
        # waveletlevels=15
        # mode=soft
        waveletdenoiseVisu = denoise_wavelet(data,method='VisuShrink',mode='soft',wavelet_levels=self.wavelet_level,wavelet='sym8',rescale_sigma='False')
        return waveletdenoiseVisu

    def harmonic_component(self,data):
        # harmonic component seperation from ambient noise
        # decomposition=hpss
        harmonic=lb.effects.harmonic(y=data)
        return harmonic

    # returns the pure sample by removing FFT induced weak signals
    def getPureSample(self,original_data,filtered_data):
        start=0
        end=len(original_data)
        
        for i in range(len(original_data)):
            if original_data[i]!=0:
                start=i
                break
            
        for i in reversed(range(len(original_data))):
            if original_data[i]!=0:
                end=i
                break
                
        newOutputSignal=[]
        for i in range(len(filtered_data)):
            if i<start or i>end:
                newOutputSignal.append(0)
            else:
                newOutputSignal.append(filtered_data[i])
        
        return newOutputSignal
    
    def filterbank(self,signaldata,samplingrate=44100):
        # Applies 3 filter layers to the input signal
        # step 1. harmonic-percussive component seperation
        # step 2. wavelet denoise
        # step 3. Butterworth Bandpass
        # step 4. Cleaning sample 

        #first harmonic extraction
        harmonic = self.harmonic_component(np.array(signaldata))

        #wavelet_output = wavelet_denoise_bayes_shrink(signaldata)
        wavelet_output = self.wavelet_denoise_visu_shrink(harmonic)
        
        # butterworth bandpass layer
        # adjusted low and high cut for a 100-1000Hz frequency band
        bandpass_output = self.butter_bandpass_filter(wavelet_output, lowcut=self.bandpass_lowcut, highcut=self.bandpass_highcut, fs=samplingrate, order=self.bandpass_order)
        
        #removing low power signal
        puresample = self.getPureSample(signaldata,bandpass_output)
        
        return puresample

    pass