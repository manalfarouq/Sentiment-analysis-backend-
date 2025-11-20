from fastapi import APIRouter, HTTPException
from jose import jwt
from app.schemas.user_schema import user_schema
from app.core.config import settings
from app.database.db_connection import get_db_connection  
import bcrypt   


"""
Qu'est-ce qui se passe ?

1. Connexion : On ouvre la porte vers PostgreSQL
2. Vérification : On regarde si le username existe déjà
   SQL : SELECT username FROM users WHERE username = 'manal'
3. Hashing : On crypte le mot de passe avec bcrypt
   123456 → $2b$12$xyz...
4. Insertion : On ajoute le nouvel utilisateur dans la table users
   SQL : INSERT INTO users (username, password) VALUES ('manal', '$2b$12$xyz...')
5. Commit : On sauvegarde les changements (sans ça, rien n'est enregistré !)
6. Fermeture : On ferme la connexion (pour ne pas laisser de portes ouvertes)
"""

router = APIRouter(prefix="/register", tags=["Inscription Utilisateur"])


@router.post("/register")
def register(data: user_schema):
    """
    Inscrit un nouvel utilisateur
    """

    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Vérifier si le username existe
        cursor.execute("SELECT username FROM users WHERE username = %s", (data.username,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Username already exists")
        
        # Hasher le mot de passe
        hashed_password = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt())

        # Insérer dans la base
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (data.username, hashed_password.decode())
        )
        conn.commit()

        return {"message": "User created successfully"}
    
    except:
        raise HTTPException(status_code=500, detail="Server error")
    
    finally:
        cursor.close()
        conn.close()
