from sqlalchemy import Column, Integer, String, Float
from api.database import db
from datetime import datetime, timezone


Base = db.Base


class Track(Base):
    __tablename__ = "tracks"

    id = Column(Integer, primary_key=True, index=True)
    spotify_id = Column(String, unique=True, index=True)
    name = Column(String)
    genre = Column(String)
    danceability = Column(Float)
    energy = Column(Float)
    tempo = Column(Float)
    loudness = Column(Float)
    valence = Column(Float)

    def __init__(self, spotify_id,
                 name, genre, danceability,
                 energy, tempo, loudness, valence):
        self.spotify_id = spotify_id
        self.name = name
        self.genre = genre
        self.danceability = danceability
        self.energy = energy
        self.tempo = tempo
        self.loudness = loudness
        self.valence = valence


class PredictionResult(Base):
    __tablename__ = "prediction_results"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    spotify_id = Column(String, unique=True, index=True)
    predicted_genre = Column(String)
    confidence_score = Column(Float)
    prediction_date = datetime.now(timezone.utc)
    model_used = Column(String)
    test_data_id = Column(String)
    status = Column(String)
    notes = Column(String)

    def __init__(self, spotify_id,
                 predicted_genre, confidence_score,
                 model_used, test_data_id,
                 status, notes, name):
        self.name = name
        self.spotify_id = spotify_id
        self.predicted_genre = predicted_genre
        self.confidence_score = confidence_score
        self.model_used = model_used
        self.test_data_id = test_data_id
        self.status = status
        self.notes = notes


class PerformanceMetrics(Base):
    __tablename__ = "performance_metrics"

    id = Column(Integer, primary_key=True, index=True)
    model_used = Column(String)
    test_data_id = Column(String)
    trained_data_count = Column(Integer)
    tested_data_count = Column(Integer)
    accuracy = Column(Float)
    precision = Column(Float)
    recall = Column(Float)
    f1_score = Column(Float)
    timestamp = datetime.now(timezone.utc)

    def __init__(self, model_used, test_data_id,
                 trained_data_count, tested_data_count,
                 accuracy, precision=None,
                 recall=None, f1_score=None):
        self.model_used = model_used
        self.test_data_id = test_data_id
        self.trained_data_count = trained_data_count
        self.tested_data_count = tested_data_count
        self.accuracy = accuracy
        self.precision = precision
        self.recall = recall
        self.f1_score = f1_score
