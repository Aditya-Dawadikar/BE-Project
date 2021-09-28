from flask import request,jsonify
from flask_restful import Resource
from app.Controllers import Classifier,Utilities

utils = Utilities.Utilities()
result_visualizer = Classifier.Classifier_Result()

class PredictAbnormality(Resource):
    def __init__(self):
        self.abnormality_classifier = Classifier.Abnormality_classifier_wrapper()
        pass

    def get(self):
        data = request.json
        signaldata=np.asarray(data["signaldata"])
        samplingrate=data["samplingrate"]
        classes,results=self.abnormality_classifier.predict(signaldata,samplingrate)
        return {
                "classes":classes,
                "probabilities":probabilities
                }

class PredictDisorder(Resource):
    def __init__(self):
        self.disorder_classifier = Classifier.Disorder_classifier_wrapper()
        pass

    def get(self):
        data = request.json
        signaldata=np.asarray(data["signaldata"])
        samplingrate=data["samplingrate"]
        classes,results=self.disorder_classifier.predict(signaldata,samplingrate)
        return {
                "classes":classes,
                "probabilities":probabilities
                }

class Visualize_Result(Resource):
    def get(self):
        data = request.json
        classes=data["classes"]
        probabilities=data["probabilities"]
        plot=result_visualizer.visualize_results(classes,probabilities)
        return utils.send_plot(plot)