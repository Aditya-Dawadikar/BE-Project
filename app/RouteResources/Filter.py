from flask import request,jsonify
from flask_restful import Resource
from app.Controllers import FilterBank,Preprocessor
import numpy as np

filter = FilterBank.FilterBank()
preprocessor = Preprocessor.Preprocessor()

class Harmonic(Resource):
    def get(self):
        data = request.json
        try:
            signaldata=data["signaldata"]    
            samplingrate=data["samplingrate"]
        except TypeError:
            return {"Error":"missing key-value"},400

        y_harmonic=filter.harmonic_component(signaldata)
        return {"y_filtered":y_harmonic.tolist()}

class WaveletFilter(Resource):
    def get(self):
        data = request.json
        try:
            signaldata=data["signaldata"]    
            samplingrate=data["samplingrate"]
        except TypeError:
            return {"Error":"missing key-value"},400

        filtered_data=filter.wavelet_denoise_visu_shrink(signaldata)
        return {"y_filtered":filtered_data.tolist()}

class ButterworthFilter(Resource):
    def get(self):
        data = request.json
        try:
            signaldata=data["signaldata"]    
            samplingrate=data["samplingrate"]
        except TypeError:
            return {"Error":"missing key-value"},400

        filtered_data=filter.butter_bandpass_filter(data=signaldata, lowcut=filter.bandpass_lowcut, highcut=filter.bandpass_highcut, fs=samplingrate, order=5)
        cleaned_data=filter.getPureSample(signaldata,filtered_data)
        return {"y_filtered":cleaned_data}

class FilterPipeline(Resource):
    def get(self):
        data = request.json
        try:
            signaldata=data["signaldata"]    
            samplingrate=data["samplingrate"]
        except TypeError:
            return {"Error":"missing key-value"},400
            
        filtered_data=filter.filterbank(signaldata=signaldata,samplingrate=samplingrate)
        return {"y_filtered":filtered_data}
