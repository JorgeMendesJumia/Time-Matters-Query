# Time-Matters-Query
## How to install Time-Matters-Query
```bash
pip install git+https://github.com/JMendes1995/Time-Matters-Query.git
```
## How to use Time-Matters-Query
### Time-Matters-Query with arquivo.pt api
``` bash
from Time_Matters_Query import Query

max_items=3
offset=0
query = Query(max_items, offset)
domains = ['http://publico.pt/', 'http://www.dn.pt/']
q = 'guerra na síria'
result_articles = query.arquivo_pt(q,domains)
```

#### _arquivo_pt  parameters_
- `q` : <b>(requireded)</b> query to search.
- `max_items` : <b>(optional)</b> Maximum number of items on the response.(Default: 50, Max: 2000) 
- `offset`: <b>(optional)</b> The position of the text indices where the search begins. (Default: 0)
- `domains`: <b>(optional)</b> List of domains to search into (e.g. ['http://publico.pt/', 'http://www.dn.pt/'])
- `from` : <b>(optional)</b> Set an initial date for the time span of the search. Format: YYYYMMDDHHMMSS, also accepts a shorter date fotmat, e.g. (YYYY). (Default: 1996)
- `to` : <b>(optional)</b> Set a end date for the time span of the search. format: YYYYMMDDHHMMSS, also accepts a shorter date format, for example (YYYY). (Default: Current Year-1)
- `url` : <b>(optional)</b> Custom url  (e.g. https://arquivo.pt/textsearch?versionHistory=http://www.ipt.pt&maxItems=1000&from=2010&to=2016)

###### Output
The output will be a list of dictionaries composed by:
- `fullContentLenght_Newspaper3K`: full content extracted by Newspaper3K
- `Summary_Newspaper3k`: summarized content by Newspaper3K
- `fullContentLenght_Arquivo`: full content extracted by arquivo.pt
- `snippet`: Snippet extracted by arquivo.pt
- `crawledData`: Content Timestamp 
- `title`: Page Title
- `url`: arquivo.pt URL
- `domain`:  list of domains userd to perform the search

### Temporal search with Time-Matters
```bash
list_articles = [article['fullContentLenght_Newspaper3K'] for article in result_articles]

temporal_search_multiple_doc = query.Time_Matters_MultipleDocs(articles)
```
