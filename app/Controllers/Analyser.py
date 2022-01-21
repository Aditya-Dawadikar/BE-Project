import numpy as np
import librosa as lb

from app.Controllers import Utilities,Preprocessor,FeatureExtractor
from app.Classifiers import AbnormalityClassifier, DisorderClassifier

utils=Utilities.Utilities()
preprocessor = Preprocessor.Preprocessor()
featureExtractor = FeatureExtractor.FeatureExtractor()
abmormalityClassifier = AbnormalityClassifier.AbnormalityClassifier()
disorderClassifier = DisorderClassifier.DisorderClassifier()

class Analyser:
    def __init__(self):
        self.samplingrate=22050
        pass

    def analyse(self,signaldata,samplingrate):

        #step1: preprocessing
        #step2: feature extraction
        #step3: abnormality analysis
        #step4: disorder analysis
        #step5: severity analysis

        #step1: preprocessing
        print(type(signaldata))
        if samplingrate != self.samplingrate:
            signaldata = lb.resample(y=signaldata, orig_sr=samplingrate, target_sr=self.samplingrate)
            
        signaldata= np.array(signaldata)

        padded_segment = preprocessor.get_padded_segment(signaldata,samplingrate=self.samplingrate)
        filtered_segment = preprocessor.get_filtered_segment(signaldata,samplingrate=self.samplingrate)

        #step2: feature extraction
        mfcc = featureExtractor.get_mfcc(signaldata,self.samplingrate)
        spec = featureExtractor.get_mel_spectrogram(signaldata,self.samplingrate)
        chroma_stft = featureExtractor.get_chroma_stft(signaldata,self.samplingrate)

        #step3: abnormality analysis
        abnormality_classes,abmormality_probabilities = abmormalityClassifier.predict(mfcc,chroma_stft,spec) 
        #step4: disorder analysis
        disorder_classes,disorder_probabilities = disorderClassifier.predict(mfcc,chroma_stft,spec)
        #step5: severity analysis

        abnormality_object = {}
        for i,c in enumerate(abnormality_classes):
            abnormality_object[c] = abmormality_probabilities[i]

        disorder_object = {}
        for i,c in enumerate(disorder_classes):
            disorder_object[c] = disorder_probabilities[i]

        result={
            "abnormality":abnormality_object,
            "disorder":disorder_object,
            "severity": 1
        }
        return result
