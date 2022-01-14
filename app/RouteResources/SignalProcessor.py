from flask_restful import Resource
from flask import request,jsonify

import librosa as lb 
import numpy as np

import json

class Melspectrogram(Resource):
    def post(self):
        body = request.json # axios request keys: [data,headers]
        # access payload directly when used with postman

        # print(data)

        data = body["data"]
        try:
            signaldata=data["signaldata"]
            samplingrate=data["samplingrate"]
        except TypeError:
            return {"Error":"missing key-value"},400

        signaldata = list(signaldata.values()) # flask is reading list from the json object as dictionary hence type casting is necessary

        signaldata=np.array(signaldata,dtype=float)
        melspec = lb.feature.melspectrogram(y=signaldata, sr=samplingrate, S=None, n_fft=2048, hop_length=512, win_length=None, window='hann', center=True, pad_mode='reflect', power=2.0)
        melspec_list=[]
        for i in range(melspec.shape[0]):
            row=[]
            for j in range(melspec.shape[1]):
                row.append(round(melspec[i][j],4))
            melspec_list.append(row)
        
        min = np.min(melspec_list)
        max = np.max(melspec_list)

        payload={
            "melspectrogram":melspec_list,
            "min": min,
            "max": max,
        }
        print(payload["min"])
        print(payload["max"])

        response = jsonify(payload)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response