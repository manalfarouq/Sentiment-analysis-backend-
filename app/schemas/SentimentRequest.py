from pydantic import BaseModel

# Créer un modèle Pydantic pour valider les données
class SentimentRequest(BaseModel):
    text: str 