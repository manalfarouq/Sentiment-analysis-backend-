import requests
from app.core.config import settings

# Récupérer le token depuis Pydantic Settings
HF_TOKEN = settings.HF_API_TOKEN


if not HF_TOKEN:
    raise ValueError("HF_TOKEN non trouvé dans .env")

# Configuration de l'API Hugging Face
API_URL = "https://router.huggingface.co/hf-inference/models/nlptown/bert-base-multilingual-uncased-sentiment"
HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
}

def process_text(text: str):
    """Analyse le sentiment d'un texte et retourne positif/negatif/neutre"""
    payload = {"inputs": text}
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    result = response.json()

    # Format de result = [[{label: "5 stars", score: ...}, ...]]
    predictions = result[0]

    # Choisir le score le plus élevé
    best = max(predictions, key=lambda x: x["score"])

    # Récupérer le nombre d'étoiles
    stars = int(best["label"].split()[0])

    # Convertir les étoiles → sentiment
    if stars <= 2:
        return "Negative Feedback (1 or 2 stars)"
    elif stars == 3:
        return "Neutral Feedback (3 stars)"
    else:
        return "Positive Feedback (4 or 5 stars)"
