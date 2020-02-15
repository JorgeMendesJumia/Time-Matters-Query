import requests
from langdetect import detect
from Time_Matters_Query.lang import languages
from Time_Matters_SingleDoc import Time_Matters_SingleDoc
from Time_Matters_MultipleDocs import Time_Matters_MultipleDocs
from datetime import datetime
from newspaper import Article

class Query():
    def __init__(self, max_items=50, offset=0):
        self.max_items = max_items
        self.offset = offset

    def arquivo_pt(self, query, max_items=50, offset=0, domains=[], from_date='', to_date='', url=''):
        result_list = []
        if url == '':
            arquivo_pt = 'http://arquivo.pt/textsearch'
            domains = ','.join(domains)
            payload = {'q': query,
                       'maxItems': max_items,
                       'offset': offset,
                       'siteSearch': domains,
                       'from':from_date,
                       'to':to_date,
                       'fields':'title,originalURL,linkToExtractedText,linkToNoFrame,linkToArchive,tstamp,date,siteSearch,snippet'}
            r = requests.get(arquivo_pt, params=payload)
        else:
            r = requests.get(url)

        contentsJSon = r.json()
        for item in contentsJSon["response_items"]:
            fullContentLenght_Newspaper3K, Summary_Newspaper3k = self.newspaper3k(item['linkToNoFrame'])
            page = requests.get(item["linkToExtractedText"])

            fullContentLenght_Arquivo = page.content.decode('utf-8')
            result = {'fullContentLenght_Newspaper3K':fullContentLenght_Newspaper3K,
                      'Summary_Newspaper3k':Summary_Newspaper3k,
                      'fullContentLenght_Arquivo': fullContentLenght_Arquivo,
                      'snippet':item['snippet'], 'crawledData':item['tstamp'],
                      'title':item["title"],
                      'url':item["linkToArchive"],
                      'domain':domains}

            result_list.append(result)
        return result_list

    def google(self, query):
        from googlesearch import search
        list = []
        for url in search(query, tld='com', start = self.offset, stop=self.max_items):
            r = requests.get(url)
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(r.text, 'lxml')

            #soup = BeautifulSoup(r.text, 'html.parser')
            list.append(soup.text.encode().decode('utf-8'))
            text = soup.find_all(text=True)
            #print(text)
        return list

    def Time_Matters_MultipleDocs(self, list, temporal_tagger=['rule_based'], time_matters=[], score_type='ByCorpus'):
        results = Time_Matters_MultipleDocs(list, temporal_tagger=temporal_tagger, time_matters=time_matters, score_type=score_type, debug_mode=False)
        return results

    def newspaper3k(self, url):
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()
        return article.text, article.summary
