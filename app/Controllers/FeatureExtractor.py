import librosa as lb 

from app.Controllers import Utilities

utils = Utilities.Utilities()

class FeatureExtractor:
    def __init__(self):
        self.n_mfcc=13
        self.n_chroma=12
        pass

    # returns 2D matrix or a Flat array of MFCC features
    def get_mfcc(self,signaldata,samplingrate,flat=False):
        if samplingrate!=utils.resamp_rate:
            signaldata=utils.resample(signaldata,samplingrate,utils.resamp_rate)
            samplingrate=utils.resamp_rate
        mfcc=lb.feature.mfcc(y=signaldata,sr=samplingrate, n_mfcc=self.n_mfcc)
        if flat==True:
            mfcc=mfcc.flatten()
        return mfcc

    # returns 2D matrix or a Flat array of chroma stft
    def get_chroma_stft(self,signaldata,samplingrate,flat=False):
        if samplingrate!=utils.resamp_rate:
            signaldata=utils.resample(signaldata,samplingrate,utils.resamp_rate)
            samplingrate=utils.resamp_rate
        chroma_stft=lb.feature.chroma_stft(y=signaldata,sr=samplingrate, n_chroma=self.n_chroma)
        if flat==True:
            chroma_stft=chroma_stft.flatten()
        return chroma_stft

    # returns 2D matrix or a Flat array of mel spectrogram
    def get_mel_spectrogram(self,signaldata,samplingrate,flat=False):
        if samplingrate!=utils.resamp_rate:
            signaldata=utils.resample(signaldata,samplingrate,utils.resamp_rate)
            samplingrate=utils.resamp_rate
        mel_spectrogram=lb.feature.melspectrogram(y=signaldata,sr=samplingrate)
        if flat==True:
            mel_spectrogram=mel_spectrogram.flatten()
        return mel_spectrogram