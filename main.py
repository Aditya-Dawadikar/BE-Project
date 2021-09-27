from flask import Flask,send_file, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

#importing resources
from app.RouteResources import Visualization as vis_resources
from app.RouteResources import Filter as filt_resources

#Handling routes
#visualization
api.add_resource(vis_resources.TimeSeries,'/visualize/timeseries')
api.add_resource(vis_resources.FrequencyDomain,'/visualize/frequency')
api.add_resource(vis_resources.Spectrogram,'/visualize/spectrogram')
api.add_resource(vis_resources.TimeFreqSpec,'/visualize/timefreqspec')

#filters
api.add_resource(filt_resources.WaveletFilter,'/filter/waveletdenoise')
api.add_resource(filt_resources.ButterworthFilter,'/filter/bandpass')
api.add_resource(filt_resources.FilterPipeline,'/filter/pipeline')

#handling page not found error
@app.errorhandler(404)
def invalid_route(e):
    return {'error':"404",
        "message":"invalide path"
    }

#main
if __name__=='__main__':
    app.run(debug=True)