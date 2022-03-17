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
        pass

    def analyse(self,signaldata,samplingrate):
        
        print(len(signaldata),samplingrate)

        #step1: preprocessing
        #step2: feature extraction
        #step3: abnormality analysis
        #step4: disorder analysis
        #step5: severity analysis

        #step1: preprocessing
        #step1 a: resampling
        signaldata = lb.resample(y=signaldata, orig_sr=samplingrate, target_sr=22050)
        #step1 b: padding
        padded_segment=[]
        if len(signaldata)<(6*22050):
            padded_segment = lb.util.pad_center(signaldata, 6*22050)
        else:
            padded_segment = padded_segment[0:6*22050]
        #step1 c: filtering
        filtered_segment = np.array(preprocessor.get_filtered_segment(padded_segment,samplingrate=22050))
        
        #step2: feature extraction
        mfcc = featureExtractor.get_mfcc(filtered_segment,22050)
        spec = featureExtractor.get_mel_spectrogram(filtered_segment,22050)
        chroma_stft = featureExtractor.get_chroma_stft(filtered_segment,22050)
        
        mfcc_arr = np.array([mfcc])
        spec_arr = np.array([spec])
        chroma_stft_arr = np.array([chroma_stft])

        #step3: abnormality analysis
        abnormality_classes,abmormality_probabilities = abmormalityClassifier.predict(mfcc_arr,chroma_stft_arr,spec_arr) 
        #step4: disorder analysis
        disorder_classes,disorder_probabilities = disorderClassifier.predict(mfcc_arr,chroma_stft_arr,spec_arr)
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
