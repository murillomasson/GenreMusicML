import pytest
import pandas as pd
from unittest.mock import MagicMock
from api.ml_models import MLModel


@pytest.fixture
def mock_track_crud():
    return MagicMock()

@pytest.fixture
def model(mock_track_crud):
    return MLModel(track_crud=mock_track_crud)

@pytest.fixture
def sample_data():
    data = {
        'danceability': [0.5, 0.6, 0.8, 0.9],
        'energy': [0.7, 0.8, 0.5, 0.6],
        'tempo': [120, 130, 140, 150],
        'loudness': [-5, -3, -7, -2],
        'valence': [0.8, 0.9, 0.7, 0.6],
        'genre': ['rock', 'pop', 'jazz', 'rock'],
        'name': ['Track1', 'Track2', 'Track3', 'Track4']
    }
    return pd.DataFrame(data), data['name'], ['spotify_id_1', 'spotify_id_2', 'spotify_id_3', 'spotify_id_4']

def test_train(model, mock_track_crud, sample_data):
    df, track_names, spotify_ids = sample_data
    model.train(df, spotify_ids)

    # Verifique se o modelo foi treinado
    assert model.model is not None
    assert model.scaler is not None

    # Verifique se os resultados foram salvos
    assert mock_track_crud.insert_prediction_result.call_count > 0
    assert mock_track_crud.insert_performance_metrics.call_count == 1

def test_predict(model):
    # Configure o modelo para que ele possa prever
    model.scaler = MagicMock()
    model.model = MagicMock()
    model.encoder = MagicMock()

    model.scaler.transform.return_value = [[0.0]]  # Simulação da saída do scaler
    model.model.predict.return_value = [1]  # Simulação de previsão
    model.model.predict_proba.return_value = [[0.2, 0.8]]  # Simulação de probabilidade
    model.encoder.inverse_transform.return_value = ['pop']  # Simulação do gênero previsto

    track_data = {
        "danceability": 0.5,
        "energy": 0.6,
        "tempo": 120,
        "loudness": -5,
        "valence": 0.8
    }

    result = model.predict(track_data)

    assert result["predicted_genre"] == "pop"
    assert result["confidence_score"] == 0.8
    assert result["model_used"] == model.model_name
    assert result["status"] == "success"

def test_predict_no_scaler(model):
    track_data = {
        "danceability": 0.5,
        "energy": 0.6,
        "tempo": 120,
        "loudness": -5,
        "valence": 0.8
    }

    with pytest.raises(Exception):
        model.predict(track_data)
