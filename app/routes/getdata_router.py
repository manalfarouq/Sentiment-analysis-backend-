from fastapi import APIRouter, HTTPException, Header
from jose import jwt, JWTError

from app.core.config import settings

router = APIRouter(prefix="/data", tags=["Test du token JWT"])


@router.get("/test")
def get_data(token: str = Header(...)):
    """
    Vérifie le token JWT passé directement dans le header.
    Format attendu : "<token>"
    """
    try:
        payload = jwt.decode(token, settings.SK, algorithms=[settings.ALG])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return {
        "message": "Token valid!",
        "user": payload.get("sub"),
    }