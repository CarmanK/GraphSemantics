from elasticsearch import Elasticsearch
es = Elasticsearch()

# Create a list of document dictionaries from the scraptedText file
# docs = []
# with open("scrapedText.txt", "r") as file:
#     lines = file.readlines()
#     for x in range(0, len(lines), 3):
#         docs.append({
#             "abstract": lines[x + 1][:-2] + ' ' + lines[x + 2][:-2]
#         })

# # # Index the dictionaries to the elasticsearch server
# i = 1
# for doc in docs:
#     es.index(index = "pubmed", id = i, body = doc)
#     i += 1

# # Index the abstracts from the other PubMed data
# with open("10.txt", "r", encoding = "ISO-8859-1") as file:
#     lines = file.readlines()
#     for line in lines:
#         es.index(index = "pubmed", id = i, body = {
#             "abstract": line[:-2]
#         })
#         i += 1
#         if i % 1000 == 0:
#             print(i)

# Allows all the newly indexed items to be searchable
# es.indices.refresh(index = "pubmed")

# To delete all indexes
# curl -X DELETE 'http://localhost:9200/_all'

# sudo systemctl start elasticsearch.service
# sudo systemctl stop elasticsearch.service






# doc = {
#     'author': 'kimchy',
#     'title': 'title1',
#     'text': 'Elasticsearch: cool. bonsai cool.',
#     'timestamp': datetime.now(),
# }
# res = es.index(index="test-index", doc_type='tweet', id=1, body=doc)
# print(res['result'])

# doc = {
#     'author': 'kevin',
#     'text': 'text here',
#     'title': 'this is the title',
#     'timestamp': datetime.now(),
# }
# res = es.index(index="test-index", doc_type='tweet', id=2, body=doc)
# print(res['result'])

# res = es.get(index="test-index", doc_type='tweet', id=1)
# print(res['_source'])

# es.indices.refresh(index="test-index")

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

