import requests
from newspaper import Article
from joblib import Parallel, delayed

class Query():
    def __init__(self, max_items=50, offset=0, newspaper3k=True):
        self.max_items = max_items
        self.offset = offset
        self.newspaper3k=newspaper3k

    def arquivo_pt(self, query,  domains=[], beginDate='', endDate='', link=''):
        domain_list = []
        import time
        start_time = time.time()
        site_search = ','.join(domains)
        if link == '':
            arquivo_pt = 'http://arquivo.pt/textsearch'
            payload = {'q': query,
                       'maxItems': self.max_items,
                       'offset': self.offset,
                       'siteSearch': site_search,
                       'from':beginDate,
                       'to':endDate,
                       'fields':'title,originalURL,linkToExtractedText,linkToNoFrame,linkToArchive,tstamp,date,siteSearch,snippet'}
            r = requests.get(arquivo_pt, params=payload)
        else:
            r = requests.get(link)
        contentsJSon = r.json()
        result_list=[]
        import multiprocessing

        multiprocessing.cpu_count()
        x = Parallel(n_jobs=multiprocessing.cpu_count()*2)(delayed(format_output)(item, self.newspaper3k) for item in contentsJSon["response_items"])
        for item in x:
            if item[0] != {}:
                result_list.append(item[0])
            if item[1] not in domain_list:
                domain_list.append(item[1])

        total_time = time.time() - start_time

        statistical_dict = search_statistics(total_time, len(result_list), len(domain_list))
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


def newspaper3k_get_text(self, url):
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()
    return article.text, article.summary


def format_output(item, newspaper3k):
    import re
    domain = re.findall('(?:https://.+?/|http://.+?/)',item['originalURL'])
    from Time_Matters_Query import normalization
    snippet= normalization(item['snippet'], html_strip=True, contraction_expansion=False)
    if newspaper3k == True:
        try:
            fullContentLenght_Newspaper3K, Summary_Newspaper3k = newspaper3k_get_text(item['linkToNoFrame'])
            result = {'fullContentLenght_Newspaper3K': fullContentLenght_Newspaper3K,
                      'Summary_Newspaper3k': Summary_Newspaper3k,
                      'snippet': snippet,
                      'crawledData': item['tstamp'],
                      'title': item["title"],
                      'url': item["linkToArchive"],
                      'domain': domain[0]}
        except:
            return {}, domain[0]
    else:
        page = requests.get(item["linkToExtractedText"])
        from Time_Matters_Query import normalization
        fullContentLenght_Arquivo = page.content.decode('utf-8')
        try:
            result = {'fullContentLenght_Arquivo': fullContentLenght_Arquivo,
                      'snippet': snippet,
                      'crawledData': item['tstamp'],
                      'title': item["title"],
                      'url': item["linkToArchive"],
                      'domain': domain[0]}
        except:
            return {}, domain[0]
    return result, domain[0]


def search_statistics(total_time, max_items, n_domains):
    statistical_dict = {
       'time': total_time,
        'n_docs': max_items,
        'n_domains': n_domains
        }
    return statistical_dict