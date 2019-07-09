import json
from elasticsearch import Elasticsearch
es = Elasticsearch()

TOP_K = 10 # Number of articles to return per pair of phrase
INDEX = 'pubmed'

def main():
    with open('./output_data/tmp/selected_phrases.json', 'r') as input_file:
        selected_phrases = json.load(input_file)

    es.indices.refresh(index = INDEX)
    
    # Query every possible pair of phrases within the layer to elasticsearch and outputs the top-k articles to a json file
    output = []
    for layer in selected_phrases:
        output.append(elastic_query(layer))
    print(output)

    with open('./output_data/tmp/article_pool.json', 'w') as output_file:
        json.dump(output, output_file, indent = 4)

def elastic_query(phrase_list):
    '''
    Queries elasticsearch for every pair of phrases in the layer
    Returns a list of the TOP-K articles from every query
    '''
    articles = []
    for i in range(len(phrase_list)):
        term_1 = ''
        term_2 = ''
        for phrase in phrase_list[i]:
            term_1 = (phrase + ' ')
        for j in range(i + 1, len(phrase_list)):
            for phrase in phrase_list[j]:
                term_2 = (phrase + ' ')
            pair = (term_1 + term_2)[:-1]
            result = es.search(index = INDEX, body = {
                'query': {
                    'match': {
                        'abstract': pair
                    }
                }
            }, size = TOP_K)
            top_articles = result['hits']['total']['value']
            for article in top_articles:
                articles.append({
                    'phrase': pair,
                    'article': result['hits']['hits'][x]['_source']['abstract']
                })
    return articles

if __name__ == '__main__':
    main()