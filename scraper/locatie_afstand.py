import requests
from bs4 import BeautifulSoup

class locatie:
    @staticmethod
    def area(site):
        try:
            response = requests.get(site)
            soup = BeautifulSoup(response.content, "html.parser")

            stad = soup.find('div', class_='locationText')
            afstand = soup.find('div', class_='locationDistance')

            stad_text = stad.get_text(strip=True) if stad else None
            afstand_text = afstand.get_text(strip=True) if afstand else None

            return stad_text, afstand_text
        except:
            return None, None
