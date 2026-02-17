import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager
from loguru import logger

# Base-Klasse für die Models
Base = declarative_base() # Zur Einfachheit nur eine Basis-DB für alle Projekte

# Prüfen, ob der Ordner existiert, wenn nicht: erstellen
db_folder = "local_db"
db_name = "database.db"
if not os.path.exists(db_folder):
    os.makedirs(db_folder)

# Den Pfad für SQLAlchemy zusammenbauen
db_local_path = f"sqlite:///{db_folder}/{db_name}"

# Datenbank-URL konfigurieren
DATABASE_URL = os.getenv("DATABASE_URL", db_local_path) # Lokal falls keine andere DB da

# Engine & Session-Fabrik
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db_session():
    """
    Öffnet die Session, committet automatisch oder macht Rollback bei Fehlern.
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Datenbank-Transaktion fehlgeschlagen: {e}")
        raise
    finally:
        session.close()

def init_db():
    """Erstellt alle Tabellen (wird einmalig aufgerufen)"""
    try:
        from projects.fut_market_scraper import models as fut_models

        Base.metadata.create_all(bind=engine)
        logger.success("Datenbank initialisiert: Tabellen erstellt.")
    except ImportError as e:
        logger.error(f"Fehler beim Importieren der Models: {e}")
    except Exception as e:
        logger.error(f"Fehler bei create_all: {e}")
