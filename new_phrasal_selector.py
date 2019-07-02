import json
from bs4 import BeautifulSoup
import math
from collections import Counter
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
ps = PorterStemmer()

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
    # print(parsed_list)

    # Stem all of the phrases
    stem_list = []
    for i in range(len(parsed_list)):
        stem_list.append(stem_phrases(parsed_list[i]))
    # print(stem_list)

    # Count the stems
    stem_frequency = []
    for i in range(len(stem_list)):
        stem_frequency.append(stem_counter(stem_list[i]))
    # print(stem_frequency)

    # Compute the TF score
    total = 0
    length_index = 0
    tf_scores = []
    for i in range(len(stem_frequency)):
        tf_scores.append(tf_calculator(stem_frequency[i], lines[total:total + lengths[length_index]]))
        total += lengths[length_index]
        length_index += 1
    # print(tf_scores)

    # Compute the IDF score
    length_index = 0
    idf_scores = []
    for i in range(len(stem_frequency)):
        idf_scores.append(idf_calculator(stem_frequency[i], lengths[length_index] + 1))
        length_index += 1
    # print(idf_scores)

    # Normalize the TF score


    # Update the stem_frequency list to the format [[{'phrase': TF_score},]]


    # Compute the TF-IDF score and combine the format to [[{'phrase':TF-IDF}]]


    # Filter the stopwords


    # Output


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

def stem_phrases(unstemmed_layer):
    '''
    Stem all of the phrases in a given layer
    Return the stemmed phrases
    '''
    stemmed_layer = []
    for i in range(len(unstemmed_layer)):
        temp_stemmed_phrase_list = []
        for phrase in unstemmed_layer[i]:
            temp_stemmed_phrase_list.append(ps.stem(phrase))
        stemmed_layer.append(temp_stemmed_phrase_list)
    return stemmed_layer

def stem_counter(stemmed_layer):
    '''
    Count all of the unique stems in the layer
    Return the layer in counted form
    '''
    counted_layer = []
    for i in range(len(stemmed_layer)):
        counted_layer.append(Counter(stemmed_layer[i]))
    return counted_layer

def tf_calculator(counted_layer, documents):
    '''
    Calculate the term frequency value for each phrase in the layer
    Return the term frequency values for the layer
    '''
    # Determine the lengths of the documents in the layer
    document_lengths = []
    for sentence in documents:
        document_lengths.append(len(sentence.split(' ')))

    # Computer the term frequency value in the layer
    document_length_index = 0
    layer_tf_score = []
    for i in range(len(counted_layer)):
        temp_tf_score = []
        for key in list(counted_layer[i].keys()):
            temp_tf_score.append(counted_layer[i][key] / document_lengths[document_length_index])
        document_length_index += 1
        temp_tf_score.sort(reverse = True)
        layer_tf_score.append(temp_tf_score)
    return layer_tf_score

def idf_calculator(counted_layer, number_of_documents):
    '''
    Calculate the inverse document frequency for each unique phrase in the layer
    Return a list of dictionaries in the format [{'phrase': idf_score}]
    '''
    unique_phrase_list = []
    layer_idf_score = []
    for i in range(len(counted_layer)):
        for key in list(counted_layer[i].keys()):
            if key not in unique_phrase_list:
                unique_phrase_list.append(key)
                document_count = 1
                for j in range(1, len(counted_layer)):
                    if key in list(counted_layer[j].keys()):
                        document_count += 1
                layer_idf_score.append({key:math.log(number_of_documents / document_count)})
    return layer_idf_score

if __name__ == '__main__':
    main()