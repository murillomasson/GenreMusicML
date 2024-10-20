from sqlalchemy.orm import sessionmaker
from api.crud import TrackCRUD
from api.models import Track
from api.database import db
import pytest


@pytest.fixture
def session():
    Session = sessionmaker(bind=db.engine)
    return Session()


@pytest.fixture
def track_crud(session):
    return TrackCRUD(session)

# Teste de asserção para verificar que um objeto track foi criado corretamente
def test_create_track(track_crud):
    track_data = {
        "spotify_id": "12345",
        "name": "Test Track",
        "genre": "Rock",
        "danceability": 0.8,
        "energy": 0.9,
        "tempo": 120,
        "loudness": -5.0,
        "valence": 0.6
    }
    
    track = track_crud.create_track(track_data)
    
    assert track.spotify_id == track_data['spotify_id']
    assert track.name == track_data['name']
    assert track.genre == track_data['genre']
    assert track.danceability == track_data['danceability']
    assert track.energy == track_data['energy']
    assert track.tempo == track_data['tempo']
    assert track.loudness == track_data['loudness']
    assert track.valence == track_data['valence']


def test_get_track_by_id(track_crud, session):
    track = session.query(Track).first()
    
    if track:
        fetched_track = track_crud.get_track_by_id(track.id)
        assert fetched_track.id == track.id
    else:
        pytest.skip("No tracks found for testing")
