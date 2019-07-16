import json
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
url = 'http://www.patentsview.org/api/patents/query?q={"patent_number":["4474388"]}'
# url = 'http://www.patentsview.org/api/patents/query?q='
# patent = {'patent_number': ["0"]}

try:
    with closing(get(url, stream = True)) as response:
        print(response.content)
except RequestException as e:
    print('Error during request to {0} : {1}'.format(url, str(e)))