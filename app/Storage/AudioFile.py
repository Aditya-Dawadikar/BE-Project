import os
import librosa as lb
import soundfile as sf
from FirebaseSetup import fbs

from app.Storage.UniqueIdGenerator import generate_unique_string

bucket = fbs.getStorageBucket()

class AudioFile():
    def __init__(self):
        self.temp_path = 'temp_audios/'
        self.dest_path='audios/'
        pass
    
    def get_filename_from_url(self,url):
        # url: public URL of the file
        tokens= url.split('/')
        return tokens[-1]
    
    def get_file_path(self,filename):
        blob = bucket.get_blob(self.dest_path+filename)
        blob.make_public()
        return blob.public_url
        
    def upload_to_cloud(self,filename,src_path,dest_path):
        # saving all files by default to the temp storage in the cloud
        # src_path: local path of the file
        # dest_path: destination path of the file on the cloud
        blob = bucket.blob(dest_path+filename)
        blob.upload_from_filename(src_path+filename)
        blob.make_public()
        return blob.public_url
        
    def delete_from_cloud(self,filename):
        # delete audio file from cloud
        try:
            blob = bucket.blob(self.dest_path+filename)
            blob.delete()
            print("deleted ",filename)
        except Exception:
            raise Exception()
        
    def migrate(self,filename):
        # downloading it locally
        blob = bucket.get_blob(self.temp_path+filename)
        blob.download_to_filename('Temp/audio_from_cloud/'+filename)
        
        # upload the local file to destination bucket
        public_url=""
        try:
            public_url = self.upload_to_cloud(filename,'Temp/audio_from_cloud/',self.dest_path)
        except Exception as e:
            raise e
        
        # delete old file from cloud
        blob = bucket.blob(self.temp_path+filename)
        blob.delete()
        
        #delete file from local device
        os.remove('Temp/audio_from_cloud/'+filename)
        
        #return updated url for file
        return public_url