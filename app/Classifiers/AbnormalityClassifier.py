from tensorflow import keras
import json

class AbnormalityClassifier:
    def __init__(self):
        self.model = keras.models.load_model('C:/Users/Admin/Desktop/BE Project/Analytics Server/app/MLModels/abnormality/abnormality_classifier_v1.h5')
        pass

    #This is Stub code
    def predict(self,mfcc_features,chroma_features,mel_spectrogram):
        all = self.model.predict(mfcc_features)
        out = self.model.predict(mfcc_features)[0]
        # print(type(out))
        probabilities = []
        for i in range( out.shape[0]):
            probabilities.append(round(float(out[i]),4))
        return ['crackles','wheezes','normal'],[0.0001411,0.12141,0.685432]
        # print(['crackles','normal','wheezes'])
        # print(probabilities)
        # return ['crackles','normal','wheezes'],probabilities