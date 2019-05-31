import requests
import pprint
query = "marcelo rebelo de sousa"
maxI = 5
payload = {'q': query,'maxItems': maxI}
r = requests.get('http://arquivo.pt/textsearch', params=payload)
contentsJSon = r.json()
pprint.pprint(contentsJSon)

for item in contentsJSon["response_items"]:
    title = item["title"]
    url = item["linkToArchive"]
    time = item["tstamp"]

    print(title)
    print(url)
    print(time)

    page = requests.get(item["linkToExtractedText"])
    # note a existencia de decode para garantirmos que o conteudo devolvido pelo Arquivo.pt (no formato ISO-8859-1) e impresso no formato (UTF-8)
    content = page.content.decode('utf-8')
    print(content)