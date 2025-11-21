from fastapi import APIRouter, HTTPException
from jose import jwt
from datetime import datetime, timedelta
from app.schemas.LoginRequest import LoginRequest
from app.core.config import settings
from app.database.db_connection import get_db_connection
import bcrypt


router = APIRouter(prefix="/auth", tags=["Login"])


@router.post("/login")
def login(data: LoginRequest):
    """
    Route simple de login :
    - Cherche l'utilisateur dans la base
    - Vérifie le mot de passe avec bcrypt
    - Retourne un token JWT valable 1 heure
    """

    # Connexion à la base de données
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        #! 1. Vérifier si l'utilisateur existe grâce à son username
        cursor.execute(
            "SELECT username, password FROM users WHERE username = %s",
            (data.username,)
        )
        user = cursor.fetchone()

        # Si aucun utilisateur trouvé → mauvais username
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # user = (username, mot_de_passe_hashé)
        db_username, db_password = user

        #! 2. Vérifier si le mot de passe entré correspond au hash stocké
        # bcrypt.checkpw() compare :
        # - data.password (le mot de passe tapé)
        # - db_password (le hash dans la base)
        if not bcrypt.checkpw(data.password.encode(), db_password.encode()):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        #! 3. Si tout est correct : créer un token JWT
        # "sub" = username (subject)
        # "exp" = date d'expiration du token (dans 1 heure)
        payload = {
            "sub": db_username,
            "exp": datetime.utcnow() + timedelta(hours=1) 
        }


        # Encodage du token avec ta clé secrète et ton algorithme JWT
        token = jwt.encode(payload, settings.SK, algorithm=settings.ALG)

        #! 4. Retourner le token au frontend
        return {"token": token}

    #? Si un problème inattendu arrive → erreur serveur (sans montrer le détail)
    except HTTPException:  # ← IMPORTANT : relancer les HTTPException
        raise
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Toujours fermer la connexion à la base
        cursor.close()
        conn.close()
