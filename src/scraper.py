from bs4 import BeautifulSoup
import json
import os
import requests
from requests.exceptions import RequestException
from contextlib import closing
import progressbar

INPUT_FILE = 'sample.txt' # List of Patent IDs

def main():
    # This scraper is data specific
    # Scrape all of the titles and sbtracts and store the lines in a text file
    url = 'https://patents.google.com/patent/US'
    url2 = '/en?oq='

    widgets = [
        ' [', progressbar.Timer(), '] ',
        progressbar.Bar(),
        ' (', progressbar.ETA(), ') ',
    ]

    with open('../input_data/' + INPUT_FILE, 'r') as input_file:
        patent_ids = input_file.readlines()
    
    with open('../output_data/tmp/titles.txt', 'w') as output_file:
        with open('../output_data/tmp/abstracts.txt', 'w') as abstract_file:
            for id in progressbar.progressbar(patent_ids, widgets = widgets):
                raw_html = html_get(id, url, url2)
                if raw_html is not None:
                    html = BeautifulSoup(raw_html, 'html.parser')
                    
                    spans = html.findAll('span', {'itemprop': 'title'})
                    title = ''
                    if spans:
                        title = spans[0].get_text()[:-1].strip()
                        if title[-1:] != '.':
                            title += '.'
                    
                    divs = html.findAll('div', {'class': 'abstract'})
                    abstract = ''
                    if divs:
                        abstract += divs[0].get_text()[:-1]
                        if abstract[-1:] != '.':
                            abstract += '.'

                    if title != '':
                        output_file.write(title + '\n')
                    if abstract != '':
                        abstract_file.write(abstract + '\n')

def html_get(id, url, url2):
    '''
    Gets the content at `url` by making an HTTP GET request.
    If the content-type of the response is HTML, return the text content, otherwise return None.
    '''
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