# Utiliser une image Python officielle
FROM python:3.10-alpine

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code
COPY . .

# Créer un utilisateur non-root pour exécuter l'application
RUN useradd -m appuser
USER appuser

# Exposer le port du serveur Django
EXPOSE 8000

# Commande pour lancer Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
