# Utiliser Python 3.11 comme base
FROM python:3.11-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Installer les dépendances système pour PostgreSQL
RUN apt-get update && apt-get install -y \
    postgresql-client \
    cmake \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*


# Copier les fichiers de dépendances
COPY pyproject.toml poetry.lock ./

# Installer Poetry
RUN pip install poetry

# Installer les dépendances Python (sans virtualenv)
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Copier tout le code de l'application
COPY . .

# Exposer le port 8000
EXPOSE 8000

# Commande pour lancer l'application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]