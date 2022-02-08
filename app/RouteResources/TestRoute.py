from flask_restful import Resource
from flask import request,jsonify

from app.Storage.AudioFile import AudioFile

af = AudioFile()

class TestFlask(Resource):
    def get(self):
        print(af.get_file("101_1b1_Al_sc_Meditron.wav"))
        return {"hello":"world"}