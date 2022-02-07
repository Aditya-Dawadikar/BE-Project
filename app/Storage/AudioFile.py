import os
import librosa as lb
import soundfile as sf
from app.Storage.UniqueIdGenerator import generate_unique_string
from FirebaseSetup import fbs

bucket = fbs.getStorageBucket()

class AudioFile():
    def __init__(self):
        self.temp_path = 'temp_audios/'
        self.dest_path='audios/'
        pass
    
    def upload_to_cloud(self,filename,src_path,dest_path):
        # saving all files by default to the temp storage in the cloud
        blob = bucket.blob(dest_path+filename)
        blob.upload_from_filename(src_path+filename)
        blob.make_public()
        return blob.public_url
    
    def standardize_data(self,signaldata,samplingrate):
        # standardization
        target_sr = 22050
        duration = 6
        resampled=lb.resample(y=signaldata, orig_sr=samplingrate, target_sr=target_sr)
        reqLen=duration*target_sr
            
        if len(resampled)<duration*target_sr:
            padded_data = lb.util.pad_center(resampled, reqLen)
            return padded_data,target_sr
        else:
            return resampled[0:reqLen],target_sr
            
    def save_audio_file(self,signaldata,samplingrate):
        temp_dest_path = 'C:/Users/Admin/Desktop/BE Project/Analytics Server/Temp/audios/'
        filename=generate_unique_string()+".wav"
        file = temp_dest_path+filename
        
        #standardizing the wav file
        std_raw,std_sr = self.standardize_data(signaldata,samplingrate)
        
        # writing to temp storage
        sf.write(file, std_raw, std_sr, 'PCM_24')
        
        #upload to cloud
        try:
            res = self.upload_to_cloud(filename,temp_dest_path,self.temp_path)
            return res
        except Exception:
            raise Exception()
        
    def delete_audio_file(self,filename):
        try:
            blob = bucket.blob(self.dest_path+filename)
            blob.delete()
            print("deleted ",filename)
        except Exception:
            raise Exception()
        
    def get_filename_from_url(self,filename):
        tokens= filename.split('/')
        return tokens[-1]
    
    def upload_audio(self,signaldata,samplingrate):
        fileurl = self.save_audio_file(signaldata,samplingrate)
        filename = self.get_filename_from_url(fileurl) 
        return filename
    
    def migrate_audio(self,filename):
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