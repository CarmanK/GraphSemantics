from elasticsearch import Elasticsearch
es = Elasticsearch()

# Create a list of document dictionaries from the scraptedText file
# docs = []
# with open('scrapedText.txt', 'r') as file:
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
# with open('10.txt', 'r', encoding = "ISO-8859-1") as file:
#     lines = file.readlines()
#     for line in lines:
#         es.index(index = "pubmed", id = i, body = {
#             "abstract": line[:-2]
#         })
#         i += 1
#         if i % 1000 is 0:
#             print(i)

# Allows all the newly indexed items to be searchable
# es.indices.refresh(index = "pubmed")

result = es.search(index = "pubmed", body = {
    "query": {
        "match_phrase": {
            "abstract": ""
        }
    }
})
print("%d Hits" % result['hits']['total']['value'])





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

# To delete all indexes
# curl -X DELETE 'http://localhost:9200/_all'