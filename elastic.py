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
top_k = 10 # Number of articles to return and output to the json
with open('./output_data/tmp/selected_phrases.json', 'r') as input_file:
    phrase_list = json.load(input_file)
keylist = []
for i in range(len(phrase_list)):
    keys = []
    for key in phrase_list[i]:
        keys.append(key)
    keylist.append(keys)

output = []
for i in range(len(keylist)):
    layer_output = []
    for j in range(len(keylist[i])):
        for k in range(j, len(keylist[i])):
            if j != k:
                result = es.search(index = "pubmed", body = {
                    "query": {
                        "match": {
                            "abstract": keylist[i][j] + " " + keylist[i][k]
                        }
                    }
                }, size = top_k)
                top_articles = result["hits"]["total"]["value"]
                if top_articles > top_k: # We selected our top-k articles to be 10 instead of 100
                    top_articles = top_k
                for x in range(top_articles):
                    layer_output.append({
                        "phrase": keylist[i][j] + " " + keylist[i][k],
                        "article": result["hits"]["hits"][x]["_source"]["abstract"]
                    })
    output.append(layer_output)

with open('./output_data/tmp/article_pool.json', 'w') as output_file:
    json.dump(output, output_file, indent = 4)