from flask_restful import Resource
from flask import request,jsonify

from app.Services.GraphPlotter import gp

class TestFlask(Resource):
    def post(self):
        data = request.json
        return gp.spectrogram(signaldata=data["signaldata"],samplingrate=data["samplingrate"])