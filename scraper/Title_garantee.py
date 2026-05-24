class title_garantes:
    @staticmethod
    def marktplaats_title(title, search):
        title_lower = title.get_text(strip=True).lower()
        words = search.replace('+', ' ').lower().split()
        match = any(w in title_lower for w in words)
        return match, title.get_text(strip=True)

    @staticmethod
    def marktplaats_title_text(title_text, search):  # ← nieuw
        words = search.replace('+', ' ').lower().split()
        match = any(w in title_text.lower() for w in words)
        return match, title_text