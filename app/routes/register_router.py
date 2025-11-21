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

router = APIRouter(prefix="/register", tags=["User Registration"])


@router.post("/register")
def register(data: user_schema):
    """
    Inscrit un nouvel utilisateur dans la base de données.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Vérifier si l'utilisateur existe déjà
        cursor.execute("SELECT username FROM users WHERE username = %s", (data.username,))
        
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Username already exists")
        
        # Hasher le mot de passe
        hashed_password = bcrypt.hashpw(data.password.encode('utf-8'), bcrypt.gensalt())
        
        # Insérer le nouvel utilisateur
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (data.username, hashed_password.decode('utf-8'))
        )
        conn.commit()
        
        return {"message": "User created successfully"}
    
    except HTTPException:  # ← IMPORTANT : relancer les HTTPException(pour test_unitaires)
        raise
    
    except Exception as e: # Capturer les autres erreurs (500)
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        cursor.close()
        conn.close()
