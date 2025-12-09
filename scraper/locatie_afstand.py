import requests
from bs4 import BeautifulSoup

class locatie:
    @staticmethod
    def area(site):
        try:
            response = requests.get(site)
            soup = BeautifulSoup(response.content, "html.parser")

            stad = soup.find('div', class_='SellerLocationSection-locationName')

            stad_text = stad.get_text(strip=True) if stad else None
            


            return stad_text
        except:
            return None
