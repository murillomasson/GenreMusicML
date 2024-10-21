import pytest
from api.database import Database


@pytest.fixture
def database():
    return Database()


def test_database_connection(database):
# Teste para verificar se a conexão com base de dados ocorre com sucesso ou não
    try:
        database.test_connection()
        connected = True
    except Exception:
        connected = False

    assert connected
