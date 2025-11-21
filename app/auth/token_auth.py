from fastapi import Header, HTTPException, Depends
from jose import jwt, JWTError
from app.core.config import settings


def verify_token(token: str = Header(...)):
    """
    Vérifie le token JWT passé dans le header.
    Retourne le payload si valide, sinon lève une exception 401.
    """
    try:
        payload = jwt.decode(token, settings.SK, algorithms=[settings.ALG])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")