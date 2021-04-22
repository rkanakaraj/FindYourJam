from conjoint_analysis.music_analyser import MusicAnalyser
from music_extraction.extract_music import SpotifyClient
import seaborn as sns
import matplotlib.pyplot as plt

class Runner:
    def __init__(self):
        self.extracter = SpotifyClient("./data/config.json")
        self.analyser = MusicAnalyser("./data/config.json") 
    
    def plot_history(self, history_df):
        
        # basic data exploration
        _ = sns.pairplot(history_df.iloc[:,:9]) #, diag_kind="kde")
        plt.title("Data exploration")
        plt.show()
        
        # sns.distplot(history_df["rating"])
        # plt.title("User rating histogram")
        # plt.show()
        
        
        
    def plot_pw_df(self, pw_df):
        pass
    
    def run(self):
        history = self.extracter.load_user_history()
        self.plot_history(history)
        
        pp_history = self.analyser.preprocess_history(history)
        part_worths, attribute_importance, relative_importance = self.analyser.conjoint_analysis(pp_history)
        # t = self.analyser.process_song_df(part_worths, history)
        
        return history, pp_history, part_worths, attribute_importance, relative_importance
        
    def check(self, part_worths, song_list):
        history_df = self.extracter.make_history(song_list)
        return self.analyser.process_song_df(part_worths.values[0], history_df)
        
        
test1 = ["Sacrifice", "We're Good", "Prisoner", "Girls like you"]
        
