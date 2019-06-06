import requests
import pprint
from Time_Matters_MultipleDoc import Time_Matters_MultipleDoc
from Time_Matters_SingleDoc import Time_Matters_SingleDoc
from langdetect import detect
from lang import languages


def query(query, max_items):
    import urllib
    import requests
    payload = {'q': query, 'maxItems': max_items}
    r = requests.get('http://arquivo.pt/textsearch', params=payload)
    import pprint
    contentsJSon = r.json()
    list = []
    for item in contentsJSon["response_items"]:
        title = item["title"]
        url = item["linkToArchive"]
        time = item["tstamp"]

        print(title)
        print(url)
        print(time)

        page = requests.get(item["linkToExtractedText"])
        #print(page.encoding)

        # note a existencia de decode para garantirmos que o conteudo devolvido pelo Arquivo.pt (no formato ISO-8859-1) e impresso no formato (UTF-8)
        content = page.content.decode('utf-8')
        print(content)
        lang_code = detect(content)
        lang_name = 'English'
        for n_list_of_lang in range(len(languages)):
            if lang_code in languages[n_list_of_lang]:
                lang_name = languages[n_list_of_lang][1]

        list.append((content, lang_name))
    return title, url, list


def time_matters_query(query_text, max_items):
    title, url, list = query(query_text, max_items)
    json = {}
    for i in range(len(list)):
        json[i] = {'title': title, 'url': url, 'dates': []}
        dates = Time_Matters_SingleDoc(list[i][0], language=list[i][1])
        array_dates = []
        for dt in dates:
            json[i]['dates'] += dt
    print(json)
    return json


# if __name__ == '__main__':
#    json = time_matters_query('Donald Trump', 2)
