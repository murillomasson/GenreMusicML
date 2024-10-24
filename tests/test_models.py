import pytest
from api.spotify_service import SpotifyService


@pytest.fixture
def spotify_service():
    return SpotifyService()


def test_spotify_service_initialization(mocker, spotify_service):
    # Mockar o método de autenticação para verificar se a API é acessível
    mocker.patch.object(spotify_service.sp,
                        'recommendations',
                        return_value={'tracks': []})
    # Verifica se a instância foi criada e se a autenticação está funcionando
    assert spotify_service.client_id is not None
    assert spotify_service.client_secret is not None
    assert spotify_service.sp is not None


def test_get_recommendations(mocker, spotify_service):
    mock_recommendations = {
        'tracks': [{'id': '123', 'name': 'Test Track'}]
    }
    mocker.patch.object(spotify_service.sp,
                        'recommendations',
                        return_value=mock_recommendations)
    result = spotify_service.get_recommendations_for_genre('rock', limit=1)
    assert result == [('123', 'Test Track')]


def test_get_audio_features(mocker, spotify_service):
    mock_features = [{'danceability': 0.8, 'energy': 0.9}]
    mocker.patch.object(spotify_service.sp,
                        'audio_features',
                        return_value=mock_features)
    track_ids = ['123']
    result = spotify_service.get_audio_features(track_ids)
    assert result == mock_features
