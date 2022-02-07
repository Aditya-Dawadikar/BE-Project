from flask_restful import Resource
from flask import request,jsonify

from app.Storage.AudioFile import AudioFile

af = AudioFile()

class TestFlask(Resource):
    def get(self):
        print(af.migrate_audio("1644248278_73b0811cd20f4636bb61f05a18a3712b.wav"))
        return {"hello":"world"}