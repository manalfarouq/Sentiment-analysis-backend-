-- Ce script est exécuté automatiquement au premier démarrage de PostgreSQL

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Donner les droits à l'utilisateur
GRANT ALL PRIVILEGES ON TABLE users TO sentiment_user;
GRANT USAGE, SELECT ON SEQUENCE users_id_seq TO sentiment_user;
