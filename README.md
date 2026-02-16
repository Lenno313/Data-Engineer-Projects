# Data-Engineer-Projects

Herzlich willkommen in meinem Data Engineering Repository! Hier dokumentiere ich den Aufbau und die Automatisierung verschiedener Daten-Pipelines, die auf einem **Raspberry Pi Home-Server** in einer **Docker-Umgebung** laufen.

## Vision
Ziel dieses Repositories ist es, bisherige Projekte von mir einmal zu Modularisieren und in strukturierte Daten-Pipelines zu verpacken.

---

## Die Projekte

### Projekt 1: F1 Telemetry & Race Analytics

#### Zusammenfassung
Automatisierte Erfassung von Runden- und Sektorenzeiten der Formel 1. Dieses Projekt simuliert den Umgang mit hochpräzisen Transaktionsdaten.

<details>
<summary>▶ Details anzeigen</summary>

#### Tech-Stack
- **Quelle:** FastF1 Library / Ergast API
- **Processing:** Python (Pandas zur Bereinigung von Zeitstempeln)
- **Persistence:** SQLAlchemy Models (Hierarchische Struktur: Race -> Driver -> Lap)

#### Beschreibung

</details>

---

### Projekt 2: FIFA Ultimate Team Market Tracker (FUTWIZ)

#### Zusammenfassung
Überwachung von Spielerpreisen auf dem Transfermarkt. Fokus liegt auf der Extraktion von Daten aus HTML-Strukturen, wo keine offizielle API existiert.

<details>
<summary>▶ Details anzeigen</summary>

#### Tech-Stack
- **Quelle:** Web-Scraping (BeautifulSoup / Requests)
- **Transform:** Cleaning-Logik (z.B. Umwandlung von "1.2K" Strings in Integer `1200`)
- **Storage:** PostgreSQL

#### Beschreibung

</details>

---

### Projekt 3: Garmin Health & Activity Ingestor 

#### Zusammenfassung
Abruf von persönlichen Aktivitätsdaten (Leistung, Herzfrequenz, GPS). Vorbereitung der Daten für ein späteres BI-Dashboard.

<details>
<summary>▶ Details anzeigen</summary>

#### Tech-Stack
- **Quelle:** Garmin Connect API
- **Format:** JSON-Parsing komplexer Nested Objects
- **DB:** SQL-Datenbank (Normalisierte Tabellen für Aktivitäten und Splits)

#### Beschreibung

</details>

---

## Infrastruktur (Raspberry Pi Setup)

Das gesamte Lab wird über eine zentrale `docker-compose.yml` auf einem Raspberry Pi gesteuert.

<details>
<summary>▶ Infrastruktur-Details & Docker-Setup</summary>

- **Datenbank:** PostgreSQL Container mit persistenten Volumes auf einer externen SSD.
- **Automatisierung:** - Die Skripte werden über Cronjobs auf dem Host-System oder innerhalb eines speziellen Cron-Containers getriggert.
  - Secrets (Passwörter/Keys) werden sicher über `.env`-Dateien verwaltet.
- **Monitoring:** (Geplant) Dashboard zur Überwachung der Pipeline-Status.

</details>

---

## Roadmap
#### Phase 1 - Code-Modularisierung & Aufsetzen der Infrastruktur
- [ ] Überführung der bestehenden Scraping-, FastF1- und Garmin-Skripte in eine geordnete Klassenstruktur (Ingestor-Pattern).
- [ ] Initialer Aufbau der Datenbank-Schemata (SQLAlchemy).
- [ ] Neuaufsetzen des Raspberry Pi OS (Lite) und Konfiguration der Docker-Engine sowie Docker Compose.

#### Phase 2 
- [ ] Database Layer: Deployment des PostgreSQL-Containers
- [ ] Containerisierung: Erstellung von Docker-Images für jeden Ingestor.
- [ ] Automation: Implementierung der Cron-Logik zur regelmäßigen Datenabfrage (FIFA z.B. täglich, F1 rennwochenendspezifisch).
- [ ] Secret Management: Umstellung aller Hardcoded-Credentials auf Umgebungsvariablen (.env).

#### Phase 3: Weitere Feature-Ideen wie Analytics & Monitoring einbauen
- [ ] Data Quality Checks: Implementierung von Logging und einfachen Validierungsskripten, um Ingestions-Fehler frühzeitig zu erkennen.
- [ ] Visualisierung: Aufbau eines Streamlit-Dashboards, das direkt auf die PostgreSQL-DB zugreift, um Preisverläufe (FIFA) und Sektorenvergleiche (F1) darzustellen.
- [ ] Health Check: Einbindung eines einfachen Monitoring-Tools (z.B. Portainer oder sogar kurze Status-Mail), um den Zustand des Raspberry Pi zu überwachen.
