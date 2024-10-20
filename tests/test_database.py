import pytest
from api.database import Database


@pytest.fixture
def database():
    return Database()

def test_database_connection(database):
    try:
        database.test_connection()
        connected = True
    except Exception as e:
        connected = False
    
    assert connected
