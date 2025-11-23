import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.db_connection import get_db_connection

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    """
    Fixture : Crée les tables et les vide avant chaque test.
    Ceci est crucial pour GitHub Actions où la DB est vierge.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Crée la table users
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        
        # Vide les tables
        cur.execute("DELETE FROM users;")
        conn.commit()
    finally:
        cur.close()
        conn.close()
    
    yield
    
    # Cleanup après le test
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM users;")
        conn.commit()
    finally:
        cur.close()
        conn.close()


def get_valid_token():
    """
    Helper : Crée un utilisateur et retourne son token
    """
    # Créer un utilisateur
    client.post(
        "/register/register",
        json={
            "username": "sentiment_test_user",
            "password": "test123"
        }
    )
    
    # Se connecter
    response = client.post(
        "/auth/login",
        json={
            "username": "sentiment_test_user",
            "password": "test123"
        }
    )
    
    return response.json()["token"]


def test_predict_sentiment_without_token():
    """
    Test : Essayer de prédire sans token → doit échouer
    """
    response = client.post(
        "/sentiment/predict",
        json={"text": "Ce produit est génial!"}
    )
    
    # Vérifier que ça échoue (status 422 ou 403)
    assert response.status_code in [422, 403]


def test_predict_sentiment_with_valid_token(mocker):
    """
    Test : Prédire avec un token valide → doit marcher
    """
    token = get_valid_token()
    
    # Mock de l'API HuggingFace
    mock_response = mocker.Mock()
    mock_response.json.return_value = [
        [
            {"label": "5 stars", "score": 0.85},
            {"label": "4 stars", "score": 0.10},
            {"label": "3 stars", "score": 0.03},
            {"label": "2 stars", "score": 0.01},
            {"label": "1 star", "score": 0.01}
        ]
    ]
    mock_response.status_code = 200
    
    mocker.patch('requests.post', return_value=mock_response)
    
    response = client.post(
        "/sentiment/predict",
        json={"text": "Ce produit est excellent!"},
        headers={"token": token}
    )
    
    assert response.status_code == 200
    assert "result" in response.json()


def test_get_data_with_valid_token():
    """
    Test : Accéder à /data/test avec un token valide
    """
    token = get_valid_token()
    
    response = client.get(
        "/data/test",
        headers={"token": token}
    )
    
    assert response.status_code == 200
    assert "user" in response.json()