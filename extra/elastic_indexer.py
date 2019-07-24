from elasticsearch import Elasticsearch
es = Elasticsearch()

INDEX = 'patents'

with open('./output_data/tmp/scraped_text.txt', 'r') as scraped_file:
    lines = scraped_file.readlines()

try:
    # Allows all the newly indexed items to be searchable
    es.indices.refresh(index = INDEX)
    count = es.count(index = INDEX)['count']
except:
    count = 0

# Index the unique data that is scraped from the website
# May just index duplicates in the future to reduce the massive computation time
duplicate_counter = 0
for line in lines:
    result = es.search(index = INDEX, body = {
        'query': {
            'match': {
                'abstract': {
                    'query': line[:-1],
                    'operator': 'and'
                }
            }
        }
    }, size = 1)
    if result['hits']['total']['value'] >= 1:
        duplicate_counter += 1
    else:
        # Index the unique data
        es.index(index = INDEX, id = count, body = {
            'abstract': line[:-1]
        })
        count += 1
        es.indices.refresh(index = INDEX)

print(str(len(lines) - duplicate_counter) + ' unique documents indexed.')