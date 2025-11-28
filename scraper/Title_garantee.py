class title_garantes:
    @staticmethod
    def marktplaats_title(title, search):
        title_lower = title.get_text(strip=True)
        search = search.replace('+', ' ')
        return search.lower() in title_lower.lower(), title_lower
