import os
import librosa as lb
import soundfile as sf
from app.Storage.UniqueIdGenerator import generate_unique_string

from app.Controllers.Utilities import util

class TempAudioFile():
    def __init__(self):
        self.temp_local_path = 'C:/Users/Admin/Desktop/BE Project/Analytics Server/Temp/audios/'
        pass
        
    def get_file_path(self,filename):
        # returns file path
        return self.temp_local_path+filename    
    
    def save_to_local_storage(self,signaldata,samplingrate):
        #save audio file to temporary storage on server
        filename=generate_unique_string()+".wav"
        file = self.temp_local_path+filename
        
        #standardizing the wav file
        std_raw,std_sr = util.standardize_data(signaldata,samplingrate)
        
        # writing to temp storage
        sf.write(file, std_raw, std_sr, 'PCM_24')
        return filename
        
    def delete_from_local_storage(self,filename):
        if os.path.exists(self.temp_local_path+filename):
            os.remove(self.temp_local_path+filename)
            return {
                "message": "file removed"
            }
        else:
            return {
                "message": "file does not exist"
            }
            
    