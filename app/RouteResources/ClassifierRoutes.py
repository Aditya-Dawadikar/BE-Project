from flask import request,jsonify
from flask_restful import Resource
from app.Controllers import Utilities, Analyser
from app.Storage.TempAudioFile import TempAudioFile
import numpy as np

from app.Storage.UniqueIdGenerator import generate_unique_string

utils = Utilities.Utilities()
taf = TempAudioFile()

class Analyse(Resource):
    def post(self):
        data = request.json
        try:
            signaldata=list(data["signaldata"].values())  #this modification is necessary for getting data from client.
            samplingrate=data["samplingrate"]
        except TypeError:
            return {"Error":"missing key-value"},400

        # filename = taf.save_to_local_storage(np.array(signaldata),samplingrate)
        analyser = Analyser.Analyser()
        result=analyser.analyse(np.array(signaldata),samplingrate)
        # result["segment_id"] = filename
        result["segment_id"] = generate_unique_string()+".wav"
        return result
