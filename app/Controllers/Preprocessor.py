import numpy as np 
import librosa as lb 
from app.Controllers import FilterBank 

class Preprocessor:
    
    def __init__(self):
        self.duration=6

    def get_padded_segment(self,signaldata,samplingrate):
        reqLen=self.duration*samplingrate # required samples are of length 6 secs
        padded_data = lb.util.pad_center(signaldata, reqLen) # pad the sample with zero on both ends to make it 6 secs long
        return padded_data

    def get_filtered_segment(self,signaldata,samplingrate):
        filter = FilterBank.FilterBank()
        filtered_data = filter.filterbank(signaldata=signaldata,samplingrate=samplingrate)
        return filtered_data