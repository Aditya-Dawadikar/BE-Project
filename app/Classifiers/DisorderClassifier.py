from tensorflow import keras
import json

class DisorderClassifier:
    def __init__(self):
        self.model = keras.models.load_model('C:/Users/Admin/Desktop/BE Project/Analytics Server/app/MLModels/disorder/mfcc_chroma_spec.h5')
        pass

    #This is Stub code
    def predict(self,mfcc_features,chroma_features,mel_spectrogram):
        # console.log(mfcc_features)
        out = self.model.predict({"mfcc":mfcc_features,"chroma":chroma_features,"mspec":mel_spectrogram})[0]
        print(type(out))
        probabilities = []
        for i in range( out.shape[0]):
            probabilities.append(round(float(out[i]),4))
        
        # return ['asthma','bronchial_disorders','copd','healthy','pneumonia'],[0.0001411,0.12141,0.685432,0.0012142,0.012411262]
        return ['asthma','bronchiectasis','bronchiolitis','fibrosis','healthy','pneumonia'],probabilities