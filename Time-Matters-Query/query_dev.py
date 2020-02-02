from Time_Matters_SingleDoc import Time_Matters_SingleDoc
from Time_Matters_MultipleDocs import Time_Matters_MultipleDocs
from langdetect import detect
from lang import languages
import imp
import os

def query(query, max_items, offset):
    import requests
    payload = {'q': query, 'maxItems': max_items, 'offset': offset}
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

        page = requests.get(item["linkToExtractedText"])

        content = page.content.decode('utf-8')
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


def Time_Matters_Query(query_text, temporal_tagger=[], time_matters=[], max_items=3, offset=0, search_type='singleText', heroku=False):
    if heroku:
        path = imp.find_module('py_heideltime')[1]
        full_path = path + "/Heideltime/TreeTaggerLinux/bin/*"
        command = 'chmod 111 ' + full_path
        result_comand = os.popen(command).read()
        print(result_comand)
    list = query(query_text, max_items, offset)
    list_of_docs = []
    json = {'query': []}
    for i in range(len(list)):
        one_sentence = list[i][0].split('. ')

        try:
            if search_type == 'singleText':
                json['query'] += [{'title': list[i][2], 'url': list[i][3], 'oneSentence': one_sentence[0] + "...", 'dates': []}]
                dates = Time_Matters_SingleDoc(list[i][0],time_matters=time_matters, temporal_tagger=temporal_tagger, score_type='ByDoc', debug_mode=False)
                print()
                json['query'][i]['dates'].append(dates[0])
                json['query'][i]['dates'].append(dates[3])
            elif search_type == 'multipleText':
                json['query'] += [{'title': list[i][2], 'url': list[i][3], 'oneSentence': one_sentence[0] + "..."}]

                list_of_docs.append(list[i][0])
            else:
                print('Please specify a valid type of search\n'
                      'options:\n'
                      '     singleText;\n'
                      '     multipleText;')
                return {}
        except:
            pass
    if search_type == 'multipleText':
        dates = Time_Matters_MultipleDocs(list_of_docs, time_matters, temporal_tagger, score_type='ByDoc', debug_mode=True)
        json['query'].append({'dates': dates[0]})
        json['query'].append({'dates': dates[0]})
    return json


if __name__ == '__main__':
    json = Time_Matters_Query('Cristiano Ronaldo', temporal_tagger=['rule_based'], time_matters=[1], max_items=1, offset=0, search_type='singleText')
    print(json)