import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.db_connection import get_db_connection

# Créer un client de test
client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_users_table():
    """
    Cette fixture est exécutée automatiquement avant chaque test.
    Elle vide la table 'users' pour éviter les conflits.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users;")  # Supprime tous les utilisateurs
    conn.commit()
    cur.close()
    conn.close()

def test_register_new_user():
    """
    Test : Inscription d'un nouvel utilisateur
    """
    response = client.post(
        "/register/register",
        json={
            "username": "test_user",
            "password": "test123"
        }
    )
    
    # Vérifier que ça marche (status 200)
    assert response.status_code == 200
    assert response.json()["message"] == "User created successfully"



def test_login_success():
    """
    Test : Connexion avec des credentials valides
    """
    # D'abord créer un utilisateur
    client.post(
        "/register/register",
        json={
            "username": "login_user",
            "password": "test123"
        }
    )
    
    # Essayer de se connecter
    response = client.post(
        "/auth/login",
        json={
            "username": "login_user",
            "password": "test123"
        }
    )
    
    # Vérifier que ça marche
    assert response.status_code == 200
    assert "token" in response.json()
    # Bonus : vérifier que le token n'est pas vide
    assert len(response.json()["token"]) > 0


