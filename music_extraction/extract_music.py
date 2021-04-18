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
        
        To download Spotify's Million Playlist dataset follow the link below:
        https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge/
    """
    def __init__(self, config_path):
        # data containers
        with open(config_path) as f:
            self.config = json.load(f)
        self.track_ids = []
        self.embeddings = []
        self.track_names = []
        self.order_list = []
        self.cm_playlist_id = -1 # last completed playlist id
        self.keys = ["danceability","energy","loudness","speechiness",
                     "acousticness","instrumentalness","liveness","valence","tempo"]
        
        # client setup
        self.client_credentials_manager = SpotifyClientCredentials(client_id=self.config["client_id"], 
                                                                   client_secret=self.config["client_secret"])
        self.sp = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)
    


    def get_track_by_name(self, track_name, n_count=10):
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
    
config_path = "config.json" #"YOUR CONFIG PATH"

sp = SpotifyClient(config_path)

song_list = ["Levitating", "perfect", "cross me"]
for song in song_list:
    track = sp.get_track_by_name(song)['items'][0]
    track_id = track['id']
    features = sp.get_audio_features([track_id])
    for i in range(len(features)):
        temp = []
        temp.extend([features[i][key] for key in sp.keys])
        temp.extend([track_id, song])
        sp.embeddings.append(temp)

df = pd.DataFrame(sp.embeddings, columns = ["danceability","energy","loudness","speechiness",
                     "acousticness","instrumentalness","liveness","valence","tempo","track_id","track_name"])
df.to_csv("SongFeatures.csv")