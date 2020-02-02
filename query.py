import requests
from langdetect import detect
from lang import languages
from Time_Matters_SingleDoc import Time_Matters_SingleDoc
from Time_Matters_MultipleDocs import Time_Matters_MultipleDocs

class Query():

    def __init__(self, max_items=0, offset=0, search_type='singleText'):
        self.max_items = max_items
        self.offset = offset
        self.search_type = search_type

    def arquivo_pt(self, query):

        arquivo_pt='http://arquivo.pt/textsearch'
        payload = {'q': query, 'maxItems': self.max_items, 'offset': self.offset}
        r = requests.get(arquivo_pt, params=payload)
        contentsJSon = r.json()
        list = []
        for item in contentsJSon["response_items"]:
            title = item["title"]
            url = item["linkToArchive"]
            date = item["date"]

            from datetime import datetime
            normal_date = datetime.fromtimestamp(int(date))
            import datetime
            formated_date = datetime.datetime.strptime(str(normal_date), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")

            page = requests.get(item["linkToExtractedText"])

            content = page.content.decode('utf-8')
            try:
                lang_code = detect(content)
                lang_name = 'English'
                for n_list_of_lang in range(len(languages)):
                    if lang_code in languages[n_list_of_lang]:
                        lang_name = languages[n_list_of_lang][1]
            except:
                lang_name = 'English'

            #list.append((content, lang_name, title, url, formated_date))
            list.append(content)
        return list


    def google(self, query):
        from googlesearch import search
        list = []
        for url in search(query, tld='com', start = self.offset, stop=self.max_items):
            print(url)
            import urllib.request

            r = requests.get(url)
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(r.text, 'lxml')

            #soup = BeautifulSoup(r.text, 'html.parser')
            list.append(soup.text.encode().decode('utf-8'))
            text = soup.find_all(text=True)
            #print(text)
        return list

    def Time_Matters_SingleDoc(self, list, temporal_tagger=['rule_based'], time_matters=[], score_type='ByDoc'):
        results = Time_Matters_SingleDoc(list[0], temporal_tagger=temporal_tagger, time_matters=time_matters, score_type=score_type, debug_mode=False)
        return results

    def Time_Matters_MultipleDocs(self, list, temporal_tagger=['rule_based'], time_matters=[], score_type='ByCorpus'):
        results = Time_Matters_MultipleDocs(list, temporal_tagger=temporal_tagger, time_matters=time_matters, score_type=score_type, debug_mode=False)
        return results