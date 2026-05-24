import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import json

from .Title_garantee import title_garantes
from .prijsen_select import prijzen_check
from .Datum_select import datum_check
from .locatie_afstand import locatie
from .persoon_select import persoons

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

class Scrap:
    def __init__(self):
        self.data = {}

    def martktplaats_scrape(self, search):
        search_url = f'https://www.marktplaats.nl/q/{search}'
        response = requests.get(search_url, headers=HEADERS)
        soup = BeautifulSoup(response.content, "html.parser")

        # paginering uit JSON halen
        script = soup.find('script', id='__NEXT_DATA__')
        json_data = json.loads(script.string)
        hoeveel_int = json_data['props']['pageProps']['searchRequestAndResponse']['maxAllowedPageNumber']

        counter = 0
        index = 0

        while counter < hoeveel_int:
            page_url = search_url + f'/p/{counter+1}/'
            response = requests.get(page_url, headers=HEADERS)
            soup = BeautifulSoup(response.content, "html.parser")

            # listings uit JSON halen in plaats van HTML
            script = soup.find('script', id='__NEXT_DATA__')
            json_data = json.loads(script.string)
            listings = json_data['props']['pageProps']['searchRequestAndResponse']['listings']
            print(f"Gevonden listings op pagina {counter+1}: {len(listings)}")

            for item in listings:
                title_text = item.get('title', '')
                title_value, title_text = title_garantes().marktplaats_title_text(title_text, search)

                if title_value:
                    price_info = item.get('priceInfo', {})
                    price_type = price_info.get('priceType', '')
                    price_cents = price_info.get('priceCents', 0)

                    if price_type == 'FIXED':
                        prijs_value = price_cents / 100
                        top_prijs = prijs_value
                    elif price_type == 'MIN_BID':
                        prijs_value = None
                        top_prijs = price_cents / 100
                    else:
                        prijs_value, top_prijs = None, None

                    try:
                        datums = datum_check().marktplaats_datum_text(item.get('date'))
                    except:
                        datums = None

                    vip_url = item.get('vipUrl', None)
                    listing_url = f"https://www.marktplaats.nl{vip_url}" if vip_url else None
                    website_raw = item.get('sellerInformation', {}).get('showWebsiteUrl', False)

                    if listing_url:
                        locaties = locatie().area(listing_url)
                        persoon, aantal_jaar, reviews = persoons().persoons_gegevens(listing_url)
                    else:
                        locaties, persoon, aantal_jaar, reviews = None, None, None, None

                    self.data[index] = {
                        'Naam': title_text,
                        'Prijs': prijs_value,
                        'Bieden': top_prijs,
                        'Datum': datums,
                        'Locatie': locaties,
                        'Verkoper': persoon,
                        'Vertrouwbaarheid': aantal_jaar,
                        'reviews': reviews,
                        'Website': website_raw,
                        'url': listing_url
                    }
                    index += 1

            counter += 1

        return self.data