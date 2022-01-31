import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import librosa as lb
import soundfile as sf

from firebase_admin import credentials, initialize_app, storage
from Config import storageconfig

from UniqueIdGenerator import generate_unique_string

# Init firebase with your credentials
cred = credentials.Certificate("../Config/be-project-4b4bf-firebase-adminsdk-wjqnp-4dd24d1742.json")
initialize_app(cred,{'storageBucket': storageconfig.firebaseConfig["storageBucket"]})

bucket = storage.bucket()

class AudioFile():
    def __init__(self):
        self.dest_path='audios/'
        pass
    
    def upload_to_cloud(self,filename,src_path):
        blob = bucket.blob(self.dest_path+filename)
        blob.upload_from_filename(src_path+filename)
        blob.make_public()
        return blob.public_url
    
    def standardize_data(self,signaldata,samplingrate):
        # standardization
        target_sr = 22050
        duration = 6
        reqLen=duration*target_sr
        resampled=lb.resample(y=signaldata, orig_sr=samplingrate, target_sr=target_sr)
        padded_data = lb.util.pad_center(resampled, reqLen)
        return padded_data,target_sr
    
    def save_audio_file(self,signaldata,samplingrate):
        temp_dest_path = '../../Temp/audios/'
        filename=generate_unique_string()+".wav"
        file = temp_dest_path+filename
        
        #standardizing the wav file
        std_raw,std_sr = self.standardize_data(signaldata,samplingrate)
        
        # writing to temp storage
        sf.write(file, std_raw, std_sr, 'PCM_24')
        
        #upload to cloud
        try:
            res = self.upload_to_cloud(filename,temp_dest_path)
            print(res)
        except Exception:
            raise Exception()
        
    def delete_audio_file(self,filename):
        try:
            blob = bucket.blob(self.dest_path+filename)
            blob.delete()
            print("deleted ",filename)
        except Exception:
            raise Exception()
        
        