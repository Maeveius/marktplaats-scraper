import requests
from bs4 import BeautifulSoup

class locatie:
    @staticmethod
    def area(site):
        try:
            response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})  # ← fix
            soup = BeautifulSoup(response.content, "html.parser")
            stad = soup.find('div', class_='SellerLocationSection-locationName')
            return stad.get_text(strip=True) if stad else None
        except:
            return None