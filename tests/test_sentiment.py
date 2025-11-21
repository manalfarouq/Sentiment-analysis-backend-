import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


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


def test_predict_sentiment_with_invalid_token():
    """
    Test : Essayer de prédire avec un faux token → doit échouer
    """
    response = client.post(
        "/sentiment/predict",
        json={"text": "Ce produit est génial!"},
        headers={"token": "fake_invalid_token"}
    )
    
    # Vérifier que ça échoue (status 401)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or expired token"


def test_predict_sentiment_with_valid_token():
    """
    Test : Prédire avec un token valide → doit marcher
    """
    token = get_valid_token()
    
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