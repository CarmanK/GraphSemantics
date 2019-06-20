import json
from elasticsearch import Elasticsearch
es = Elasticsearch()

TOP_K = 10 # Number of articles to return per pair of phrase
INDEX = 'pubmed'

with open('./output_data/tmp/selected_phrases.json', 'r') as input_file:
    keylist = json.load(input_file)

es.indices.refresh(index = INDEX)

# Searches the elasticsearch data for every pair of phrases within the layer and outputs the top-k ids, and articles for every phrase to a json file
output = []
for i in range(len(keylist)):
    layer_output = []
    for j in range(len(keylist[i])):
        for k in range(j, len(keylist[i])):
            if j != k:
                result = es.search(index = INDEX, body = {
                    'query': {
                        'match': {
                            'abstract': keylist[i][j] + ' ' + keylist[i][k]
                        }
                    }
                }, size = TOP_K)
                top_articles = result['hits']['total']['value']
                if top_articles > TOP_K:
                    top_articles = TOP_K
                for x in range(top_articles):
                    layer_output.append({
                        'phrase': keylist[i][j] + ' ' + keylist[i][k],
                        'article': result['hits']['hits'][x]['_source']['abstract']
                    })
    output.append(layer_output)

with open('./output_data/tmp/article_pool.json', 'w') as output_file:
    json.dump(output, output_file, indent = 4)