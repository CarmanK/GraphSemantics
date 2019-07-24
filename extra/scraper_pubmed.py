from bs4 import BeautifulSoup
import json
import os
from requests import get
from requests.exceptions import RequestException
from contextlib import closing

def html_get(url):
    """
    Gets the content at `url` by making an HTTP GET request.
    If the content-type of the response is HTML, return the text content, otherwise return None.
    """
    try:
        with closing(get(url, stream = True)) as response:
            if is_html(response):
                return response.content
            else:
                return None

    except RequestException as e:
        print('Error during request to {0} : {1}'.format(url, str(e)))
        return None

def is_html(response):
    """
    Returns True if the response is HTML, false otherwise.
    """
    content_type = response.headers['Content-Type'].lower()
    return (response.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)

if not os.path.exists('output_data'):
    os.mkdir('output_data')
if not os.path.exists('output_data/tmp'):
    os.mkdir('output_data/tmp')

# This scraper is data specific and not written well
# Scrape all of the titles and abstracts and store the lines in a text file
lengths = []
with open('./input_data/links.json', 'r') as input_file:
    with open('./output_data/tmp/scraped_text.txt', 'w') as output_file:
        urls = json.load(input_file)
        for i in range(len(urls)):
            length = 0
            for j in range(len(urls[i])):
                raw_html = html_get(urls[i][j])
                if raw_html is not None:
                    html = BeautifulSoup(raw_html, 'html.parser')

                    html_titles = html.find(id = 'primarycitation')
                    if html_titles is not None:
                        title = html_titles.select('h4')[0].text
                        if title[-1:] is not '.':
                            title += '.'
                    else:
                        title = ''
                        print('Error finding title data at ' + urls[i][j])

                    html_paragraphs = html.find(id = 'abstractFull')
                    if html_paragraphs is not None:
                        abstract = html_paragraphs.select('p')[0].text
                    else:
                        abstract = ''
                        print('Error finding abstract data at ' + urls[i][j])
                    
                    output_file.write(title + ' ' + abstract + '\n')
                    length += 1
                else:
                    print('Error scraping data from ' + urls[i][j])
            lengths.append(length)


# Save the data
with open('./output_data/tmp/meta_scraped_text.json', 'w') as meta_file:
    json.dump(lengths, meta_file, indent = 4)