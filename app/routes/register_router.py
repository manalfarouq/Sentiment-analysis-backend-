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
    # 1. Se connecter à la base de données
    conn = get_db_connection()
    cursor = conn.cursor()  # Un cursor = comme un pointeur pour exécuter des commandes SQL
    
    try:
        # 2. Vérifier si l'utilisateur existe déjà
        cursor.execute("SELECT username FROM users WHERE username = %s", (data.username,))
        
        if cursor.fetchone():  # Si on trouve quelque chose, l'utilisateur existe déjà
            raise HTTPException(status_code=400, detail="Username already exists")
        
        # 3. Hasher (crypter) le mot de passe avant de le stocker
        hashed_password = bcrypt.hashpw(data.password.encode('utf-8'), bcrypt.gensalt())
        
        # 4. Insérer le nouvel utilisateur dans la base
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (data.username, hashed_password.decode('utf-8'))
        )
        conn.commit()  # IMPORTANT : sauvegarder les changements dans la base
        
        return {"message": "User created successfully"}
    
    except Exception as e:
        conn.rollback()  # En cas d'erreur, annuler les changements
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        cursor.close()  # Fermer le cursor
        conn.close()    # Fermer la connexion