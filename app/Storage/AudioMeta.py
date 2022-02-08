from app.Storage.UniqueIdGenerator import generate_unique_string
from FirebaseSetup import fbs
from app.Services.ResponseMessage import rm
collection = fbs.getAudioMetaCollection()

class AudioMeta:
    def __init__(self):
        pass
    
    def get_audio_meta_by_id(self,document_id):
        doc = collection.document(document_id).get()
        
        if doc.exists:
            return {"document":doc.to_dict()}
        else:
            return rm.dataNotFound()
        
    def get_all_audio_meta(self):
        doc = collection.stream()
        return doc
        
    def save_audio_meta(self,analysis_object):
        try:
            doc_id = analysis_object["filename"].split('.')[0]
            res = collection.document(doc_id).set({
                "filename":analysis_object["filename"],
                "abnormality":analysis_object["abnormality"],
                "disorder":analysis_object["disorder"],
                "severity":analysis_object["severity"],
                "symptoms":analysis_object["symptoms"],
            })
            return {
                "document_id":doc_id
            }
        except Exception as e:
            print(e)
        
    def update_audio_meta(self,document_id,updateable_fields):
        try:
            doc = collection.document(document_id)
            res = doc.update(updateable_fields)
            return {
                "document_id":document_id
            }
        except Exception as e:
            print(e)
        
    def delete_audio_meta(self,document_id):
        try:
            doc = collection.document(document_id).get()
            if doc.exists:
                doc.delete()
                return {
                    "message":"document deleted successfully"
                }
            else :
                return {
                        "message":"document not found"
                }
        except Exception as e:
            print(e)
            