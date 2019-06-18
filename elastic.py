import os
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

# Searches the elasticsearch data for every pair of phrases within the layer and outputs the top-k ids, and articles for every phrase to a json file
if not os.path.exists('output_data'):
    os.mkdir('output_data')
k = 50 # Number of articles to return and output to the json
input_files = [
    "layer_1.json",
    "layer_2.json",
    "layer_3.json"
]
layer_index = 1
for input in input_files:
    keys = []
    output_data = []
    with open("./output_data/layer_" + str(layer_index) + "_output.json", "w") as output_file:
        with open("./jupter/top_k_output/" + input, "r") as file:
            layer = json.load(file)
        for key in layer: # This makes a list of all the attribute names of the input json file
            keys.append(key)
        for i in range(len(keys)):
            for j in range(i, len(keys)):
                if i != j:
                    result = es.search(index = "pubmed", body = {
                        "query": {
                            "match": {
                                "abstract": keys[i] + " " + keys[j]
                            }
                        }
                    }, size = k)
                    top_articles = result["hits"]["total"]["value"]
                    if top_articles > k: # We selected our top-k articles to be 10 instead of 100
                        top_articles = k
                    for x in range(top_articles):
                        output_data.append({
                            "phrase": keys[i] + " " + keys[j],
                            "id": result["hits"]["hits"][x]["_id"],
                            "article": result["hits"]["hits"][x]["_source"]["abstract"]
                        })
        json.dump(output_data, output_file)
    layer_index += 1