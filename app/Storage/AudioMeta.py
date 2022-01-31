import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from firebase_admin import credentials, initialize_app, firestore
from Config import storageconfig

from UniqueIdGenerator import generate_unique_string

# Init firebase with your credentials
cred = credentials.Certificate("../Config/be-project-4b4bf-firebase-adminsdk-wjqnp-4dd24d1742.json")
initialize_app(cred)

db = firestore.client()
collection = db.collection('audio_meta')

class AudioMeta:
    def __init__(self):
        pass
        
    def save_audio_meta(self,analysis_object):
        try:
            document_id=generate_unique_string()
            res = collection.document(document_id).set({
                "report_id":analysis_object["report_id"],
                "segmentname":analysis_object["segmentname"],
                "samplingrate":analysis_object["samplingrate"],
                "abnormality":analysis_object["abnormality"],
                "diagnosis":analysis_object["diagnosis"],
                "severity":analysis_object["severity"],
                "symptoms":analysis_object["symptoms"],
            })
            return res
        except Exception:
            raise Exception()
        
    def delete_audio_meta(self,document_id):
        try:
            res = collection.document(document_id).delete()
            return res
        except Exception:
            raise Exception()