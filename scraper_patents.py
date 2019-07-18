from bs4 import BeautifulSoup
import json
import os
import requests
from requests.exceptions import RequestException
from contextlib import closing
import time
import random

def main():
    # This scraper is data specific
    # Scrape all of the titles and sbtracts and store the lines in a text file
    if not os.path.exists('output_data'):
        os.mkdir('output_data')
    if not os.path.exists('output_data/tmp'):
        os.mkdir('output_data/tmp')

    url = 'https://patents.google.com/patent/US'
    url2 = '/en?oq='

    with open('./input_data/patent_ids.txt', 'r') as input_file:
        patent_ids = input_file.readlines()
    
    with open('./output_data/tmp/scraped_patent_text.txt', 'w') as output_file:
        for id in range(0, 10000):
            raw_html = html_get(patent_ids[id], url, url2)
            if raw_html is not None:
                html = BeautifulSoup(raw_html, 'html.parser')
                divs = html.findAll("div", {"class": "abstract"})
                if divs:
                    output_file.write(divs[0].get_text() + '\n')
                else:
                    print(patent_ids[id])

                # abstract = html.find_all(['p'])[0].get_text()
                # if abstract[:21] != '  Current U.S. Class:':
                #     # Clean up the abstract
                #     abstract = abstract.replace('\n', '')
                #     abstract = abstract.replace('    ', '')
                #     output_file.write(abstract + '\n')
                # else:
                #     print('The abstract of ID "' + patent_ids[id][:-1] + '" could not be found.')

def html_get(id, url, url2):
    '''
    Gets the content at `url` by making an HTTP GET request.
    If the content-type of the response is HTML, return the text content, otherwise return None.
    '''
    # time.sleep(random.random())
    # session = requests.Session()
    # session.headers.update({'Host': 'patft.uspto.gov',
    #                         'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
    #                         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #                         'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
    #                         'Accept-Encoding': 'gzip, deflate',
    #                         'Connection': 'keep-alive',
    #                         'Pragma': 'no-cache',
    #                         'Cache-Control': 'no-cache'})
    url += (id[:-1] + url2 + id[:-1])
    try:
        with closing(requests.get(url, stream = True)) as response:
            if is_html(response):
                return response.content
            else:
                return None
    except RequestException as e:
        print('Error during request to {0} : {1}'.format(url, str(e)))
        return None

def is_html(response):
    '''
    Returns True if the response is HTML, false otherwise.
    '''
    content_type = response.headers['Content-Type'].lower()
    return (response.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)

if __name__ == '__main__':
    main()