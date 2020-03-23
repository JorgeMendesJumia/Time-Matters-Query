import requests
from newspaper import Article
from joblib import Parallel, delayed


class Query():
    def __init__(self, max_items=50, offset=0, newspaper3k=False):
        self.max_items = max_items
        self.offset = offset
        self.newspaper3k=newspaper3k

    def arquivo_pt(self, query,  domains=[], beginDate='', endDate='', link=''):
        domain_list = []
        content_list = []
        import time
        start_time = time.time()

        if domains != []:
            for domain in domains:
                if link == '':
                    arquivo_pt = 'http://arquivo.pt/textsearch'
                    payload = {'q': query,
                               'maxItems': self.max_items,
                               'offset': self.offset,
                               'siteSearch': domain,
                                'from':beginDate,
                                'to':endDate,
                                'fields':'title,originalURL,linkToExtractedText,linkToNoFrame,linkToArchive,tstamp,date,siteSearch,snippet'}
                    r = requests.get(arquivo_pt, params=payload)
                    contentsJSon = r.json()
                    final_list, domain_list = self.request_arquivo_api(domain_list, contentsJSon)
                    for i in final_list:
                        content_list.append(i)
                else:
                    r = requests.get(link)
                    contentsJSon = r.json()
                    final_list, domain_list = self.request_arquivo_api(domain_list, contentsJSon)
                    for i in final_list:
                        content_list.append(i)
        else:
            if link == '':
                arquivo_pt = 'http://arquivo.pt/textsearch'
                payload = {'q': query,
                           'maxItems': self.max_items,
                           'offset': self.offset,
                           'from': beginDate,
                           'to': endDate,
                           'fields': 'title,originalURL,linkToExtractedText,linkToNoFrame,linkToArchive,tstamp,date,siteSearch,snippet'}
                r = requests.get(arquivo_pt, params=payload)
            else:
                r = requests.get(link)
            contentsJSon = r.json()
            content_list, domain_list = self.request_arquivo_api(domain_list, contentsJSon)

        total_time = time.time() - start_time
        lt=[]
        for i in content_list:
            if i not in lt:
                lt.append(i)
        statistical_dict = search_statistics(total_time, len(lt), len(domain_list), domain_list)
        final_output=[statistical_dict, lt]
        return final_output

    def google(self, query):
        from googlesearch import search
        list = []
        for url in search(query, tld='com', start = self.offset, stop=self.max_items):
            if self.newspaper3k:
                fullContentLenght_Newspaper3K, Summary_Newspaper3k = newspaper3k_get_text(url)

                r = requests.get(url)
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(r.text, 'lxml')
                result = {'fullContentLenght_Newspaper3K':fullContentLenght_Newspaper3K,
                          'Summary_Newspaper3k':Summary_Newspaper3k,
                           'fullContentLenght': soup.text.encode().decode('utf-8'),
                           'url':url}
                list.append(result)


        return list


# ------------------------------------------------------------------------------------------------------

    def request_arquivo_api(self, domain_list, contentsJSon):
        result_list = []
        import multiprocessing

        multiprocessing.cpu_count()
        x = Parallel(n_jobs=multiprocessing.cpu_count() * 2)(
            delayed(format_output)(item, self.newspaper3k) for item in contentsJSon["response_items"])

        for item in x:
            if item[0] != {}:
                result_list.append(item[0])
                if item[1] not in domain_list:
                    domain_list.append(item[1])
        return result_list, domain_list

def newspaper3k_get_text(url):
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()
    return article.text, article.summary


def format_output(item, newspaper3k):
    import re
    fetched_domain = re.findall('https://(.+?)/|http://(.+?)/',item['originalURL'])
    domain = [ d for d in fetched_domain[0] if d != ""]

    from Time_Matters_Query import normalization
    snippet= normalization(item['snippet'], html_strip=True, contraction_expansion=False)
    if newspaper3k == True:
        try:
            fullContentLenght_Newspaper3K, Summary_Newspaper3k = newspaper3k_get_text(item['linkToNoFrame'])
            result = {'fullContentLenght_Newspaper3K': fullContentLenght_Newspaper3K,
                      'Summary_Newspaper3k': Summary_Newspaper3k,
                      'snippet': snippet.replace('\xa0', '').replace('\x95', ''),
                      'crawledDate': item['tstamp'],
                      'title': item["title"].replace('\xa0', '').replace('\x95', ''),
                      'url': item["linkToArchive"],
                      'domain': domain[0]}
        except:
            return {}, domain[0]
    else:
        page = requests.get(item["linkToExtractedText"])
        from Time_Matters_Query import normalization
        fullContentLenght_Arquivo = page.content.decode(encoding = 'UTF-8',errors = 'strict').replace('\xa0', '').replace('\x95', '')
        try:
            result = {'fullContentLenght_Arquivo': fullContentLenght_Arquivo,
                      'snippet': snippet.replace('\xa0', '').replace('\x95', ''),
                      'crawledDate': item['tstamp'],
                      'title': item["title"].replace('\xa0', '').replace('\x95', ''),
                      'url': item["linkToArchive"],
                      'domain': domain[0]}
        except:
            return {}, domain[0]
    return result, domain[0]


def search_statistics(total_time, max_items, n_domains, domains):
    statistical_dict = {
       'time': total_time,
        'n_docs': max_items,
        'n_domains': n_domains,
        'domains': domains}
    return statistical_dict