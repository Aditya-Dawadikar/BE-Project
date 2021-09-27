from flask_restful import Resource
from flask import request,jsonify
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq, rfft, rfftfreq
import numpy as np

from app.Controllers import Utilities

utils = Utilities.Utilities()

class TimeSeries(Resource):
    def get(self):
        #extracting request body
        data = request.json
        signaldata=data["signaldata"]
        #plotting timeseries data
        plt.plot(signaldata)
        plot=utils.wrap_to_bytesio(plt)        
        return utils.send_plot(plot)

class Spectrogram(Resource):
    def get(self):        
        #extracting request body
        data = request.json
        signaldata=data["signaldata"]
        #plotting spectrogram data
        plt.specgram(signaldata)
        plot=utils.wrap_to_bytesio(plt)        
        return utils.send_plot(plot)

class FrequencyDomain(Resource):
    def get(self):        
        #extracting request body
        data = request.json
        signaldata=data["signaldata"]
        samplingrate=data["samplingrate"]
        duration=data["duration"]   #seconds
        #precomputation for plot
        N = samplingrate * duration # duration:6secs
        yf = rfft(signaldata)
        xf = rfftfreq(N, 1 / samplingrate)
        #plotting frequency domain data
        plt.plot(xf, np.abs(yf))
        plot=utils.wrap_to_bytesio(plt)        
        return utils.send_plot(plot)

class TimeFreqSpec(Resource):
    def visualize_audio(self,data,samplingrate):
        f = plt.figure(figsize=(20,5),dpi=utils.dpi)

        ax1 = f.add_subplot(131)
        ax2 = f.add_subplot(132)
        ax3 = f.add_subplot(133)

        #time domain visualization
        ax1.plot(data)
        ax1.set_xlabel('Sample')
        ax1.set_ylabel('Amplitude')
        ax1.set_title("Time Domain")
        
        #frequency domain visualization
        N = samplingrate * 6 # duration:6secs
        yf = rfft(data)
        xf = rfftfreq(N, 1 / samplingrate)
        ax2.plot(xf, np.abs(yf))
        ax2.set_xlabel('Frequency')
        ax2.set_ylabel('Magnitude')
        ax2.set_title("Frequency Domain")

        #spectrogram
        ax3.specgram(data,Fs=samplingrate)
        ax3.set_xlabel('Time')
        ax3.set_ylabel('Frequency')
        ax3.set_title("Spectrogram")
        return plt

    def get(self):
        #extracting request body
        data = request.json
        signaldata=data["signaldata"]
        samplingrate=data["samplingrate"]
        duration=data["duration"]   #seconds
        plot=utils.wrap_to_bytesio(self.visualize_audio(data=signaldata,samplingrate=samplingrate))        
        return utils.send_plot(plot)
