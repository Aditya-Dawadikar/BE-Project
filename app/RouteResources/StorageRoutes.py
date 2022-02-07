from flask import request,jsonify
from flask_restful import Resource

from app.Services.ResponseMessage import rm
from app.Controllers import ReportGenerator
from app.Storage.AudioMeta import AudioMeta

am = AudioMeta()

class SavePDF(Resource):
    def post(self):
        data = request.json
        try:
            print("here")
            # doctor_info = data["doctor_info"]
            # patient_info = data["patient_info"]
            # report_summary = data["report_summary"]
            # segment_list = data["segment_list"]
        except TypeError:
            return {"Error":"missing key-value"},400

        return {"report_data":data}
    
class AudioMetaResource(Resource):
    
    def get(self):
        data = request.json
        try:
            res = am.get_audio_meta_by_id(data["document_id"])
            return res
        except TypeError:
            return rm.dataMissing()
        
        # get all
        # res = am.get_all_audio_meta()
        # for doc in res:
        #     print(doc.to_dict())
        # return {"hello":"world"}
    
    def post(self):
        data = request.json
        try:
            analysis_object={
                    "segmentname":data["segmentname"],
                    "samplingrate":data["samplingrate"],
                    "abnormality":data["abnormality"],
                    "diagnosis":data["diagnosis"],
                    "severity":data["severity"],
                    "symptoms":data["symptoms"]
            }
            res = am.save_audio_meta(analysis_object)
        except TypeError:
            return {"Error":"missing key-value"},400
        
        return {"res":res}
    
    def put(self):
        data = request.json
        try:
            document_id = data["document_id"]
            updateable_fields = {
                "abnormality":{
                    "classes":data["abnormality"]["classes"],
                    "probabilities":data["abnormality"]["probabilities"],
                },
                "diagnosis":{
                    "classes":data["diagnosis"]["classes"],
                    "probabilities":data["diagnosis"]["probabilities"],
                },
                "severity":data["severity"],
                "isapproved":bool(data["isapproved"])
            }
            
            res = am.update_audio_meta(document_id,updateable_fields)
            return {"res":res}
        except ValueError:
            return {"Error":"missing key-value"},400
        
    def delete(self):
        data=request.json
        try:
            document_id = data["document_id"]
            res = am.delete_audio_meta(document_id)
            return res
        except ValueError as e:
            return {"Error":"missing key-value"},400
        
    