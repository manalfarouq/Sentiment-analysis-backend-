from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.sentiment_router import router as sentiment_router
from app.routes.login_router import router as login_router
from app.routes.getdata_router import router as get_data_router
from app.routes.register_router import router as register_router

app = FastAPI(title="Sentiment Analysis API")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # URL du frontend
    allow_credentials=True,
    allow_methods=["*"],  # Autorise toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],  # Autorise tous les headers
)

@app.get("/")
async def root():
    return {"message": "Bienvenue dans Sentiment Analysis API!"}

# Inclure les routers
app.include_router(login_router)
app.include_router(register_router)
app.include_router(sentiment_router)
app.include_router(get_data_router)

