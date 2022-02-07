from flask import Flask,send_file, request
from flask_restful import Api, Resource
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
cors=CORS(app,resources={r"/api/*": {"origins": "http://localhost:3000"}})

#importing resources
from app.RouteResources import Visualization as vis_resources
from app.RouteResources import Filter as filt_resources
from app.RouteResources import ClassifierRoutes as classifier_resources
from app.RouteResources import TestRoute as test_resources
from app.RouteResources import StorageRoutes as storage_resources

#Handling routes
#visualization
api.add_resource(vis_resources.TimeSeries,'/api/visualization/timeseries')
api.add_resource(vis_resources.FrequencyDomain,'/api/visualation/frequency')
api.add_resource(vis_resources.Spectrogram,'/api/visualization/spectrogram')
api.add_resource(vis_resources.TimeFreqSpec,'/api/visualization/timefreqspec')
api.add_resource(vis_resources.Probability,'/api/visualization/probability')

#filters
api.add_resource(filt_resources.Harmonic,'/api/filter/harmonic')
api.add_resource(filt_resources.WaveletFilter,'/api/filter/waveletdenoise')
api.add_resource(filt_resources.ButterworthFilter,'/api/filter/bandpass')
api.add_resource(filt_resources.FilterPipeline,'/api/filter/pipeline')

#classifier
api.add_resource(classifier_resources.Analyse,'/api/analysis/predict')

#storage
api.add_resource(storage_resources.AudioMetaResource,'/api/storage/audiometa')
api.add_resource(storage_resources.SavePDF,'/api/storage/report')

#testing
api.add_resource(test_resources.TestFlask,'/api/test')

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