import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from app.Controllers import Utilities

utils=Utilities.Utilities()

class Classifier:
    def __init__(self):
        pass

class Classifier_Result(Classifier):
    def __init__(self):
        pass

    def get_plot_input(self,classes,probabilities):
        data = {
            "Class": classes,
            "Probability": probabilities
            }
    
        df = pd.DataFrame(data, columns=['Class', 'Probability'])
        return df

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

    def visualize_results(self,classes,probabilities):
        df = self.get_plot_input(classes,probabilities)
        plot = utils.wrap_to_bytesio(self.get_plot_result(df))
        return plot