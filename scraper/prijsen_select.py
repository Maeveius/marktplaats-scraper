import requests
from bs4 import BeautifulSoup

class prijzen_check:
    @staticmethod
    def marktplaats_prijs(prijs, item):
        
        prijs_raw = prijs.get_text(strip=True)

        prijs_value = None
        top_prijs = None

        #zodra het 1 van de 2 is word de dataframe met none ingevult
        if prijs_raw in ['Zie omschrijving','Gereserveerd']:
            prijs_value = None

        elif prijs_raw == "Bieden":
            mini_url_tag = item.find('a', class_='hz-Link')
                        
            if mini_url_tag and mini_url_tag.has_attr("href"):
                listing_url = "https://www.marktplaats.nl" + mini_url_tag["href"]
                top_prijs = prijzen_check.deepsearch(listing_url)
            else:
                top_prijs = 0

        else:
            prijs_clean = prijs_raw.replace('\xa0', ' ')
            prijs_clean = prijs_clean.replace('€ ', '')
            prijs_clean = prijs_clean.replace(',', '.')
            prijs_clean = prijs_clean.replace('-', '00')
            prijs_value = float(prijs_clean)
            top_prijs = float(prijs_clean)

        return prijs_value , top_prijs



    @staticmethod
    def deepsearch(url):
        try:
            response = requests.get(url)
        except Exception as e:
            print("Deepsearch fout:", e)
            return None

        soup = BeautifulSoup(response.content, "html.parser")

        biedingen = soup.find_all("span", class_="hz-Offer-bidPrice")

        prijzen = []

        for bid in biedingen:
            raw = bid.get_text(strip=True)
            raw = raw.replace("€ ", "").replace(",", ".")
            try:
                prijzen.append(float(raw))
            except:
                continue

        if prijzen:
            return max(prijzen)
        return None