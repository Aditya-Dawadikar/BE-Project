from app.Storage.UniqueIdGenerator import generate_unique_string
from FirebaseSetup import fbs

bucket = fbs.getStorageBucket()

class ReportFile():
    def __init__(self):
        self.dest_path='reports/'
        pass
    
    def upload_to_cloud(self,filename,src_path):
        blob = bucket.blob(self.dest_path+filename)
        blob.upload_from_filename(src_path+filename)
        blob.make_public()
        return blob.public_url
        
    def delete_pdf_file(self,filename):
        try:
            blob = bucket.blob(self.dest_path+filename)
            blob.delete()
            print("deleted ",filename)
        except Exception:
            raise Exception()
        
        