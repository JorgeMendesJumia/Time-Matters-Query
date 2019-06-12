from Time_Matters_SingleDoc import Time_Matters_SingleDoc
from langdetect import detect
from lang import languages


def query(query, max_items):
    import requests
    payload = {'q': query, 'maxItems': max_items}
    r = requests.get('http://arquivo.pt/textsearch', params=payload)
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
        print(formated_date)
        print('title'+title)
        print(url)

        page = requests.get(item["linkToExtractedText"])
        #print(page.encoding)

        # note a existencia de decode para garantirmos que o conteudo devolvido pelo Arquivo.pt (no formato ISO-8859-1) e impresso no formato (UTF-8)
        content = page.content.decode('utf-8')
        print(content)
        try :
            lang_code = detect(content)
            lang_name = 'English'
            for n_list_of_lang in range(len(languages)):
                if lang_code in languages[n_list_of_lang]:
                    lang_name = languages[n_list_of_lang][1]
        except:
            lang_name = 'English'

        list.append((content, lang_name, title, url, formated_date))
    return list


def time_matters_query(query_text, max_items, offset):
    import imp
    import os
    path = imp.find_module('py_heideltime')[1]
    full_path = path + "/Heideltime/TreeTaggerLinux"
    command = 'chmod 111 ' + full_path
    result_comand = os.popen(command).read()
    print(result_comand)
    list = query(query_text, max_items)
    json = {'query': []}
    for i in range(len(list)):
        one_sentence = list[i][0].split('. ')
        json['query'] += [{'title': list[i][2], 'url': list[i][3], 'oneSentence': one_sentence[0]+"...", 'dates': []}]
        try:
            dates = Time_Matters_SingleDoc(list[i][0], language=list[i][1], heideltime_document_creation_time=list[1][4])
            json['query'][i]['dates'].append(dates[0])
            json['query'][i]['dates'].append(dates[len(dates) - 1])
        except:
            pass
    print(json)
    return json


