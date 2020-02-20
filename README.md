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
query = Query(max_items, offset, newspaper3k=True)
domain = 'http://www.ipt.pt'
from = '2010'
to = '2009'
q = 'guerra na síria'
result_articles = query.arquivo_pt(q,domain, from, to)
```
#### _Query parameters
- `max_items` : <b>(optional)</b> Maximum number of items on the response.(Default: 50, Max: 2000) 
- `offset`: <b>(optional)</b> The position of the text indices where the search begins. (Default: 0)
- `newspaper3k`: <b>(optional)</b> Flag to return the content extracted by Newspaper3K. (Default: True)

#### _arquivo_pt  parameters_
- `q` : <b>(requireded)</b> query to search.
- `url` : <b>(optional)</b> Custom domain (e.g. http://www.ipt.pt) or a list of domains (e.g. ['http://www.publico.pt', 'http://www.jn.pt'])
- `from` : <b>(optional)</b> Set an initial date for the time span of the search. Format: YYYYMMDDHHMMSS, also accepts a shorter date fotmat, e.g. (YYYY). (Default: 1996)
- `to` : <b>(optional)</b> Set a end date for the time span of the search. format: YYYYMMDDHHMMSS, also accepts a shorter date format, for example (YYYY). (Default: Current Year-1)

###### Output
The output will be a list of 2 dictionaries composed by:
- `time`: execution time of time-matters-query
- `n_docs`: Number of docs extracted.
- `n_domains`: Number of domains found in search.
- `fullContentLenght_Newspaper3K`: full content extracted by Newspaper3K
- `Summary_Newspaper3k`: summarized content by Newspaper3K
- `fullContentLenght_Arquivo`: full content extracted by arquivo.pt
- `snippet`: Snippet extracted by arquivo.pt
- `crawledData`: Content Timestamp 
- `title`: Page Title
- `url`: arquivo.pt URL
- `domain`:  list of domains userd to perform the search

