import psycopg2
from app.core.config import settings

"""
    Qu'est-ce que ça fait ?

=> Cette fonction crée une connexion entre Python et PostgreSQL
=> C'est comme ouvrir une porte entre le code et la base de données
=> Chaque fois que je veux lire/écrire dans la base,  j'appelle cette fonction

"""

def get_db_connection():
    conn = psycopg2.connect(
        host=settings.DB_HOST,        # Adresse du serveur (localhost)
        port=settings.DB_PORT,        # Port PostgreSQL (5432)
        database=settings.DB_NAME,    # Nom de la base (sentiment_db)
        user=settings.DB_USER,        # Utilisateur (sentiment_user)
        password=settings.DB_PASSWORD # Mot de passe
    )
    return conn