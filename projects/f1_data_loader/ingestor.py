import fastf1
import os
from database import get_db_session
from .models import F1Race, F1Result
from loguru import logger

class F1Ingestor:
    def __init__(self, db_session=None, cache_dir: str ='projects/f1_data_loader/f1_cache'):
        # Hier lag der Fehler: cache_dir muss ein String sein!
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        fastf1.Cache.enable_cache(cache_dir) 
        self.db = db_session

    def ingest_2025_results(self):
        """Lädt alle bisherigen Rennergebnisse der Saison 2025."""
        schedule = fastf1.get_event_schedule(2025) # saison 2025 laden
        
        for index, event in schedule.iterrows():
            if index == 0: logger.info(event)
            if event['EventFormat'] == 'testing':
                continue # Tests ignorieren wir
                
            try:
                session = fastf1.get_session(2025, event['EventName'], 'R')
                session.load(telemetry=False) # Nur Ergebnisse laden
                
                with get_db_session() as db:
                    # Rennen speichern
                    race = F1Race(
                        season=2025,
                        round=event['RoundNumber'],
                        circuit_name=event['Location'],
                        date=str(event['EventDate'])
                    )
                    db.add(race)
                    db.flush() # damit das Rennen existiert & man es als key verwenden kann

                    # Ergebnisse speichern
                    for _, driver_res in session.results.iterrows():
                        res = F1Result(
                            race_id=race.id,
                            driver_name=driver_res['FullName'],
                            constructor=driver_res['TeamName'],
                            position=int(driver_res['Position']),
                            points=float(driver_res['Points'])
                        )
                        db.add(res)
                logger.success(f"Ergebnisse für {event['EventName']} eingelesen.")
            except Exception as e:
                logger.warning(f"Keine Daten für {event['EventName']} verfügbar (Rennen evtl. in der Zukunft).")
