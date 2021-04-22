from conjoint_analysis.music_analyser import MusicAnalyser
from music_extraction.extract_music import SpotifyClient
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

class Runner:
    def __init__(self):
        self.extracter = SpotifyClient("./data/config.json")
        self.analyser = MusicAnalyser("./data/config.json") 
    
    def plot_history(self, history_df):
        """
            basic data exploration
        """
        # data spread
        print("\nData spread:")
        bin_data = self.analyser.bin_df(history_df)
        i = 1
        f = plt.figure(figsize=(15,15))
        for column in bin_data.columns:
            x = bin_data[column].value_counts().keys().values
            y = bin_data[column].value_counts().values
            _ = plt.subplot(3,3,i)
            plt.pie(y, labels=x)
            plt.title("Binned %s"%column)
            i += 1
        plt.show()
        
        # correlation
        print("\nCorrelation heatmap:")
        f = plt.figure(figsize=(10, 10))
        history_df = history_df[self.analyser.config["keys"]]
        mask = np.triu(np.ones_like(history_df.corr(), dtype=np.bool))
        heatmap = sns.heatmap(history_df.corr(), mask=mask, vmin=-1, vmax=1, annot=True, cmap='BrBG')
        plt.show()
        
    def plot_pw_df(self, pw_df):
        pass
    
    def run(self):
        history = self.extracter.load_user_history()
        self.plot_history(history)
        
        pp_history = self.analyser.preprocess_history(history)
        part_worths, attribute_importance, relative_importance = self.analyser.conjoint_analysis(pp_history)
        
        return history, pp_history, part_worths, attribute_importance, relative_importance
        
    def check(self, part_worths, song_list):
        history_df = self.extracter.make_history(song_list)
        return self.analyser.process_song_df(part_worths.values[0], history_df)
        
        
test1 = ["Sacrifice", "We're Good", "Prisoner", "Girls like you"]
        
