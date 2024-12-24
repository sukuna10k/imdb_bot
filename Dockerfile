# Utilisez une image Python officielle comme base
FROM python:3.10-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers locaux dans le conteneur
COPY . /app

# Installer les dépendances du projet
RUN pip install --no-cache-dir -r requirements.txt

# Spécifier la commande pour démarrer l'application
CMD ["python", "bot.py"]