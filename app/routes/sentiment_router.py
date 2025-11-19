from fastapi import APIRouter
from app.services.huggingface_service import process_text
from app.schemas.SentimentRequest import SentimentRequest



router = APIRouter(prefix="/sentiment", tags=["Sentiment Analysis"])


@router.post("/predict")
async def predict_sentiment(data: SentimentRequest):
    result = process_text(data.text)
    return {"result": result}