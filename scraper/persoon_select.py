import requests
from bs4 import BeautifulSoup

class persoons:
    @staticmethod
    def persoons_gegevens(site):
        try:
            response = requests.get(site)
            soup = BeautifulSoup(response.content, "html.parser")

            naam = soup.find('a', href=f'#verkoper')
            naam = naam.get_text(strip=True) if naam else None

            jaar = soup.find('div', class_='SellerInfoSmall-row')
            jaar = jaar.get_text(strip=True) if jaar else None

            review_raw = soup.find('span', class_='hz-StarRating-number')
            review_raw = review_raw.get_text(strip=True) if review_raw else None

            # betrouwbaarheid
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

            # review classificatie
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
