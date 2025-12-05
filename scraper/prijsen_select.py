import requests
from bs4 import BeautifulSoup

class prijzen_check:
    @staticmethod
    def marktplaats_prijs(prijs, item):

        prijs_raw = prijs.get_text(strip=True)
        prijs_value = None
        top_prijs = None

        if prijs_raw in ['Zie omschrijving', 'Gereserveerd']:
            return None, None

        if prijs_raw == "Bieden":
            mini_url_tag = item.find('a', class_='hz-Link')
            if mini_url_tag and mini_url_tag.has_attr("href"):
                listing_url = "https://www.marktplaats.nl" + mini_url_tag["href"]
                top_prijs = prijzen_check.deepsearch(listing_url)
            return None, top_prijs

        # normale prijs
        clean = (
            prijs_raw.replace('\xa0', ' ')
            .replace('€ ', '')
            .replace(',', '.')
            .replace('-', '00')
        )

        try:
            prijs_value = float(clean)
            top_prijs = prijs_value
        except:
            prijs_value, top_prijs = None, None

        return prijs_value, top_prijs

    @staticmethod
    def deepsearch(url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            biedingen = soup.find_all("span", class_="hz-Offer-bidPrice")

            prijzen = []
            for bid in biedingen:
                try:
                    raw = bid.get_text(strip=True).replace('€ ', '').replace(',', '.')
                    prijzen.append(float(raw))
                except:
                    pass

            return max(prijzen) if prijzen else None
        except:
            return None
