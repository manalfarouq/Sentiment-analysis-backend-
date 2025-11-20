from fastapi import APIRouter, HTTPException
from jose import jwt
from datetime import datetime, timedelta
from app.schemas.LoginRequest import LoginRequest
from app.core.config import settings
from app.database.db_connection import get_db_connection
import bcrypt


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login")
def login(data: LoginRequest):
    """
    Authentifie un utilisateur avec username et password.
    Retourne un token JWT si les credentials sont valides.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Chercher l'utilisateur dans la base
        cursor.execute(
            "SELECT username, password FROM users WHERE username = %s",
            (data.username,)
        )
        user = cursor.fetchone()
        
        # Vérifier si l'utilisateur existe
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        db_username, db_password = user
        
        # Vérifier le mot de passe
        if not bcrypt.checkpw(data.password.encode('utf-8'), db_password.encode('utf-8')):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Créer le token JWT
        payload = {
            "sub": db_username,
            "exp": datetime.utcnow() + timedelta(hours=1)
        }
        token = jwt.encode(payload, settings.SK, algorithm=settings.ALG)
        
        return {"token": token, "token_type": "bearer"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        cursor.close()
        conn.close()