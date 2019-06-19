from html_requests import html_get
from bs4 import BeautifulSoup
import json
import os

if not os.path.exists('output_data'):
    os.mkdir('output_data')
if not os.path.exists('output_data/tmp'):
    os.mkdir('output_data/tmp')

# Scrape all of the titles and abstracts and store them per layer in a json and line by line in a text file
output = []
lengths = []
with open('./input_data/links.json', 'r') as input_file:
    with open('./output_data/tmp/scraped_text.txt', 'w') as txt_output_file:
        urls = json.load(input_file)
        for i in range(len(urls)):
            length = 0
            temp_output = []
            for j in range(len(urls[i])):
                raw_html = html_get(urls[i][j])
                if raw_html is not None:
                    html = BeautifulSoup(raw_html, 'html.parser')

                    html_titles = html.find(id = 'primarycitation')
                    if html_titles is not None:
                        title = html_titles.select('h4')[0].text
                    else:
                        title = ''
                        print('Error finding title data at ' + urls[i][j])

                    html_paragraphs = html.find(id = 'abstractFull')
                    if html_paragraphs is not None:
                        abstract = html_paragraphs.select('p')[0].text
                    else:
                        abstract = ''
                        print('Error finding abstract data at ' + urls[i][j])
                    
                    temp = title + ' ' + abstract
                    temp_output.append(temp)
                    txt_output_file.write(temp + '\n')
                    length += 1
                else:
                    print('Error scraping data from ' + urls[i][j])
            output.append(temp_output)
            lengths.append(length)


# Save the data
with open('./output_data/scraped_text.json', 'w') as output_file:
    json.dump(output, output_file)
with open('./output_data/tmp/meta_scrapted_text.txt', 'w') as meta_file:
    json.dump(lengths, meta_file)
