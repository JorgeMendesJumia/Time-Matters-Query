import requests
from newspaper import Article
from joblib import Parallel, delayed
from random import random
import random
from multiprocessing import Pool
from itertools import repeat
import requests

class Query():
    def __init__(self, max_items=50, offset=0, newspaper3k=False):
        self.max_items = max_items
        self.offset = offset
        self.newspaper3k=newspaper3k

    def arquivo_pt(self, query,  domains=[], beginDate='', endDate='', link=''):
        import time
        start_time = time.time()
        if not (domains):
            domains=['']
        else:
            random.shuffle(domains)

        import multiprocessing

        with Pool(processes=multiprocessing.cpu_count()*4) as pool:
            results_by_domain = pool.starmap(self.getResultsByDomain,
                                             zip(domains, repeat(query),  repeat(beginDate), repeat(endDate), repeat(link)))
        results_flat_list = [item for sublist in results_by_domain for item in sublist['response_items']]

        with Pool(processes=multiprocessing.cpu_count()*4) as pool:
            result = pool.starmap(format_output,
                                             zip(results_flat_list, repeat(self.newspaper3k)))
        domains_list = [item[1] for item in result]
        filter_domains_list = list(dict.fromkeys(domains_list))

        docs_info_list = [item[0] for item in result]

        all_results = []

        for dominio_list in [dominio_list for dominio_list in results_by_domain if dominio_list is not None]:
            all_results.extend(dominio_list)

        total_time = time.time( ) - start_time
        statistical_dict = search_statistics(total_time, len(docs_info_list), len(filter_domains_list), filter_domains_list)
        final_output=[statistical_dict, docs_info_list]

        return final_output


    def getResultsByDomain(self, domain, query, beginDate, endDate, link):
        itemsPerSite = self.max_items
        if link == '':
            arquivo_pt = 'http://arquivo.pt/textsearch'
            payload = {'q': query,
                       'maxItems': self.max_items,
                       'offset': self.offset,
                       'siteSearch': domain,
                       'from': beginDate,
                       'to': endDate,
                       'itemsPerSite': itemsPerSite,
                       'fields': 'title,originalURL,linkToExtractedText,linkToNoFrame,linkToArchive,tstamp,date,siteSearch,snippet'}
            r = requests.get(arquivo_pt, params=payload)
            contentsJSon = r.json( )

        else:
            r = requests.get(link)
            contentsJSon = r.json( )

        return contentsJSon

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
    snippet= normalization(item['snippet'], html_strip=True, accented_char_removal=False, contraction_expansion=False,
                  text_lower_case=False, special_char_removal=False, remove_digits=False)
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
            return [{}, domain[0]]
    else:
        page = requests.get(item["linkToExtractedText"])
        from Time_Matters_Query import normalization
        fullContentLenght_Arquivo = page.content.decode(encoding = 'UTF-8',errors = 'strict').replace('\xa0', '').replace('\x95', '')
        full_content_arquivo = normalization(fullContentLenght_Arquivo, contraction_expansion=False)

        try:
            result = {'fullContentLenght_Arquivo': full_content_arquivo,
                      'snippet': snippet.replace('\xa0', '').replace('\x95', ''),
                      'crawledDate': item['tstamp'],
                      'title': item["title"].replace('\xa0', '').replace('\x95', ''),
                      'url': item["linkToArchive"],
                      'domain': domain[0]}
        except:
            return [{}, domain[0]]
    return [result, domain[0]]


def search_statistics(total_time, max_items, n_domains, domains):
    statistical_dict = {
       'time': total_time,
        'n_docs': max_items,
        'n_domains': n_domains,
        'domains': domains}
    return statistical_dict