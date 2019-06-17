import json
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

# This obviously shouldn't just be copy pasted 3 times and should be made scalable
# keys = []
# output_data = []
# with open("layer_1_output.json", "w") as output:
#     with open("layer_1.json") as file:
#         layer_1 = json.load(file)
#     for key in layer_1:
#         keys.append(key)
#     for i in range(len(keys)):
#         for j in range(i, len(keys)):
#             if i != j:
#                 # print(keys[i] + ' ' + keys[j])
#                 result = es.search(index = "pubmed", body = {
#                     "query": {
#                         "match": {
#                             "abstract": keys[i] + " " + keys[j]
#                         }
#                     }
#                 })
#                 # print("%d Hits" % result['hits']['total']['value'])
#                 top_articles = result["hits"]["total"]["value"]
#                 if top_articles > 10:
#                     top_articles = 10
#                 for k in range(top_articles):
#                     output_data.append({
#                         "phrase": keys[i] + " " + keys[j],
#                         "id": result["hits"]["hits"][k]["_id"],
#                         "article": result["hits"]["hits"][k]["_source"]["abstract"]
#                     })
#     json.dump(output_data, output)

# keys = []
# output_data = []
# with open("layer_2_output.json", "w") as output:
#     with open("layer_2.json") as file:
#         layer_1 = json.load(file)
#     for key in layer_1:
#         keys.append(key)
#     for i in range(len(keys)):
#         for j in range(i, len(keys)):
#             if i != j:
#                 # print(keys[i] + ' ' + keys[j])
#                 result = es.search(index = "pubmed", body = {
#                     "query": {
#                         "match": {
#                             "abstract": keys[i] + " " + keys[j]
#                         }
#                     }
#                 })
#                 # print("%d Hits" % result['hits']['total']['value'])
#                 top_articles = result["hits"]["total"]["value"]
#                 if top_articles > 10:
#                     top_articles = 10
#                 for k in range(top_articles):
#                     output_data.append({
#                         "phrase": keys[i] + " " + keys[j],
#                         "id": result["hits"]["hits"][k]["_id"],
#                         "article": result["hits"]["hits"][k]["_source"]["abstract"]
#                     })
#     json.dump(output_data, output)

# keys = []
# output_data = []
# with open("layer_3_output.json", "w") as output:
#     with open("layer_3.json") as file:
#         layer_1 = json.load(file)
#     for key in layer_1:
#         keys.append(key)
#     for i in range(len(keys)):
#         for j in range(i, len(keys)):
#             if i != j:
#                 # print(keys[i] + ' ' + keys[j])
#                 result = es.search(index = "pubmed", body = {
#                     "query": {
#                         "match": {
#                             "abstract": keys[i] + " " + keys[j]
#                         }
#                     }
#                 })
#                 # print("%d Hits" % result['hits']['total']['value'])
#                 top_articles = result["hits"]["total"]["value"]
#                 if top_articles > 10:
#                     top_articles = 10
#                 for k in range(top_articles):
#                     output_data.append({
#                         "phrase": keys[i] + " " + keys[j],
#                         "id": result["hits"]["hits"][k]["_id"],
#                         "article": result["hits"]["hits"][k]["_source"]["abstract"]
#                     })
#     json.dump(output_data, output)