import json
import pandas as pd
import numpy as np

class MusicAnalyser():
    """ module used to perform Conjoint Anlaysis """
    def __init__(self):
        with open("../data/config.json") as config_fp:
            self.config = json.load(config_fp)
        self.extracter = None
    
    def get_history_df(self):
        """
            #TODO: Update changes in module names.
            Extract user's music history_df, previously created by extracter module.
        """
        try:
            history_df = pd.read_csv("../data/history.csv")
        except:
            #TODO: get this data from extracter ie) no. of columns and column names
            history_df = pd.DataFrame([[0]*12]).drop(0,0)
            history_df.columns = ["danceability","energy","loudness","speechiness",
                     "acousticness","instrumentalness","liveness","valence","tempo","rating","artist","track"]
        return history_df
    
    def run_extracter(self):
        """
            #TODO: Update changes in module names.
            Create user's music history_df, by using spotipy queries.    
        """
        pass
    
    def preprocess_history(self, history_df):
        """
            Pre-process user's music history/search space dataframe to a form suitable for conjoint analysis.
            Quartile binning.
        """
        pp_history = pd.DataFrame()
        try:
            pp_history["rating"] = history_df["rating"]
        except:
            pass
        #TODO: get this data from extracter, data regarding max value for a feature, for quartile binning
        max_val = [10]*9
        feature_index = 0
        for column in history_df.columns[:9]:
            q_bin = [i*max_val[feature_index]/4 for i in range(5)]
            temp = pd.cut(history_df[column], bins=q_bin, labels=["Q1","Q2","Q3","Q4"])
            for new_column in [prefix+"_"+column for prefix in ["Q1","Q2","Q3","Q4"]]:
                pp_history[new_column] = (temp.iloc[:,0]==new_column.split("_")[0]).astype("int")
        pp_history["artist"] = history_df["artist"]
        pp_history["track"] = history_df["track"]
        return pp_history
    
    def conjoint_analysis(self, df):
        """
            find partworth vector based on user data.
        """
        
        df = df.drop(["rating","artist","track"],1)
        
        # STEP 1: multiple ratings/scores with columns
        for column in df.columns[-1:]:
            df[column] = df[column]*df["rating"]
        df = df.drop(["rating"],1)
        
        # STEP 2: find average
        average = pd.DataFrame()
        for column in df.columns:
            average[column] = np.mean([val for val in df[column].values() if val!=0])
        
        # STEP 3: find part_worth
        part_worth = pd.DataFrame()
        col_ind = 0
        bin_ind = -1
        for column in average.columns:
            if col_ind%4 == 0:
                bin_ind += 1
            part_worth[column] = average[column] - average.iloc[0,bin_ind*4:bin_ind*4+4].mean()
            col_ind += 1
        pw_vector = part_worth.values[0]
        
        return pw_vector
    
    def process_song_df(self, pw_vector, song_df):
        """
            Find part worth of each track and returns dataframe ordered by part_worth.
        """
        part_worth = []
        for song in song_df.iloc[:,:9].values:
            part_worth.append(pw_vector*song)
        song_df["part_worth"] = part_worth
        return song_df.sort_values(by=["part_worth"])
        