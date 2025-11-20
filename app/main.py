from fastapi import FastAPI
from app.routes.sentiment_router import router as sentiment_router
from app.routes.login_router import router as login_router

app = FastAPI(title="Sentiment Analysis API")


# Inclure les routers
app.include_router(sentiment_router)
app.include_router(login_router)

@app.get("/")
async def root():
    return {"message": "Bienvenue dans Sentiment Analysis API!"}