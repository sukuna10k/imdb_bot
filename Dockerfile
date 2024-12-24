# Utilisez une image Python officielle
FROM python:3.10-slim

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers du projet dans le conteneur
COPY . /app

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Lancer le bot
CMD ["python", "bot.py"]
