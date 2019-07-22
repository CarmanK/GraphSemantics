import progressbar
from elasticsearch import Elasticsearch
es = Elasticsearch()

INDEX = 'patents'

with open('../input_data/elasticsearch_patent_data.txt', 'r') as corpus_file:
    lines = corpus_file.readlines()

try:
    # Allows all the newly indexed items to be searchable
    es.indices.refresh(index = INDEX)
    count = es.count(index = INDEX)['count']
except:
    count = 0

widgets = [
    ' [', progressbar.Timer(), '] ',
    progressbar.Bar(),
    ' (', progressbar.ETA(), ') ',
]

for line in progressbar.progressbar(lines, widgets = widgets):
    es.index(index = INDEX, id = count, body = {
        "abstract": line[:-1]
    })
    count += 1

es.indices.refresh(index = INDEX)

# To delete all indexes
# curl -X DELETE 'http://localhost:9200/_all'

# To start and stop the elasticsearch service
# sudo systemctl start elasticsearch.service
# sudo systemctl stop elasticsearch.service