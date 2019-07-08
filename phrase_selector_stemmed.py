import json
from bs4 import BeautifulSoup
import math
from collections import Counter
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
ps = PorterStemmer()

TOP_K_SELECTED = 10 # Adjust this value to the desired number of phrases to return
BUFFER = 10 # This value shoudn't need to be adjusted. Its purpose is to lower the computation required for filtering the stopwords from the selected phrases.

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

    # Stem all of the phrases, also store the original phrase with the generated stem
    stem_list = []
    stem_phrase_pairs = []
    for i in range(len(parsed_list)):
        temp_stems, temp_stem_phrase_pairs = stem_phrases(parsed_list[i])
        stem_list.append(temp_stems)
        stem_phrase_pairs.append(temp_stem_phrase_pairs)
    # print(stem_list)
    # print(stem_phrase_pair)

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

    # Adjust the stem list to the format [[[{'phrase': TF_score}]]]
    combined_stem_tf = []
    for i in range(len(stem_frequency)):
        combined_stem_tf.append(combine_stem_tf(stem_frequency[i], tf_scores[i]))
    # print(combined_stem_tf)

    # Maximize the TF score
    maximized_tf_score = []
    for i in range(len(combined_stem_tf)):
        maximized_tf_score.append(tf_max(combined_stem_tf[i]))
    # print(maximized_tf_score)

    # Compute the TF-IDF score and combine the format to [[{'phrase':TF-IDF}]]
    tf_idf_score = []
    for i in range(len(maximized_tf_score)):
        tf_idf_score.append(tf_idf_calculator(idf_scores[i], maximized_tf_score[i]))
    # print(tf_idf_score)

    # Choose the TOP-K phrases
    buffered_top_phrases = []
    for i in range(len(tf_idf_score)):
        buffered_top_phrases.append(choose_top_phrases(tf_idf_score[i]))
    # print(buffered_top_phrases)

    # Filter the stopwords
    with open('./AutoPhrase/data/EN/stopwords.txt', 'r') as stopwords_file:
        stopwords = stopwords_file.readlines()
    filtered_top_phrases = []
    for i in range(len(buffered_top_phrases)):
        filtered_top_phrases.append(filter_stopwords(buffered_top_phrases[i], stopwords))
    # print(filtered_top_phrases)

    # Replace the stemmed phrases with their original phrases
    final_selected_phrases = []
    for i in range(len(filtered_top_phrases)):
        final_selected_phrases.append(unstem_phrases(filtered_top_phrases[i], stem_phrase_pairs[i]))
    # print(final_selected_phrases)

    # Output
    with open('./output_data/tmp/selected_phrases.json', 'w') as json_out:
        json.dump(final_selected_phrases, json_out, indent = 4)

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
    Return the stemmed phrases in a list along with a second list of dictionarys containing the pairs of stems and unstemmed words
    '''
    stemmed_layer = []
    before_and_after = []
    for i in range(len(unstemmed_layer)):
        temp_stemmed_phrase_list = []
        for phrase in unstemmed_layer[i]:
            stem = ps.stem(phrase)
            stem_dict = list(filter(lambda temp_stem_dict: temp_stem_dict['stem'] == stem, before_and_after))
            if stem_dict:
                if phrase not in stem_dict[0]['phrase']:
                    stem_dict[0]['phrase'].append(phrase)
            else:
                before_and_after.append({
                    'stem': stem,
                    'phrase': [phrase]
                })
            temp_stemmed_phrase_list.append(stem)
        stemmed_layer.append(temp_stemmed_phrase_list)
    return stemmed_layer, before_and_after

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

def combine_stem_tf(stem_frequency_layer, tf_score_layer):
    '''
    Combine the stem_frequency list and the tf_score list to the format [[[{'phrase': TF_score}]]]
    Return the newly formatted list
    '''
    combined_list = []
    for i in range(len(stem_frequency_layer)):
        index = 0
        temp_document = []
        for key in list(stem_frequency_layer[i].keys()):
            temp_document.append({key:tf_score_layer[i][index]})
            index += 1
        combined_list.append(temp_document)
    return combined_list

def tf_max(combined_stem_tf_layer):
    '''
    Find the maximum tf score for each phrase in the layer
    Return the maximum tf score for each phrase in the layer
    '''
    unique_phrase_list = []
    max_tf_list = []
    for i in range(len(combined_stem_tf_layer)):
        for j in range(len(combined_stem_tf_layer[i])):
            key = list(combined_stem_tf_layer[i][j].keys())[0]
            # Search for the maximum TF score for each key
            if key not in unique_phrase_list:
                max_tf = combined_stem_tf_layer[i][j][key]
                for k in range(len(combined_stem_tf_layer)):
                    for m in range(len(combined_stem_tf_layer[k])):
                        if key in list(combined_stem_tf_layer[k][m].keys()) and combined_stem_tf_layer[k][m][key] > max_tf:
                            max_tf = combined_stem_tf_layer[k][m][key]
                unique_phrase_list.append(key)
                max_tf_list.append(max_tf)
    
    # Combine the unique phrases with their respective max score
    maximized_tf_scores = []
    for i in range(len(unique_phrase_list)):
        maximized_tf_scores.append({unique_phrase_list[i]: max_tf_list[i]})
    return maximized_tf_scores

def tf_idf_calculator(idf_scores_layer, maximized_tf_scores_layer):
    '''
    Compute the TF-IDF score for each phrase in the layer
    Return the TF-IDF scores for the layer
    '''
    tf_idf_scores = []
    for i in range(len(idf_scores_layer)):
        key = list(idf_scores_layer[i].keys())[0]
        tf_idf_scores.append({
                'phrase': key,
                'score': idf_scores_layer[i][key] * maximized_tf_scores_layer[i][key]
            })
    return tf_idf_scores

def choose_top_phrases(tf_idf_scores_layer):
    '''
    Select the TOP K + BUFFER phrases
    Return the selected phrases
    '''
    sorted_list = sorted(tf_idf_scores_layer, key = lambda j: (j['score'], j['phrase']))
    return sorted_list[:TOP_K_SELECTED + BUFFER]

def filter_stopwords(buffered_top_phrases_layer, stopwords):
    '''
    Remove any phrases that are defined as stopwords from the layer
    Return the filtered list with the buyffer removed
    '''
    # Extract the phrases into a list
    phrase_list = []
    for i in range(len(buffered_top_phrases_layer)):
        phrase_list.append(buffered_top_phrases_layer[i]['phrase'])

    # Check the buffered amount of selected phrases against the provided stopwords
    stopword_indexes = []
    for i in range(len(phrase_list)):
        for word in stopwords:
            if phrase_list[i] == word:
                stopword_indexes.append(i)
                print('The selected phrase "' + word + '" was indetified as a stopword and removed.')
                break
    # Delete the identified stopwords from the list while ensuring at least K are returned
    stopword_indexes.reverse()
    for i in stopword_indexes:
        if len(phrase_list) <= TOP_K_SELECTED:
            print("Warning: Selected phrase quality may be lower than normal.")
            break
        else:
            del phrase_list[i]
    return phrase_list[:TOP_K_SELECTED]

def unstem_phrases(filtered_stemmed_layer, unstemmed_layer):
    '''
    Replace the stem with its original phrases
    Return a list of the original phrases
    '''
    # stem_dict = list(filter(lambda temp_stem_dict: temp_stem_dict['stem'] == stem, before_and_after))
    original_phrases = []
    for stem in filtered_stemmed_layer:
        original_dict = list(filter(lambda temp_pair: temp_pair['stem'] == stem, unstemmed_layer))
        original_phrases.append(original_dict[0]['phrase'])
    return original_phrases

if __name__ == '__main__':
    main()