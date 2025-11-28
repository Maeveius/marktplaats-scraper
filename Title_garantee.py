class title_garantes:
    def marktplaats_title(self,title, search):
        search = search.replace('+', ' ')
        return search.lower() in title.lower()