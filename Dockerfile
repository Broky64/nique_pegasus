# === Stage 1 : Builder (Installation des dépendances Python) ===
FROM --platform=linux/amd64 python:3.9-slim AS builder

WORKDIR /install

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc build-essential \
 && rm -rf /var/lib/apt/lists/*

# Créer un environnement virtuel
RUN python -m venv /opt/venv

# Copier et installer les dépendances Python
COPY requirements.txt .
RUN /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# === Stage 2 : Image finale (Runtime minimal avec Chrome et Cron) ===
FROM --platform=linux/amd64 python:3.9-slim

# Installer les paquets système nécessaires pour Google Chrome et Cron
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    gnupg2 \
    ca-certificates \
    cron \
 && rm -rf /var/lib/apt/lists/*

# Installer Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y --no-install-recommends google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail de l'application
WORKDIR /app

# Copier le code source
COPY . .

# Copier l'environnement virtuel depuis l'étape builder
COPY --from=builder /opt/venv /opt/venv

# Mettre à jour le PATH pour utiliser l'environnement virtuel
ENV PATH="/opt/venv/bin:$PATH"
ENV CHROME_BINARY=/usr/bin/google-chrome

# Ajouter la configuration du job cron : exécuter app.py toutes les 15 minutes (00:00, 00:15, etc.)
RUN echo "*/15 * * * * root /opt/venv/bin/python /app/app.py >> /var/log/cron.log 2>&1" > /etc/cron.d/app-cron && \
    chmod 0644 /etc/cron.d/app-cron && \
    crontab /etc/cron.d/app-cron

# Déclarer un volume pour consulter les logs si besoin
VOLUME /var/log

# Copier le script d'entrypoint qui exécute app.py dès le démarrage puis lance cron
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Définir l'entrypoint
ENTRYPOINT ["/entrypoint.sh"]