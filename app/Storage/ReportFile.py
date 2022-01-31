import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import PyPDF2

from firebase_admin import credentials, initialize_app, storage
from Config import storageconfig

from UniqueIdGenerator import generate_unique_string

# Init firebase with your credentials
cred = credentials.Certificate("../Config/be-project-4b4bf-firebase-adminsdk-wjqnp-4dd24d1742.json")
initialize_app(cred,{'storageBucket': storageconfig.firebaseConfig["storageBucket"]})

bucket = storage.bucket()

class AudioFile():
    def __init__(self):
        self.dest_path='reports/'
        pass
    
    def upload_to_cloud(self,filename,src_path):
        blob = bucket.blob(self.dest_path+filename)
        blob.upload_from_filename(src_path+filename)
        blob.make_public()
        return blob.public_url
    
    # def save_pdf_file(self,file):
    #     temp_dest_path = '../../Temp/reports/'
    #     filename=generate_unique_string()+".pdf"
    #     file = temp_dest_path+filename
        
        # writing to temp storage
        
        
        #upload to cloud
    #     try:
    #         res = self.upload_to_cloud(filename,temp_dest_path)
    #         print(res)
    #     except Exception:
    #         raise Exception()
        
    def delete_pdf_file(self,filename):
        try:
            blob = bucket.blob(self.dest_path+filename)
            blob.delete()
            print("deleted ",filename)
        except Exception:
            raise Exception()
        
        