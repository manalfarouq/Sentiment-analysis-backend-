from fastapi import FastAPI
from app.routes.sentiment_router import router as sentiment_router

app = FastAPI(title="Sentiment Analysis API")


# Inclure les routers
app.include_router(sentiment_router)

@app.get("/")
async def root():
    return {"message": "Bienvenue dans Sentiment Analysis API!"}