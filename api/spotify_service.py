import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

RECOMMENDATIONS_LIMIT = 100

load_dotenv()


class SpotifyService:
    def __init__(self):
        self.client_id = os.getenv("SPOTIPY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
        self.client_credentials_manager = SpotifyClientCredentials(client_id=self.client_id, client_secret=self.client_secret)
        self.sp = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)

    def get_recommendations_for_genre(self, genre, 
                                      limit=RECOMMENDATIONS_LIMIT):
        recommendations = self.sp.recommendations(seed_genres=[genre],
                                                  limit=limit)
        track_tuples = [(track['id'], track['name']) 
                        for track in recommendations['tracks']]
        return track_tuples

    def get_audio_features(self, track_ids):
        valid_track_ids = [track_id for track_id in track_ids 
                           if isinstance(track_id, str) and track_id]
        if not valid_track_ids:
            return []
        features = self.sp.audio_features(valid_track_ids)
        return features

    def get_genre_tracks(self, genres):
        genres_tracks = {}
        for genre in genres:
            genres_tracks[genre] = self.get_recommendations_for_genre(genre)
        return genres_tracks


    def create_dataframe(self, genres):
        data = []

        genres_tracks = self.get_genre_tracks(genres)

        for genre, track_tuples in genres_tracks.items():
            track_ids = [track_id for track_id, _ in track_tuples]
            features = self.get_audio_features(track_ids)

            for (track_id, name), feature in zip(track_tuples, features):
                if feature:
                    track_data = {
                        'spotify_id': track_id,
                        'name': name,
                        'danceability': feature['danceability'],
                        'energy': feature['energy'],
                        'tempo': feature['tempo'],
                        'loudness': feature['loudness'],
                        'valence': feature['valence'],
                        'genre': genre
                    }
                    data.append(track_data)

        return pd.DataFrame(data)
