import requests
from bs4 import BeautifulSoup
from datetime import date
from datetime import timedelta

month_map = {
    'jan': '01', 'feb': '02', 'mrt': '03', 'apr': '04',
    'mei': '05', 'jun': '06', 'jul': '07', 'aug': '08',
    'sep': '09', 'okt': '10', 'nov': '11', 'dec': '12'
}

class datum_check:
    def marktplaats_datum(self, datum):
        datum_text = datum.get_text(strip=True)
        if datum_text == 'Vandaag':
            datums = date.today()
        elif datum_text == 'Gisteren':
            datums = date.today() - timedelta(days=1)
        elif datum_text == 'Eergisteren':
            datums = date.today() - timedelta(days=2)
        else:
            datum_text = datum_text.replace(' ', '-')

            for short, num in month_map.items():
                datum_text = datum_text.replace(short, num)
            
            parts = datum_text.split('-')
            
            if len(parts) == 3:
                dag, maand, jaar = parts
                if len(jaar) == 2:
                    jaar = 2000 + int(jaar)
                datums = date(int(jaar), int(maand), int(dag))
            else:

                datums = datum_text

        return datums