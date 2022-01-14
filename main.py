from flask import Flask,send_file, request
from flask_restful import Api, Resource
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)

#importing resources
from app.RouteResources import Visualization as vis_resources
from app.RouteResources import Filter as filt_resources
from app.RouteResources import Classifier as classifier_resources
from app.RouteResources import SignalProcessor as signalprocessor_resources

#Handling routes
#visualization
api.add_resource(vis_resources.TimeSeries,'/visualize/timeseries')
api.add_resource(vis_resources.FrequencyDomain,'/visualize/frequency')
api.add_resource(vis_resources.Spectrogram,'/visualize/spectrogram')
api.add_resource(vis_resources.TimeFreqSpec,'/visualize/timefreqspec')

#filters
api.add_resource(filt_resources.Harmonic,'/filter/harmonic')
api.add_resource(filt_resources.WaveletFilter,'/filter/waveletdenoise')
api.add_resource(filt_resources.ButterworthFilter,'/filter/bandpass')
api.add_resource(filt_resources.FilterPipeline,'/filter/pipeline')

#classifier
api.add_resource(classifier_resources.PredictAbnormality,'/classifier/abnormality')
api.add_resource(classifier_resources.PredictDisorder,'/classifier/disorder')
api.add_resource(classifier_resources.Visualize_Result,'/classifier/visualize')

#signal processing
api.add_resource(signalprocessor_resources.Melspectrogram,'/signal/melspectrogram')

#handling page not found error
@app.errorhandler(404)
def invalid_route(e):
    return {'error':"404",
        "message":"invalide path"
    }

@app.errorhandler(400)
def bad_req(e):
    return {'error':"400",
        "message":"bad request"
    }

#main
if __name__=='__main__':
    app.run(debug=True)