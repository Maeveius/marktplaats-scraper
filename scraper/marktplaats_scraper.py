import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

from .Title_garantee import title_garantes
from .prijsen_select import prijzen_check
from .Datum_select import datum_check
from .locatie_afstand import locatie
from .persoon_select import persoons

class Scrap:
    def __init__(self):
        self.data = {}

    data = {}
    def martktplaats_scrape(self, search):

        
        search_url = f'https://www.marktplaats.nl/q/{search}'
        response = requests.get(search_url)
        soup = BeautifulSoup(response.content, "html.parser")

        #dit is voor het instellen van de pagina's of er 1 of meerderen zijn
        hoeveel = soup.find('span', attrs={'class': 'hz-PaginationControls-pagination-amountOfPages'})
        if hoeveel:
            hoeveel_tekst = hoeveel.get_text(strip=True).replace('Pagina 1 van ', '')
            hoeveel_int = int(hoeveel_tekst)
        else:
            hoeveel_int = 1

        counter = 0
        index = 0
        
        #de algemene loop door de pagina's heen
        while counter < hoeveel_int:

            page_url = search_url + f"?page={counter+1}"
            response = requests.get(page_url)
            soup = BeautifulSoup(response.content, "html.parser")

            listings = soup.find_all('li', class_='hz-Listing')

            #selecteer per pagina de wat er in gebeurt
            for item in listings:
                title = item.find('h3', attrs={'class':'hz-Listing-title'})
                prijs = item.find('span', attrs={'class':'hz-Listing-price'})
                datum = item.find('span', attrs={'class':'hz-Listing-date'})
                website = item.find('a', attrs={'class': 'hz-TextLink'})
                mini_url = item.find('a', attrs={'class':'hz-Link'})

                #pakt de titel van de advertensie (pakt alleen wat er echt gevraagt word aan het systeem (dus ook niet wat er in de buurt van zit))
                if title:
                    title_value, title_text = title_garantes().marktplaats_title(title, search)
                else:
                    continue

                # zonder title die matcht mag die niet verder (haalt random stuf er om heen weg)
                if title_value == True:

                    #vraagt de prijs op (ook van bieden)
                    if prijs:
                        prijs_value, top_prijs = prijzen_check().marktplaats_prijs(prijs, item)
                    else:
                        prijs_value, top_prijs = None, None

                    #haalt de datums op van de advertentie
                    if datum:
                        datums = datum_check().marktplaats_datum(datum)
                    else:
                        continue

                    #laat zien of er een site aan gelinket staat (atm instabiel)
                    website_raw = bool(website)

                    #geeft de link van de advertensie (ook instabiel atm)
                    if mini_url and mini_url.has_attr("href"):
                        listing_url = "https://www.marktplaats.nl" + mini_url["href"]
                    else:
                        listing_url = None
                    
                    #geeft informatie over de locatie en de persoon zelf
                    if listing_url:
                        locaties = locatie().area(listing_url)
                        persoon, aantal_jaar, reviews = persoons().persoons_gegevens(listing_url)
                    else:
                        locaties, persoon, aantal_jaar, reviews = None, None, None, None

                    #update de dataframe met de nieuwe informatie
                    self.data[index] = {
                            'Naam':title_text,
                            'Prijs': prijs_value,
                            'Bieden': top_prijs,
                            'Datum': datums,
                            'Locatie':locaties,
                            'Verkoper':persoon,
                            'Vertrouwbaarheid':aantal_jaar,
                            'reviews':reviews,
                            'Website': website_raw,
                            'url': listing_url}
                    
                else:
                    continue
                
                index += 1

            counter += 1
        return self.data

