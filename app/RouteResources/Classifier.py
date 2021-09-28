from flask import request,jsonify
from flask_restful import Resource
from app.Controllers import Classifier,Utilities

utils = Utilities.Utilities()
result_visualizer = Classifier.Classifier_Result()

class Visualize_Result(Resource):
    def get(self):
        data = request.json
        classes=data["classes"]
        probabilities=data["probabilities"]
        plot=result_visualizer.visualize_results(classes,probabilities)
        return utils.send_plot(plot)