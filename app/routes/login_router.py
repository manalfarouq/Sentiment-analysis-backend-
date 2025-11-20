from fastapi import APIRouter, HTTPException
from jose import jwt
from app.database.database import data_db
from app.schemas.user_schema import user_schema
from app.core.config import settings

router = APIRouter(prefix="/login", tags=["User Authentication"])

@router.post("/login")
def login(data: user_schema):
    if data.username == data_db["username"] and data.password == data_db["password"]:
        # Utiliser settings.SK et settings.ALG
        token = jwt.encode({}, key=settings.SK, algorithm=settings.ALG)
        return {"access_token": token}  
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")
