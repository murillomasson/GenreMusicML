import pytest
from api.database import Database


@pytest.fixture
def database():
    return Database()
# Teste para verificar se a conexão com base de dados ocorre com sucesso ou não
def test_database_connection(database):
    try:
        database.test_connection()
        connected = True
    except Exception as e:
        connected = False
    
    assert connected
