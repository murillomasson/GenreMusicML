from sqlalchemy.orm import Session
from api.models import Track, PredictionResult, PerformanceMetrics


class TrackCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create_track(self, track_data):
        existing_track = self.db.query(Track).filter(
            Track.spotify_id == track_data["spotify_id"]).first()
        if existing_track:
            return existing_track

        new_track = Track(
            spotify_id=track_data["spotify_id"],
            name=track_data["name"],
            genre=track_data["genre"],
            danceability=track_data["danceability"],
            energy=track_data["energy"],
            tempo=track_data["tempo"],
            loudness=track_data["loudness"],
            valence=track_data["valence"]
        )
        self.db.add(new_track)
        self.db.commit()
        self.db.refresh(new_track)
        return new_track

    def get_track_by_id(self, track_id: int):
        return self.db.query(Track).filter(Track.id == track_id).first()

    def get_all_tracks(self):
        return self.db.query(Track).all()

    def update_track(self, track_id: int, updated_data):
        track = self.get_track_by_id(track_id)

        if track:
            track.genre = updated_data.get("genre", track.genre)
            track.danceability = updated_data.get("danceability", track.danceability) # noqa: E501
            track.energy = updated_data.get("energy", track.energy)
            track.tempo = updated_data.get("tempo", track.tempo)
            track.loudness = updated_data.get("loudness", track.loudness)
            track.valence = updated_data.get("valence", track.valence)
            track.name = updated_data.get("name", track.name)

            self.db.commit()
            self.db.refresh(track)

        return track

    def delete_track(self, track_id: int):
        track = self.get_track_by_id(track_id)

        if track:
            self.db.delete(track)
            self.db.commit()

        return track

    def insert_prediction_result(self, prediction_data):
        existing_track = self.db.query(Track).filter(
            Track.spotify_id == prediction_data["spotify_id"]).first()
        print(prediction_data["spotify_id"])
        if not existing_track:
            new_track = Track(
                spotify_id=prediction_data["spotify_id"],
                genre=prediction_data.get("genre"),
                danceability=prediction_data.get("danceability"),
                energy=prediction_data.get("energy"),
                tempo=prediction_data.get("tempo"),
                loudness=prediction_data.get("loudness"),
                valence=prediction_data.get("valence"),
                name=prediction_data.get("name"),

            )
            self.db.add(new_track)
            self.db.commit()
            self.db.refresh(new_track)

        existing_prediction = self.db.query(PredictionResult).filter(PredictionResult.spotify_id == prediction_data["spotify_id"]).first() # noqa: E501

        if not existing_prediction:
            print(prediction_data)

            new_prediction = PredictionResult(
                spotify_id=prediction_data["spotify_id"],
                name=prediction_data["name"],
                predicted_genre=prediction_data["predicted_genre"],
                confidence_score=prediction_data["confidence_score"],
                model_used=prediction_data["model_used"],
                test_data_id=prediction_data["test_data_id"],
                status=prediction_data["status"],
                notes=prediction_data.get("notes")
            )
            self.db.add(new_prediction)
            self.db.commit()
            self.db.refresh(new_prediction)
            return new_prediction
        else:
            print(f"Prediction to spotify_id {prediction_data['spotify_id']} already exists") # noqa: E501
            return existing_prediction

    def insert_performance_metrics(self, model_used,
                                   test_data_id, trained_data_count,
                                   tested_data_count, accuracy,
                                   precision=None, recall=None,
                                   f1_score=None):
        performance_metrics = PerformanceMetrics(
            model_used=model_used,
            test_data_id=test_data_id,
            trained_data_count=trained_data_count,
            tested_data_count=tested_data_count,
            accuracy=accuracy,
            precision=precision,
            recall=recall,
            f1_score=f1_score
        )
        self.db.add(performance_metrics)
        self.db.commit()
        self.db.refresh(performance_metrics)
        return performance_metrics
