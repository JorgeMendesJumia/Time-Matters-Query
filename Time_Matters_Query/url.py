import requests
from newspaper import Article
from joblib import Parallel, delayed

from Time_Matters_Query.query import newspaper3k_get_text, search_statistics
class URL:
    def __init__(self, max_items=50, offset=0, newspaper3k=False):
        self.max_items = max_items
        self.offset = offset
        self.newspaper3k=newspaper3k

    def arquivo_pt(self, url='', beginDate='', endDate=''):
        domain_list = []
        import time
        start_time = time.time()
        arquivo_pt = 'http://arquivo.pt/textsearch'
        payload = {'versionHistory': url,
                       'maxItems': self.max_items,
                       'offset': self.offset,
                       'from': beginDate,
                       'to': endDate,
                       'fields': 'title,originalURL,linkToExtractedText,linkToNoFrame,linkToArchive,tstamp,date,siteSearch,snippet'}
        r = requests.get(arquivo_pt, params=payload)
        contentsJSon = r.json()
        result_list = []
        import multiprocessing

        multiprocessing.cpu_count()
        x = Parallel(n_jobs=multiprocessing.cpu_count() * 2)(
            delayed(format_output)(item, self.newspaper3k) for item in contentsJSon["response_items"])
        for item in x:
            if item[0] != {}:
                result_list.append(item[0])
            if item[1] not in domain_list and 'www.'+item[1] not in domain_list:
                domain_list.append(item[1])

        total_time = time.time() - start_time

        statistical_dict = search_statistics(total_time, len(result_list), len(domain_list), domain_list)
        final_output = [statistical_dict, result_list]
        return final_output



def format_output(item, newspaper3k):
    import re
    fetched_domain = re.findall('''https://(.+?)/|http://(.+?)/''', item['originalURL'])

    domain = [d for d in fetched_domain[0] if d != "" ]
    if newspaper3k == True:
        try:
            fullContentLenght_Newspaper3K, Summary_Newspaper3k = newspaper3k_get_text(item['linkToNoFrame'])
            result = {'fullContentLenght_Newspaper3K': fullContentLenght_Newspaper3K,
                      'Summary_Newspaper3k': Summary_Newspaper3k,
                      'crawledDate': item['tstamp'],
                      'title': item["title"].replace('\xa0', '').replace('\x95', ''),
                      'url': item["linkToArchive"],
                      'domain': domain[0]}
        except:
            return {}, domain[0]
    else:
        try:
            page = requests.get(item["linkToExtractedText"])
            fullContentLenght_Arquivo = page.content.decode(encoding = 'UTF-8',errors = 'strict').replace('\xa0', '').replace('\x95', '')

            result = {'fullContentLenght_Arquivo': fullContentLenght_Arquivo,
                          'crawledDate': item['tstamp'],
                          'title': item["title"].replace('\xa0', '').replace('\x95', ''),
                          'url': item["linkToArchive"],
                          'domain': domain[0]}
        except:
            return {}, domain[0]

    return result, domain[0]

