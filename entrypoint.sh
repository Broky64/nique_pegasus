#!/bin/sh
echo "Exécution initiale de app.py..."
/opt/venv/bin/python /app/app.py
echo "Lancement de cron..."
exec cron -f
