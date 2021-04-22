from conjoint_analysis.music_analyser import MusicAnalyser
from music_extraction.extract_music import SpotifyClient

class Runner:
    def __init__(self):
        self.extracter = SpotifyClient("./data/config.json")
        self.analyser = MusicAnalyser("./data/config.json") 
        
    def run(self):
        history = self.extracter.make_df()
        pp_history = self.analyser.preprocess_history(history)
        part_worths = self.analyser.conjoint_analysis(pp_history)
        t = self.analyser.process_song_df(part_worths, history)
        
        return history, pp_history, part_worths, t
        
    