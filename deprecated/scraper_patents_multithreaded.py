from bs4 import BeautifulSoup
import json
import os
import sys
import requests
from requests.exceptions import RequestException
from contextlib import closing
import threading
import shutil

def main(patent_ids, lower_bound, upper_bound, url, url2, thread_number):
    # This scraper is data specific
    # Scrape all of the titles and sbtracts and store the lines in a text file
    path = './output_data/tmp/threads/scraped_patent_text_' + str(thread_number) + '.txt'
    with open(path, 'w', encoding = 'utf-8') as output_file:
        for i in range(lower_bound, upper_bound):
            raw_html = html_get(patent_ids[i], url, url2)
            if raw_html is not None:
                html = BeautifulSoup(raw_html, 'html.parser')
                
                spans = html.findAll('span', {'itemprop': 'title'})
                title = ''
                if spans:
                    title = spans[0].get_text()[:-1].strip()
                    if title[-1:] != '.':
                        title += '.'
                
                divs = html.findAll('div', {'class': 'abstract'})
                abstract = ' '
                if divs:
                    abstract += divs[0].get_text()[:-1]
                    if abstract[-1:] != '.':
                        abstract += '.'

                combined = (title + abstract + '\n')
                output_file.write(combined)

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
    if not os.path.exists('output_data'):
        os.mkdir('output_data')
    if not os.path.exists('output_data/tmp'):
        os.mkdir('output_data/tmp')
    if os.path.exists('output_data/tmp/threads'):
        shutil.rmtree('output_data/tmp/threads')
    os.mkdir('output_data/tmp/threads')
    
    THREADS = 16
    url = 'https://patents.google.com/patent/US'
    url2 = '/en?oq='

    with open('./input_data/patent_ids.txt', 'r') as input_file:
        patent_ids = input_file.readlines()

    threads = []
    section = len(patent_ids) / THREADS
    for i in range(0, THREADS):
        lower_bound = int(section * i)
        upper_bound = int(section * (i + 1))
        threads.append(threading.Thread(target = main, args = (patent_ids, lower_bound, upper_bound, url, url2, i,)))
        
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    # Combine all of the data collected by the threads into one file
    os.chdir('./output_data/tmp/threads/')
    files = os.listdir()
    if sys.platform == 'win32':    
        command = 'type '
    else:
        command = 'cat '
    for data in files:
        command += data + ' '
    os.system(command + '> ../scraped_text.txt')
    os.chdir('..')
    shutil.rmtree('./threads/')