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
        # Crée la table users si elle n'existe pas
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        
        # Vide la table
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
    
    assert response.status_code == 200
    assert "token" in response.json()
    assert len(response.json()["token"]) > 0