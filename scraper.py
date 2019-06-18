from html_requests import html_get
from bs4 import BeautifulSoup
import json
import os

# Scrape all of the titles and abstracts and store them per layer layer
output = []
with open('./input_data/links.json', 'r') as input_file:
    urls = json.load(input_file)
    for i in range(len(urls)):
        temp_output = []
        for j in range(len(urls[i])):
            raw_html = html_get(urls[i][j])
            if raw_html is not None:
                html = BeautifulSoup(raw_html, 'html.parser')

                html_titles = html.find(id = "primarycitation")
                if html_titles is not None:
                    title = html_titles.select('h4')[0].text
                else:
                    title = ""
                    print("Error finding title data at " + urls[i][j])

                html_paragraphs = html.find(id = "abstractFull")
                if html_paragraphs is not None:
                    abstract = html_paragraphs.select('p')[0].text
                else:
                    abstract = ""
                    print("Error finding abstract data at " + urls[i][j])
                
                temp_output.append(title + ' ' + abstract)
            else:
                print("Error scraping data from " + urls[i][j])
        output.append(temp_output)

# Save the data
if not os.path.exists('output_data'):
    os.mkdir('output_data')
with open('./output_data/scrapedText.json', 'w') as output_file:
    json.dump(output, output_file)