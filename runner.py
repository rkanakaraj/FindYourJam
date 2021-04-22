from conjoint_analysis.music_analyser import MusicAnalyser
from music_extraction.extract_music import SpotifyClient
import seaborn as sns
import numpy as np
import pandas as pd
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
        
        print("\n\n*************************\n\
              Exploring User's liked songs\n*************************")
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
        
    def plot_analysis(self, pw, ri):
        print("\n\n*************************\n\
              Analysing User's liked songs\n*************************")
        attributes = sum([[i]*4 for i in ri.columns],[])
        levels = pw.columns
        
        work_space = pd.DataFrame({"attributes":attributes, "levels":levels, "part_worth":pw.values[0]})

        print("\nPart worth of levels:")
        f = plt.figure(figsize=(10, 10))
        sns.barplot(y="levels", x="part_worth", data = work_space, hue="attributes", 
                    dodge=False)
        plt.legend(bbox_to_anchor=(1, 1), loc=2)
        plt.show()
        
        print("\nRelative importance of attributes:")
        relative_imp = pd.DataFrame({"attributes":ri.columns, "relative_importance":ri.values[0]})
        f = plt.figure(figsize=(8, 8))
        sns.barplot(x="attributes", y="relative_importance", data = relative_imp, dodge=False)
        plt.xticks(rotation=45)
        plt.show()
        
        
    def plot_test(self, utility_df):
        """
            Exploring test data
        """
        print("\nUtility worths of playlist:\n","; ".join(utility_df["track_name"]).strip("; "))
        f = plt.figure(figsize=(8, 8))
        sns.barplot(x="track_name", y="worth", data=utility_df)
        # print(utility_df["worth"].sum())
        plt.xticks(rotation=45)
        plt.show()
    
    
    def run(self):
        history = self.extracter.load_user_history()
        self.plot_history(history)
        
        pp_history = self.analyser.preprocess_history(history)
        part_worths, attribute_importance, relative_importance = self.analyser.conjoint_analysis(pp_history)
        self.plot_analysis(part_worths, relative_importance)
        
        return history, pp_history, part_worths, relative_importance
        
    def check(self, part_worths, song_list):
        history_df = self.extracter.make_history(song_list)
        u_df = self.analyser.process_song_df(part_worths.values[0], history_df)
        return u_df
    
    def run_tests(self, part_worths, song_lists):
        print("\n\n*************************\n\
              Checking Worth of playlist\n*************************")
        worth_list = []
        # index = 0
        for song_list in song_lists:
            worth = self.check(part_worths, song_list)
            self.plot_test(worth)
            worth_list.append(worth["worth"].mean()) #TODO: mean or sum?
            # index += 1
        print("\nMost valuable playlist is playlist number: ", worth_list.index(max(worth_list))+1)
        return worth_list

# add song names of playlist to check its worth
playlists = [["Sacrifice", "We're Good", "Prisoner", "Girls like you", "anywhere","genius"],
             ["Never say never","too good at goodbyes", "six feet under", "play date", "royals"],
             ["nails, hair, hips, heels", "soulmate", "peaches"]]

#usage
# r = Runner()
# history, pp_history, part_worths, relative_importance = r.run() # user's liked songs are processed
# _ = r.run_tests(part_worths, playlists) # worth of playlists according to the user

        
