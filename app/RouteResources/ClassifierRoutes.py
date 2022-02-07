from flask import request,jsonify
from flask_restful import Resource
from app.Controllers import Utilities, Analyser
from app.Storage.AudioFile import AudioFile
import numpy as np

utils = Utilities.Utilities()

class Analyse(Resource):
    def post(self):
        data = request.json
        try:
            signaldata=list(data["signaldata"].values())  #this modification is necessary for getting data from client.
            samplingrate=data["samplingrate"]
        except TypeError:
            return {"Error":"missing key-value"},400

        af = AudioFile()
        filename = af.upload_audio(np.array(signaldata),samplingrate)
        analyser = Analyser.Analyser()
        result=analyser.analyse(np.array(signaldata),samplingrate)
        result["segment_id"] = filename
        return result
