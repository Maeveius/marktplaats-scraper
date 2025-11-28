

        


if __name__ == '__main__':
    search = input('Zoekterm: ').replace(' ', '+')
    martktplaats_scrape(search)
    df = pd.DataFrame.from_dict(data, orient='index')
    print(df)
    