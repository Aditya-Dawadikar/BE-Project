from flask import request,jsonify
from flask_restful import Resource
from app.Controllers import Utilities, Analyser
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

        analyser = Analyser.Analyser()
        result=analyser.analyse(np.array(signaldata),samplingrate)
        return result
