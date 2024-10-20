from api.database import db
from api.crud import TrackCRUD
from api.ml_models import MLModel  
from sqlalchemy.exc import OperationalError
from api.spotify_service import SpotifyService
import pandas as pd
import uuid

GENRES_LIMITS_API = 5

def create_tables_if_not_exists():
    try:
        db.Base.metadata.create_all(bind=db.engine)
        print("Tables created successfully.")
    except OperationalError as e:
        print(f"Error creating tables: {e}")


class SpotifyPipeline:
    def __init__(self, session):
        self.track_crud = TrackCRUD(session)
        self.spotify_service = SpotifyService()


    def insert_tracks_from_spotify(self, genres):
        df = self.spotify_service.create_dataframe(genres)
        print(f"Retrieved {len(df)} tracks with audio features.")

        data = df.to_dict(orient='records')

        for track_data in data:
            track_id = track_data.get('spotify_id')
            name = track_data.get('name', 'Unknown')
            genre = track_data.get('genre')

            print(f"Track {name} (ID: {track_id}) processed.")
            prediction_data = {
                "spotify_id": track_id,
                "name": name,
                "genre": genre,
                "danceability": track_data['danceability'],
                "energy": track_data['energy'],
                "tempo": track_data['tempo'],
                "loudness": track_data['loudness'],
                "valence": track_data['valence'],
                "predicted_genre": None,
                "confidence_score": None,
                "model_used": None,
                "test_data_id": str(uuid.uuid4()),
                "status": None,
                "notes": None
            }

            self.track_crud.insert_prediction_result(prediction_data)

        print(f"Inserted {len(data)} tracks into the database.")


    def train_model(self):
        tracks = self.track_crud.get_all_tracks()
        ml_model = MLModel(self.track_crud)

        if tracks:
            data = {
                "spotify_id": [],
                "danceability": [],
                "energy": [],
                "tempo": [],
                "loudness": [],
                "valence": [],
                "genre": []
            }
            track_data = []

            for track in tracks:
                data["spotify_id"].append(track.spotify_id)
                data["danceability"].append(track.danceability)
                data["energy"].append(track.energy)
                data["tempo"].append(track.tempo)
                data["loudness"].append(track.loudness)
                data["valence"].append(track.valence)
                data["genre"].append(track.genre)

                track_data.append({
                    "spotify_id": track.spotify_id,
                    "name": track.name,
                    "genre": track.genre,
                    "danceability": track.danceability,
                    "energy": track.energy,
                    "tempo": track.tempo,
                    "loudness": track.loudness,
                    "valence": track.valence
                })               

            df = pd.DataFrame(data)

            print(f"Training model with {len(df)} tracks.")

            if 'genre' in df.columns and not df.empty:
                accuracy, precision, recall, f1 = ml_model.train(df.drop(columns=["spotify_id"]), df['genre'], track_data)
                return ml_model, accuracy, precision, recall, f1
            
        print("No tracks available for training.")
        return None, None, None, None, None


    def predict_and_save_results(self, ml_model):
        tracks = self.track_crud.get_all_tracks()

        for track in tracks:
            prediction_data = ml_model.predict({
                "danceability": track.danceability,
                "energy": track.energy,
                "tempo": track.tempo,
                "loudness": track.loudness,
                "valence": track.valence
            })

            predicted_genre = prediction_data["predicted_genre"]
            actual_genre = track.genre

            prediction_result_data = {
                "spotify_id": track.spotify_id,
                "predicted_genre": predicted_genre,
                "confidence_score": float(prediction_data["confidence_score"]),
                "model_used": prediction_data["model_used"],
                "test_data_id": prediction_data["test_data_id"],
                "status": prediction_data["status"],
                "notes": prediction_data.get("notes"),
                "name": track.name
            }

            new_prediction = self.track_crud.insert_prediction_result(prediction_result_data)
            print(f"Prediction for track '{track.name}' inserted successfully: {new_prediction.predicted_genre}")

        self.insert_performance_metrics(ml_model)


    def insert_performance_metrics(self, ml_model):
        self.track_crud.insert_performance_metrics(
            test_data_id=str(uuid.uuid4()),
            trained_data_count=len(ml_model.y_train),
            tested_data_count=len(ml_model.y_test),
            accuracy=ml_model.accuracy,
            precision=ml_model.precision,
            recall=ml_model.recall,
            f1_score=ml_model.f1_score
        )

def main_insert_tracks(genres):
    create_tables_if_not_exists()
    
    with db.get_session() as session:
        pipeline = SpotifyPipeline(session)
        pipeline.insert_tracks_from_spotify(genres)


def main_train_and_predict(genres):
    create_tables_if_not_exists()
    
    with db.get_session() as session:
        pipeline = SpotifyPipeline(session)

        ml_model, accuracy, precision, recall, f1 = pipeline.train_model()
        
        if ml_model:
            pipeline.predict_and_save_results(ml_model)


if __name__ == "__main__":
    genres = ['rock', 'pop', 'jazz', 'hip-hop', 'classical']

    #main_insert_tracks(genres)
    main_train_and_predict(genres)
