import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import os
import time
import pandas as pd
import numpy as np

class SpotifyClient():
    """
        Uses spotipy api to work on Spotify's Million Playlist dataset.
        
        To create client_id and client_secret follow the link given below:
        https://developer.spotify.com/documentation/general/guides/app-settings/
    """
    def __init__(self, config_path):
        with open(config_path) as f:
            self.config = json.load(f)
        self.keys = self.config["keys"]
        
        # client setup
        self.client_credentials_manager = SpotifyClientCredentials(client_id=self.config["client_id"], 
                                                                   client_secret=self.config["client_secret"])
        self.sp = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)
    


    def get_track_by_name(self, track_name, n_count=2):
            """
                Returns list of tracks.
                Each track is a dictionary
            """
            return self.sp.search(q=track_name,type="track",limit=n_count)["tracks"]
    
    def get_track_by_id(self, track_id):
        """
            Returns a track as dictionary
        """
        return self.sp.track(track_id)
    
    def get_audio_features(self, track_ids):
        """
           track_ids - list of track_ids (limit len(track_ids)<=100)
           Returns list of audio features corresponding to track_ids
        """
        return self.sp.audio_features(track_ids)
    
    def load_user_songs(self):
        return [i[0] for i in self.config["songs"]]
    
    def load_user_rating_map(self):
        return self.config["songs"]
    
    def make_history(self, song_list):
        df_list = []
        for track_name in song_list:
            track = self.get_track_by_name(track_name)['items'][0]
            track_id = track['id']
            temp = [track_id, track_name]
            features = self.get_audio_features([track_id])[0]
            temp = [features[key] for key in self.keys] + temp
            df_list.append(temp)
        df = pd.DataFrame(df_list, columns = self.keys+["track_id", "track_name"])
        return df 
    
    def load_user_history(self):
        df_list = []
        for track_name, rating in self.config["songs"]:
            track = self.get_track_by_name(track_name)['items'][0]
            track_id = track['id']
            temp = [track_id, track_name, rating]
            features = self.get_audio_features([track_id])[0]
            temp = [features[key] for key in self.keys] + temp
            df_list.append(temp)
        df = pd.DataFrame(df_list, columns = self.keys+["track_id", "track_name", "rating"])
        return df 
