import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.db_connection import get_db_connection

client = TestClient(app)


@pytest.fixture(autouse=True)
def cleanup():
    """
    Nettoie la base de données après chaque test
    """
    yield
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username = 'sentiment_test_user'")
        conn.commit()
        cursor.close()
        conn.close()
    except Exception:
        pass


def get_valid_token():
    """
    Fonction helper : Crée un utilisateur et retourne son token
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
    
    # Vérifier que ça échoue (status 422 car token manquant)
    assert response.status_code == 422


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
    
    # Vérifier que ça marche
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
    
    # Vérifier que ça marche
    assert response.status_code == 200
    assert "user" in response.json()