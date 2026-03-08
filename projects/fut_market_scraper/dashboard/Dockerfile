FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Hier liegt der Fehler: Der Pfad muss vom Root aus gesehen werden
COPY projects/fut_market_scraper/dashboard/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Wir kopieren alles (das gesamte Projekt) nach /app
COPY . .

# Wir springen in den Ordner, wo die Hauptdatei liegt
WORKDIR /app/projects/fut_market_scraper/dashboard

EXPOSE 8501

CMD ["streamlit", "run", "fut_dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]