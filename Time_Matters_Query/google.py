def google(self, query):
    from googlesearch import search
    list = []
    for url in search(query, tld='com', start=self.offset, stop=self.max_items):
        if self.newspaper3k:
            fullContentLenght_Newspaper3K, Summary_Newspaper3k = newspaper3k_get_text(url)

            r = requests.get(url)
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(r.text, 'lxml')
            result = {'fullContentLenght_Newspaper3K': fullContentLenght_Newspaper3K,
                      'Summary_Newspaper3k': Summary_Newspaper3k,
                      'fullContentLenght': soup.text.encode( ).decode('utf-8'),
                      'url': url}
            list.append(result)

    return list