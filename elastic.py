from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch()

# Create a list of document dictionaries
docs = []
with open('scrapedText.txt', 'r') as file:
    lines = file.readlines()
    for x in range(0, len(lines), 3):
        docs.append({
            "title": lines[x + 1][:-2],
            "abstract": lines[x + 2][:-2]
        })

# Index the dictionaries to the elasticsearch server
i = 1
for doc in docs:
    es.index(index = "pubmed", doc_type = "Abstract", id = i, body = doc)
    i += 1

# Allows all the newly indexed items to be searchable
es.indices.refresh(index = "pubmed")

# Searches for all documents indexed as 'pubmed' and prints the results
res = es.search(index = "pubmed", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total']['value'])
for hit in res['hits']['hits']:
    print("Title: %(title)s\nAbstract: %(abstract)s" % hit["_source"])