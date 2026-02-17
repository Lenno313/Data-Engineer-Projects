from .models import Player, Price, RatingSnapshot
from datetime import datetime
from playwright.sync_api import sync_playwright
from loguru import logger
from .models import Player, Price, RatingSnapshot
from datetime import datetime

class FifaPriceIngestor:
    def __init__(self, session):
        self.session = session

    # DATENBANK
    def save_player_to_db(self, f_id, f_name, l_name):
        """Prüft, ob der Spieler existiert, und legt ihn ggf. an."""
        player = self.session.query(Player).get(f_id)
        if not player:
            player = Player(
                futwiz_id=f_id,
                first_name=f_name,
                last_name=l_name
            )
            self.session.add(player)
            logger.info(f"Neuer Spieler angelegt: {f_name} {l_name} [{f_id}]")
        return player

    def save_price_to_db(self, f_id, price_val):
        """Speichert einen neuen Preiseintrag für einen Spieler."""
        new_price = Price(player_id=f_id, price_value=price_val)
        self.session.add(new_price)
        self.session.commit() # Session Zwischenspeichern

    # SCRAPING
    def fetch_by_player(self, f_id, f_name, l_name):
        """Sicherer Ingest mit Playwright."""
        self.save_player_to_db(f_id, f_name, l_name)
        
        # URL Formatierung (beachtet die Pfade aus deinen Screenshots)
        player_slug = f"{f_name.lower()}-{l_name.lower()}"
        url = f"https://www.futwiz.com/en/fc26/player/{player_slug}/{f_id}"
        
        # Wir nutzen ein Try-Block um den gesamten Playwright-Prozess
        try:
            price = self._scrape_price_with_playwright(url=url)
        except Exception as e:
            logger.error(f"Fehler bei {f_name}: {e}")

        self.save_price_to_db(f_id, price)
        logger.success(f"Preis für {player_slug} [{price}] wurde gespeichert.")
    
        """
        ALTE VERSION MIT BEATIFUL SOUP
        page = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(page.text, "html.parser")
        price_div = soup.find("div", class_="text-cyan-300")
        """

    def _scrape_price_with_playwright(self, url: str) -> int:
        """Starte einen virtuellen browser auf der Seite und lese den Preis aus."""
        clean_price = None
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True) # starte chrome browser
            
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            )
            page = context.new_page()

            page.goto(url, wait_until="domcontentloaded", timeout=10000) # öffne url
            
            # 1. Cookie-Banner Check
            try:
                consent_selector = "button:has-text('Consent')"
                page.wait_for_selector(consent_selector, timeout=5000)
                page.click(consent_selector)
            except:
                pass 

            # 2. Preis extrahieren
            price_selector = "div.text-cyan-300.text-xl.font-bold" # passenden div-block wählen
            page.wait_for_selector(price_selector, timeout=10000)
            
            raw_price = page.inner_text(price_selector)
            clean_price = raw_price.replace(".", "").replace(",", "").strip()
            
            browser.close()
        return clean_price
    
    def fetch_by_rating(self, rating):
        """Hol die Preise der 10 günstigsten Spieler mit dem rating."""
        url = f"https://www.futwiz.com/lowest-price-ratings"
        
        try:
            extracted_prices = self._scrape_rating_prices_with_playwright(url, rating)
            
            # Die 10 Ergebnisse (z.B. Top 3) als Snapshots speichern
            for index, price in enumerate(extracted_prices):
                snapshot = RatingSnapshot(
                    rating=rating,
                    price_value=price,
                    rank=index + 1,
                    timestamp=datetime.utcnow()
                )
                self.session.add(snapshot)
            
            self.session.commit() # Zwischenspeichern der session
            logger.success(f"Snapshots für Rating {rating} gespeichert.")

        except Exception as e:
            self.session.rollback()
            logger.error(f"Fehler bei Rating {rating}: {e}")

    def _scrape_rating_prices_with_playwright(self, url: str, target_rating: int) -> list:
        """Starte einen virtuellen browser auf der Seite und lies die Preise von dem Rating aus."""
        prices = []
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=10000)
            
            # 1. Cookie-Banner Check
            try:
                consent_selector = "button:has-text('Consent')"
                page.wait_for_selector(consent_selector, timeout=5000)
                page.click(consent_selector)
            except:
                pass 

            # Wir suchen die Preis-Elemente auf der gefilterten Seite
            price_selector = "span.player-value"
            page.wait_for_selector(price_selector, timeout=10000)
            
            price_elements = page.locator(price_selector).all() # Preise auswählen
            base_rating = 82
            index = target_rating - base_rating
            start_idx = 0 + index*10
            end_idx = start_idx + 10
            
            for el in price_elements[start_idx:end_idx]:
                text = el.inner_text() # Preise auslesen & bereinigen
                if 'K' in text:
                    num_part = text.replace("K", "")
                    price = int(float(num_part) * 1000)
                elif 'M' in text:
                    num_part = text.replace("M", "")
                    price = int(float(num_part) * 1000000)
                else:
                    price = int(text) # bei normaler Zahl nur zu int casten
                prices.append(price)

            browser.close()
                
        return prices
