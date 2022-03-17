import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

from app.Storage.UniqueIdGenerator import generate_unique_string

plt.rcParams["figure.figsize"] = (3,2)
plt.rc('axes', titlesize=10) 
plt.rc('axes', labelsize=8)
plt.rc('xtick', labelsize=5) 
plt.rc('ytick', labelsize=5) 

class GraphPlotter:
    def __init__(self):
        self.temp_dest = 'Temp/images/'
        pass
    
    def get_figure_index(self):
        # if figure index is not added to plot, then a blank figure is saved
        return len(os.listdir(self.temp_dest))+1
    
    def savePlot(self):
        filename = self.temp_dest+generate_unique_string()+".png"
        plt.savefig(filename)
        plt.clf()
        return filename
    
    def timeseries(self,signaldata):
        plt.figure(self.get_figure_index())
        plt.xlabel("time")
        plt.ylabel("magnitude")
        plt.title("Timeseries")
        plt.xticks(rotation=45)
        plt.yticks(rotation=45) 
        plt.plot(signaldata)
        return self.savePlot()
        
    def spectrogram(self,signaldata,samplingrate):
        plt.figure(self.get_figure_index())
        plt.xlabel("time")
        plt.ylabel("frequency")
        plt.title("Spectrogram")
        # plt.xticks(rotation=45)
        plt.yticks(rotation=45) 
        plt.specgram(signaldata,Fs=samplingrate)
        plt.ylim([0,1200])
        return self.savePlot()
    
gp = GraphPlotter()