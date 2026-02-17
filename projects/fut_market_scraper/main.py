print("--- DEBUG: init_db wurde aufgerufen ---")

from database import get_db_session, init_db
from projects.fut_market_scraper.ingestor import FifaPriceIngestor
from loguru import logger

def main():
    init_db()

    logger.info("Starte FIFA Scraper...")

    with get_db_session() as session:
        ingestor = FifaPriceIngestor(session)

        # TODO Diese Liste über eine CSV-Datei einlesen
        watchlist = [
            {
                "f_name": "lionel",
                "l_name": "messi",
                "f_id": "21442"
            },
            {
                "f_name": "cristiano",
                "l_name": "ronaldo",
                "f_id": "22012"
            }
        ]
        for player in watchlist:
            ingestor.fetch_by_player(f_name=player["f_name"], l_name=player["l_name"], f_id=player["f_id"])

        # TODO Diese Liste über eine CSV-Datei einlesen
        rating_list = [85, 88, 92]
        for rating in rating_list:
            ingestor.fetch_by_rating(rating)
        
        session.commit()
        
    logger.success("FUT-Preise erfolgreich abgerufen!")

if __name__ == "__main__":
    main()
