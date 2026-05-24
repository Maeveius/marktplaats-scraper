import requests
from bs4 import BeautifulSoup

class persoons:
    @staticmethod
    def persoons_gegevens(site):
        try:
            response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(response.content, "html.parser")

            naam_tag = soup.find('a', href='#verkoper')
            naam = naam_tag.get_text(strip=True) if naam_tag else None

            jaar_tag = soup.find('div', class_='TextEllipsis')
            jaar = jaar_tag.get_text(strip=True).replace(' op Marktplaats', '') if jaar_tag else None  # ← fix

            review_raw_tag = soup.find('p', class_='SellerTrustIndicator-body')
            review_raw = review_raw_tag.get_text(strip=True).replace(' · ', '') if review_raw_tag else None

            if jaar:
                if 'maand' in jaar:
                    betrouwbaarheid = 'niet vertrouwen'
                elif 'jaar' in jaar:
                    aantal = float(jaar.split()[0])
                    betrouwbaarheid = 'Good shit' if aantal > 5 else 'Oke'
                else:
                    betrouwbaarheid = 'idk'
            else:
                betrouwbaarheid = None

            if review_raw:
                try:
                    r = float(review_raw)
                    if r > 4: review = 'good shit'
                    elif r < 2.5: review = 'wtf'
                    else: review = 'meh'
                except:
                    review = None
            else:
                review = None

            return naam, betrouwbaarheid, review

        except:
            return None, None, None