from fastapi import APIRouter, Header
from app.services.huggingface_service import process_text
from app.schemas.SentimentRequest import SentimentRequest
from app.auth.token_auth import verify_token 


router = APIRouter(prefix="/sentiment", tags=["Sentiment Analysis"])


@router.post("/predict")
async def predict_sentiment(data: SentimentRequest, token: str = Header(...)):
    """
    Analyse le sentiment d'un texte.
    Nécessite un token JWT valide dans le header 'token'.
    """
    # Vérification du token avec ta fonction existante
    verify_token(token)
    
    # Traitement du texte
    result = process_text(data.text)
    
    return {"result": result}