import json
import pandas as pd
import numpy as np
import math 

class MusicAnalyser():
    """ module used to perform Conjoint Anlaysis """
    def __init__(self, config_path):
        with open(config_path) as config_fp:
            self.config = json.load(config_fp)
        self.extracter = None
       
    # ignore
    def get_history_df(self):
        """
            Extract user's music history_df, previously created by extracter module.
        """
        try:
            history_df = pd.read_csv("../data/history.csv")
        except:
            #TODO: get this data from extracter ie) no. of columns and column names
            history_df = pd.DataFrame([[0]*(len(self.config.keys)+3)]).drop(0,0)
            history_df.columns = ["danceability","energy","loudness","speechiness",
                     "acousticness","instrumentalness","liveness","valence","tempo","rating","artist","track"]
        return history_df
    
    def bin_df(self, history_df):
        """
            Returns binned history dataframe.
        """
        max_val = self.config["max_val"]
        min_val = self.config["min_val"]
        history_df = history_df[self.config["keys"]]
        feature_index = 0
        key_len = len(self.config["keys"])
        for column in history_df.columns[:key_len]:
            q_bin = [min_val[feature_index]+i*(max_val[feature_index]-min_val[feature_index])/4-0.001 for i in range(5)]
            temp = pd.cut(history_df[column], bins=q_bin, labels=["Q1","Q2","Q3","Q4"])
            history_df[column] = temp
            feature_index+=1
        return history_df
    
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
        max_val = self.config["max_val"]
        min_val = self.config["min_val"]
        
        feature_index = 0
        key_len = len(self.config["keys"])
        for column in history_df.columns[:key_len]:
            q_bin = [min_val[feature_index]+i*(max_val[feature_index]-min_val[feature_index])/4-0.001 for i in range(5)]
            temp = pd.cut(history_df[column], bins=q_bin, labels=["Q1","Q2","Q3","Q4"])
            for new_column in [prefix+"_"+column for prefix in ["Q1","Q2","Q3","Q4"]]:
                pp_history[new_column] = (temp==new_column.split("_")[0]).astype(int)
            feature_index+=1
        pp_history["track_id"] = history_df["track_id"]
        pp_history["track_name"] = history_df["track_name"]
        return pp_history
    
    def conjoint_analysis(self, df):
        """
            find partworth vector based on user data.
            - attribute
                -level
                -level
                -level
            - attribute
                -level
                -level
        """
        
        df = df.drop(["track_id","track_name"],1)
        
        # STEP 1: multiply ratings/scores with columns
        for column in df.columns[1:]:
            # print(column)
            df[column] = df[column]*df["rating"]
        df = df.drop(["rating"],1)
        
        # STEP 2: find average
        average = pd.DataFrame([[0]*len(df.columns)], columns=df.columns)
        for column in df.columns:
            t = [val for val in df[column].values if val!=0]
            if t==[]:
                continue
            average[column] = np.mean(t)
            
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
        # part_worth = pd.DataFrame([pw_vector], columns = df.columns)
        
        # STEP 4: find attribute importance
        attribute_importance = []
        bin_ind = 0
        for attribute in self.config["keys"]:
            _bin = pw_vector[bin_ind*4:bin_ind*4+4]
            attribute_importance.append(_bin.max()-_bin.min())
            bin_ind += 1
        
        # STEP 5: relative importance
        relative_importance = np.array(attribute_importance)/np.sum(attribute_importance)*100
        
        attribute_importance = pd.DataFrame([attribute_importance], columns = self.config["keys"])
        relative_importance = pd.DataFrame([relative_importance], columns = self.config["keys"])
        
        return part_worth, attribute_importance, relative_importance
    
    def process_song_df(self, pw_vector, song_df):
        """
            Find part worth of each track and returns dataframe ordered by part_worth.
        """
        part_worth = []
        pp_df = self.preprocess_history(song_df)
        for song in pp_df.drop(["track_id","track_name"],1).values:
            part_worth.append(sum(pw_vector*song))
        pp_df["worth"] = part_worth
        if "rating" in pp_df.columns:
            pp_df = pp_df.drop(["rating"],1)
        return pp_df.sort_values(by=["worth"], ascending=False)
        