import requests
from bs4 import BeautifulSoup

class persoons:
    @staticmethod
    def persoons_gegevens(site):
        try:
            response = requests.get(site)
            soup = BeautifulSoup(response.content, "html.parser")

            naam_tag = soup.find('a', href=f'#verkoper')
            naam = naam_tag.get_text(strip=True) if naam_tag else None

            jaar_tag = soup.find('div', class_='TextEllipsis')
            jaar = jaar_tag.get_text(strip=True) if jaar_tag else None
            jaar = jaar.replace(' op Marktplaats', '')

            review_raw_tag = soup.find('span', class_='hz-Text--bodyLargeStrong')
            review_raw = review_raw_tag.get_text(strip=True) if review_raw_tag else None
            if review_raw is not None:
                review_raw = review_raw.replace(' · ', '')

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
