from flask_restful import Resource
from flask import request,jsonify

class TestFlask(Resource):
    def post(self):
        data = request.json
        signaldata=list(data["signaldata"].values())
        return "happy"