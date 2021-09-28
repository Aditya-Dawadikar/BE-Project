import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from app.Controllers import Utilities,Preprocessor,FeatureExtractor
from app.Classifiers import Abnormality_classifier, Disorder_classifier

utils=Utilities.Utilities()
preprocessor = Preprocessor.Preprocessor()
featureExtractor = FeatureExtractor.FeatureExtractor()

class Classifier_Preprocessor:
    def __init__(self):
        pass

    # A Preprocessing pipeline for model input
    # 1. downsampling the original signal to 8000Hz
    # 2. 3 layer filter
    #   2.a harmonic component
    #   2.b wavelet denoise filter
    #   2.c bandpass filter
    #   2.d removal of FFT induced frequencies
    # 3. feature extraction
    #   3.a MFCC
    #   3.b chroma stft
    #   3.c mel spectrogram 
    def get_model_input(self,signaldata,samplingrate):
        #down sample signal
        downsampled = utils.resample(signaldata,samplingrate,utils.resamp_rate)
        #preprocess data
        preprocessed_data=preprocessor.get_filtered_segment(downsampled,utils.resamp_rate)
        #extract features
        mfcc_features=preprocessor.get_mfcc(preprocessed_data,utils.resamp_rate)
        chroma_features=preprocessor.get_chroma_stft(preprocessed_data,utils.resamp_rate)
        melspectorgram_features=preprocessor.get_mel_spectrogram(preprocessed_data,utils.resamp_rate)
        #return features model input
        return (mfcc_features,chroma_features,mel_spectrogram)

class Abnormality_classifier_wrapper:
    def __init__(self):
        self.preprocessor = Classifier_Preprocessor()
        self.abnormality_classifier = Abnormality_classifier.Abnormality_classifier()
        pass
    
    # A warpper for Proprocessor and Abnormality classifier
    def predict(self,signaldata,samplingrate):
        mfcc_features,chroma_features,mel_spectrogram = self.preprocessor.get_model_input(signaldata,samplingrate)
        classes,results=self.abnormality_classifier.predict(mfcc_features,chroma_features,mel_spectrogram)
        return classes,results

class Disorder_classifier_wrapper:
    def __init__(self):
        self.preprocessor = Classifier_Preprocessor()
        self.disorder_classifier = Disorder_classifier.Disorder_classifier()
        pass
    
    # A warpper for Proprocessor and disorder classifier
    def predict(self,signaldata,samplingrate):
        mfcc_features,chroma_features,mel_spectrogram = self.preprocessor.get_model_input(signaldata,samplingrate)
        classes,results=self.disorder_classifier.predict(mfcc_features,chroma_features,mel_spectrogram)
        return classes,results

class Classifier_Result:
    def __init__(self):
        pass

    #creates a dataframe compatible with sns horizontal bar plot
    def get_plot_input(self,classes,probabilities):
        data = {
            "Class": classes,
            "Probability": probabilities
            }
    
        df = pd.DataFrame(data, columns=['Class', 'Probability'])
        return df

    #creates a horizontal bar plot
    def get_plot_result(self,df):
        fig, ax = plt.subplots(figsize = (9,8))
        ax=sns.barplot(x = df.columns[1], y = df.columns[0], data = df,color='r',)
        ax.set_xlim([0,1])
        ax.set_xlabel("Probability",fontsize=20)
        ax.set_ylabel("Class",fontsize=20)
        ax.tick_params(axis='both', which='major', labelsize=15)
        ax.tick_params(axis='both', which='minor', labelsize=15)
        for p in ax.patches:
            plt.text(
                        p.get_width()+0.02, #horizontal padding:0.02
                        p.get_y()+p.get_height()/2, #vertical padding:p.get_height/2
                        s=f"{round(p.get_width(),2)%100}"+"%", #rounding off to 2 decimal places and converting to percentage
                        ha='left', 
                        va='center',
                        fontsize='x-large'
                    )
        return plt

    #A wrapper for generation input dataframe and horizontal bar plot 
    def visualize_results(self,classes,probabilities):
        df = self.get_plot_input(classes,probabilities)
        plot = utils.wrap_to_bytesio(self.get_plot_result(df))
        return plot