from elasticsearch import Elasticsearch
es = Elasticsearch()

INDEX = 'pubmed'

# Allows all the newly indexed items to be searchable
es.indices.refresh(index = INDEX)
print(es.count(index = INDEX)['count'])


# res = es.search(index="test-index", body={"query": {"match_all": {}}})
# print("Got %d Hits:" % res['hits']['total']['value'])
# for hit in res['hits']['hits']:
#     print("%(timestamp)s %(author)s: %(text)s\n %(title)s" % hit["_source"])

# Allows all the newly indexed items to be searchable
# es.indices.refresh(index = "pubmed")

# Searches for all documents indexed as 'pubmed' and prints the results
# res = es.search(index = "pubmed") #Defaults size to 10
# print("Got %d Hits:" % res['hits']['total']['value'])

# res = es.count(index = "pubmed")
# print(res)


# Searches for all documents indexed as 'pubmed' and prints the results
# res = es.search(index = "pubmed") # Defaults size to 10
# print("Got %d Hits" % res['hits']['total']['value'])
# print(res)
# for hit in res['hits']['hits']:
#     print("Abstract: %(abstract)s" % hit["_source"])

# res = es.count(index = "pubmed")
# print("Count: " + res["count"])

# res = es.get(index = "pubmed", id = 24)
# print(res)

