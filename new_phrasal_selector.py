import json
from bs4 import BeautifulSoup
import math
from collections import Counter

TOP_K_SELECTED = 10 # Adjust this value to the desired number of phrases to return

def main():
    with open('./output_data/tmp/segmentation.txt', 'r') as segmentation_file:
        lines = segmentation_file.readlines()
    with open('./output_data/tmp/meta_scraped_text.json', 'r') as lengths_file:
        lengths = json.load(lengths_file)

    # Create a list of all of the parsed phrases for all of the layers
    total = 0
    parsed_list = []
    for length in lengths:
        parsed_list.append(parse_phrases(lines[total:total + length]))
        total += length

    print(parsed_list)

    # tf_list = []
    # for 
    # cnt = Counter(parsed_list[0][0])
    # print(cnt)

def parse_phrases(text):
    '''
    Parse the tagged phrases from the segmentated text file
    Return the phrases contained within the layer
    '''
    layer = []
    for i in range(len(text)):
        temp_list = []
        soup = BeautifulSoup(text[i], 'lxml')
        for j in soup.find_all(['phrase']):
            temp_list.append(j.get_text().lower())
        layer.append(temp_list)
    return layer

if __name__ == '__main__':
    main()