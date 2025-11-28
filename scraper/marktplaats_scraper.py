import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from Title_garantee import title_garantes
from prijsen_select import prijzen_check
from Datum_select import datum_check

data = {}
info ={}

def martktplaats_scrape(search):
    search_url = f'https://www.marktplaats.nl/q/{search}'
    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, "html.parser")

    hoeveel = soup.find('span', attrs={'class': 'hz-PaginationControls-pagination-amountOfPages'})
    hoeveel_tekst = hoeveel.get_text(strip=True).replace('Pagina 1 van ', '')
    hoeveel_int = int(hoeveel_tekst)

    counter = 0
    index = 0
    
    while counter < hoeveel_int:

        page_url = search_url + f"?page={counter+1}"
        response = requests.get(page_url)
        soup = BeautifulSoup(response.content, "html.parser")

        listings = soup.find_all('li', class_='hz-Listing')

        for item in listings:
            title = item.find('h3', attrs={'class':'hz-Listing-title'})
            prijs = item.find('span', attrs={'class':'hz-Listing-price'})
            datum = item.find('span', attrs={'class':'hz-Listing-date'})
            website = item.find('a', attrs={'class': 'hz-TextLink'})
            mini_url = item.find('a', attrs={'class':'hz-Link'})

            title_value, title_text = title_garantes().marktplaats_title(title, search)

            if title_value == True:
                prijs_value, top_prijs = prijzen_check().marktplaats_prijs(prijs, item)
                datums = datum_check().marktplaats_datum(datum)
                website_raw = bool(website)

                if mini_url.has_attr("href"):
                    listing_url = "https://www.marktplaats.nl" + mini_url["href"]
                else:
                    listing_url = None

                        
                data[index] = {
                        'Naam':title_text,
                        'Prijs': prijs_value,
                        'Bieden': top_prijs,
                        'Datum': datums,
                        'Website': website_raw,
                        'url': listing_url}
                
            else:
                continue
            
            index += 1

        counter += 1


if __name__ == '__main__':
    search = input('Zoekterm: ').replace(' ', '+')
    martktplaats_scrape(search)
    df = pd.DataFrame.from_dict(data, orient='index')
    print(df)