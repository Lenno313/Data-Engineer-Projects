# microsoft image laden
FROM mcr.microsoft.com/playwright/python:v1.50.0-noble

# Arbeitsverzeichnis im Container festlegen
WORKDIR /app

# Wir kopieren die requirements relativ zum Hauptordner
COPY projects/fut_market_scraper/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install chromium

# Den restlichen Code kopieren
COPY . .

# Befehl zum Starten
CMD ["python", "projects/fut_market_scraper/main.py"]