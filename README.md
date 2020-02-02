# Time-Matters-Query

## How to use Time-Matters-Query
### Time-Matters-Query with arquivo.pt api
``` bash
from Time_Matters_Query import Query

max_items=1
starting_page=1
query = Query(max_items, starting_page)
articles = query.arquivo_pt('cristiano ronaldo')

temporal_search_single_doc = query.Time_Matters_SingleDoc(articles)
temporal_search_multiple_doc = query.Time_Matters_MultipleDocs(articles)

```
### Time-Matters-Query with google search engine

``` bash
from Time_Matters_Query import Query

max_items=1
starting_page=1
query = Query(max_items, starting_page)
articles = query.google('cristiano ronaldo')

temporal_search = query.Time_Matters_SingleDoc(articles)
temporal_search = query.Time_Matters_MultipleDocs(articles)
```