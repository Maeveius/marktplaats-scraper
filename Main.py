import numpy as np
import pandas as pd

from scraper.marktplaats_scraper import Scrap

class main:
    def into():
        print('selecteer:')
        print('1: searcher voor deals')
        print('2: test')



        selected = int(input())

        if selected == 1:
            search = input('Zoekterm: ').replace(' ', '+')
            result = Scrap().martktplaats_scrape(search)
            df = pd.DataFrame.from_dict(result, orient='index')
            print(df)

        elif selected == 2:
            print('good stuff')

        



if __name__ == '__main__':
    main.into()