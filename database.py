import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager
from loguru import logger
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
central_env = os.path.join(basedir, "..", "..", ".env")
load_dotenv(central_env)

Base = declarative_base() # für SQLAlchemy

def get_engine():
    # --- VERBINDUNGSAUFBAU ---
    host = os.getenv("DB_HOST", "localhost") 
    user = os.getenv("DB_USER")
    pw = os.getenv("DB_PASSWORD")
    port = os.getenv("DB_PORT", "5432")
    
    db_name = os.getenv("DB_NAME") # Docker-Weg
    
    if not db_name: # Falls wir lokal sind (kein Docker), greift dein Auto-Detect
        if "f1" in basedir.lower():
            db_name = os.getenv("DB_NAME_F1")
        elif "fut" in basedir.lower():
            db_name = os.getenv("DB_NAME_FUT")
        elif "garmin" in basedir.lower():
            db_name = os.getenv("DB_NAME_GARMIN")
        else:
            db_name = os.getenv("DB_NAME_DEFAULT")

    url = f"postgresql://{user}:{pw}@{host}:{port}/{db_name}"
    
    logger.info(f"Verbindung zu Host: {host} | Datenbank: {db_name}")
    return create_engine(url)

# Engine nach der Funktionsdefinition initialisieren
engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Datenbank-Fehler: {e}")
        raise
    finally:
        session.close()

def init_db(target_base):
    """Erstellt die Tabellen auf dem Pi oder lokal."""
    try:
        target_base.metadata.create_all(bind=engine)
        logger.success(f"Datenbank '{os.getenv('DB_NAME')}' erfolgreich initialisiert.")
    except Exception as e:
        logger.error(f"Fehler bei init_db: {e}")
