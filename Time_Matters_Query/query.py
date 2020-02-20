import requests
from langdetect import detect
from Time_Matters_Query.lang import languages
from Time_Matters_SingleDoc import Time_Matters_SingleDoc
from Time_Matters_MultipleDocs import Time_Matters_MultipleDocs
from datetime import datetime
from newspaper import Article
import time

class Query():
    def __init__(self, max_items=50, offset=0, newspaper3k=True):
        self.max_items = max_items
        self.offset = offset
        self.newspaper3k=newspaper3k

    def arquivo_pt(self, query,  domains=[], from_date='', to_date='', link=''):
        result_list = []
        site_search=[]
        d=[]
        import time
        start_time = time.time()
        if not isinstance(domains,list):
            site_search.append(domains)
        else:
            site_search=domains
        if link == '':
            arquivo_pt = 'http://arquivo.pt/textsearch'
            domains = ','.join(site_search)
            payload = {'q': query,
                       'maxItems': self.max_items,
                       'offset': self.offset,
                       'siteSearch': site_search,
                       'from':from_date,
                       'to':to_date,
                       'fields':'title,originalURL,linkToExtractedText,linkToNoFrame,linkToArchive,tstamp,date,siteSearch,snippet'}
            r = requests.get(arquivo_pt, params=payload)
        else:
            r = requests.get(link)

        contentsJSon = r.json()
        for item in contentsJSon["response_items"]:
            result, d = self.format_output(item, site_search, d)
            result_list.append(result)

        total_time = time.time() - start_time
        domains_list = list(set(d))

        statistical_dict = self.search_statistics(total_time, self.max_items, len(domains_list))
        print(domains_list)

        final_output=[statistical_dict, result_list]
        return final_output

    def google(self, query):
        from googlesearch import search
        list = []
        for url in search(query, tld='com', start = self.offset, stop=self.max_items):
            fullContentLenght_Newspaper3K, Summary_Newspaper3k = self.newspaper3k(url)

            r = requests.get(url)
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(r.text, 'lxml')
            result = {'fullContentLenght_Newspaper3K':fullContentLenght_Newspaper3K,
                      'Summary_Newspaper3k':Summary_Newspaper3k,
                      'fullContentLenght': soup.text.encode().decode('utf-8'),
                      'url':url}
            #soup = BeautifulSoup(r.text, 'html.parser')
            list.append(result)


        return list

    #def Time_Matters_MultipleDocs(self, list, temporal_tagger=['rule_based'], time_matters=[], score_type='ByCorpus'):
    #    results = Time_Matters_MultipleDocs(list, temporal_tagger=temporal_tagger, time_matters=time_matters, score_type=score_type, debug_mode=False)
    #    return results

    def newspaper3k_get_text(self, url):
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()
        return article.text, article.summary

    def format_output(self,item, domains, d):
        import re
        domain = re.findall('(?:https://.+?/|http://.+?/)',item['originalURL'])
        d.append(domain[0])

        if self.newspaper3k == True:
            fullContentLenght_Newspaper3K, Summary_Newspaper3k = self.newspaper3k_get_text(item['linkToNoFrame'])

            result = {'fullContentLenght_Newspaper3K': fullContentLenght_Newspaper3K,
                      'Summary_Newspaper3k': Summary_Newspaper3k,
                      'snippet': item['snippet'],
                      'crawledData': item['tstamp'],
                      'title': item["title"],
                      'url': item["linkToArchive"],
                      'domain': domain[0]}
        else:
            page = requests.get(item["linkToExtractedText"])

            fullContentLenght_Arquivo = page.content.decode('utf-8')
            result = {'fullContentLenght_Arquivo': fullContentLenght_Arquivo,
                      'snippet': item['snippet'],
                      'crawledData': item['tstamp'],
                      'title': item["title"],
                      'url': item["linkToArchive"],
                      'domain': domain[0]}
        return result, d

    def search_statistics(self, total_time, max_items, n_domains):
        statistical_dict = {
        'time': total_time,
        'n_docs': max_items,
        'n_domains': n_domains
        }
        return statistical_dict