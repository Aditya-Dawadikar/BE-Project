from flask import send_file
from io import BytesIO

class Utilities:
    def __init__(self):
        self.dpi=300
        self.resamp_rate=22050
        pass

    #A wrapper for converting plot to BytesIO image
    def wrap_to_bytesio(self,plt):
        bytesIO = BytesIO()
        plt.savefig(bytesIO,dpi=self.dpi)
        bytesIO.seek(0)
        return bytesIO
    
    #return plot as image/png format
    #A wrapper for sending BytesIO object as png image around flask's send_file()
    def send_plot(self,plt,mimetype='image/png'):
        return send_file(plt,mimetype)

    #downsample audio signal
    #A wrapper for librosa.resample function.
    def resample(self,signaldata,samplingrate,targetrate):
        resampled_signal=lb.resample(signaldata,samplingrate,self.resamp_rate)
        return resampled_signal
    
    # standardization
    def standardize_data(self,signaldata,samplingrate):
        target_sr = 22050
        duration = 6
        resampled=lb.resample(y=signaldata, orig_sr=samplingrate, target_sr=target_sr)
        reqLen=duration*target_sr
            
        if len(resampled)<duration*target_sr:
            padded_data = lb.util.pad_center(resampled, reqLen)
            return padded_data,target_sr
        else:
            return resampled[0:reqLen],target_sr
        
        
util = Utilities()