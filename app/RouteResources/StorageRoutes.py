from flask import request,jsonify
from flask_restful import Resource

from app.Services.ResponseMessage import rm
from app.Controllers.ReportGenerator import PDF
from app.Storage.AudioMeta import AudioMeta
from app.Storage.AudioFile import AudioFile
from app.Storage.ReportFile import ReportFile
from app.Services.GraphPlotter import GraphPlotter

import os
import librosa as lb

am = AudioMeta()
af = AudioFile()
rf = ReportFile()
    
class AudioMetaResource(Resource):
    
    def get(self):
        data = request.json
        try:
            res = am.get_audio_meta_by_id(data["document_id"])
            return res
        except ValueError:
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
        except ValueError:
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
        
    
class SaveData(Resource):
    
    def deleteFile(self,filepath):
        os.remove(filepath)
        # if os.path.exists(filepath):
        #     os.remove(filepath)
        # else:
        #     raise FileNotFoundError()
    
    def post(self):
        data = request.json
        try:
            # report related data
            doctor_info = data["doctor_info"]
            patient_info = data["patient_info"]
            report_summary = data["report_summary"]
            report_note = data["report_note"]
            symptoms = data["symptoms"]
            mode=data["mode"]
            # audio filename
            audio_segments = data["audio_segments"]
            # audio_segments:[
            #     {
            #         filename:String,                              # local filename given by the server
            #         abnormality:{classes:[],probabilities:[]},    # final abnormality suggested/approved by clinician
            #         disorder:{classes:[],probabilities:[]},       # final disorder diagnosed/approved by clinician
            #         severity:Number,                              # final severity diagnosed/approved by clinician
            #         symptoms:String                               # clinician reasoning for diagnosis
            #     },...
            # ]
        except ValueError:
            return {"Error":"missing key-value"},400
        
        # Performing final data archiving process and report generation
        # 0. extracting images for report
        audio_base_path = 'C:/Users/Admin/Desktop/BE Project/Analytics Server/Temp/audios/'
        for i,segment in enumerate(audio_segments):
            filename = segment["filename"]
            signaldata,samplingrate = lb.load(audio_base_path+filename)
            gp1 = GraphPlotter()
            gp2 = GraphPlotter()
            waveform_url = gp1.timeseries(signaldata)
            spectrogram_url = gp2.spectrogram(signaldata, samplingrate)
            
            #adding image url to each segment
            audio_segments[i]["images"] = {
                "waveform_url":waveform_url,
                "spectrogram_url":spectrogram_url
            }
        
        # 1. exporting report
        report = PDF('P', 'mm', 'A4')
        report_id = report.export(doctor_info,patient_info,report_summary,report_note,audio_segments)
        
        # 2. uploading audio files to cloud
        docs=[]
        for i,segment in enumerate(audio_segments):
            filename = segment["filename"]
            url = af.upload_to_cloud(filename=filename,src_path='Temp/audios/',dest_path=af.dest_path)
            audio_segments[i]["url"]=url
            
            #delete audio files from local machine
            delete_path = "Temp/audios/"+filename
            self.deleteFile(delete_path)
            
            #deleting images from local storage
            delete_path = segment["images"]["waveform_url"]
            self.deleteFile(delete_path)
            delete_path = segment["images"]["spectrogram_url"]
            self.deleteFile(delete_path)
            
            #removing images url from the segment object
            del segment["images"]
            
            # add new document to required collection
            newdoc = am.save_audio_meta(analysis_object=segment, type=mode)
            docs.append(newdoc)
            
        # 3. upload report to the cloud
        report_src = 'C:/Users/Admin/Desktop/BE Project/Analytics Server/Temp/reports/'
        report_public_url = rf.upload_to_cloud(filename=report_id,src_path=report_src)
        
        # 4. remove report from local storage
        self.deleteFile(report_src+report_id)
        
        res_object={
            "report_public_url":report_public_url,
            "segment_information":docs
        }
        return res_object