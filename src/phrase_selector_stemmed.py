import json
from bs4 import BeautifulSoup
import math
from collections import Counter
from nltk.stem import PorterStemmer
ps = PorterStemmer()
from nltk.tokenize import word_tokenize
from gensim import models
import re
import os

TOP_K_SELECTED = 10 # Adjust this value to the desired number of phrases to return
BUFFER = 10 # This value shoudn't need to be adjusted. Its purpose is to lower the computation required for filtering the stopwords from the selected phrases.
MODEL = 'Trained_Model' # The directory that contains the trained word2vec model

def main():
    with open('../output_data/tmp/segmentation.txt', 'r') as segmentation_file:
        lines = segmentation_file.readlines()
    # with open('../output_data/tmp/meta_scraped_text.json', 'r') as lengths_file:
    #     lengths = json.load(lengths_file)
    lengths = [len(lines)] # Temporary fix

    # Phrase Selection
    # Create a list of all of the parsed phrases for all of the layers
    total = 0
    parsed_list = []
    for length in lengths:
        parsed_list.append(parse_phrases(lines[total:total + length]))
        total += length

    # Stem all of the phrases, also store the original phrase with the generated stem
    stem_list = []
    stem_phrase_pairs = []
    for i in range(len(parsed_list)):
        temp_stems, temp_stem_phrase_pairs = stem_phrases(parsed_list[i])
        stem_list.append(temp_stems)
        stem_phrase_pairs.append(temp_stem_phrase_pairs)

    # Count the stems
    stem_frequency = []
    for i in range(len(stem_list)):
        stem_frequency.append(stem_counter(stem_list[i]))

    # Compute the TF score
    total = 0
    length_index = 0
    tf_scores = []
    for i in range(len(stem_frequency)):
        tf_scores.append(tf_calculator(stem_frequency[i], lines[total:total + lengths[length_index]]))
        total += lengths[length_index]
        length_index += 1

    # Compute the IDF score
    length_index = 0
    idf_scores = []
    for i in range(len(stem_frequency)):
        idf_scores.append(idf_calculator(stem_frequency[i], lengths[length_index] + 1))
        length_index += 1

    # Adjust the stem list to the format [[[{'phrase': TF_score}]]]
    combined_stem_tf = []
    for i in range(len(stem_frequency)):
        combined_stem_tf.append(combine_stem_tf(stem_frequency[i], tf_scores[i]))

    # Maximize the TF score
    maximized_tf_score = []
    for i in range(len(combined_stem_tf)):
        maximized_tf_score.append(tf_max(combined_stem_tf[i]))

    # Compute the TF-IDF score and combine the format to [[{'phrase':TF-IDF}]]
    tf_idf_score = []
    for i in range(len(maximized_tf_score)):
        tf_idf_score.append(tf_idf_calculator(idf_scores[i], maximized_tf_score[i]))

    # Choose the TOP-K phrases
    buffered_top_phrases = []
    for i in range(len(tf_idf_score)):
        buffered_top_phrases.append(choose_top_phrases(tf_idf_score[i]))

    # Replace the stemmed phrases with their original phrases
    top_original_phrases = []
    for i in range(len(buffered_top_phrases)):
        top_original_phrases.append(unstem_phrases(buffered_top_phrases[i], stem_phrase_pairs[i]))

    # Filter the stopwords
    with open('./AutoPhrase/data/EN/stopwords.txt', 'r') as stopwords_file:
        stopwords = stopwords_file.readlines()
    final_selected_phrases = []
    for i in range(len(top_original_phrases)):
        final_selected_phrases.append(filter_stopwords(top_original_phrases[i], stopwords))

    # Output selected phrases
    # with open('./output_data/tmp/selected_phrases.json', 'w') as json_out:
    #     json.dump(final_selected_phrases, json_out, indent = 4)

    # Ideas on how to implement this
    #1. Compute the top model.most_similar words and output them to a separate file. This file can then be used as a secondary ranking when selecting sentences.
    ### print(model_list[0].most_similar('golf'))
    #2. Check the selected phrases against each other and discard phrases that do not pass a threshold.
    ### print(model_list[0].similarity('golf', 'the'))
    #3. Check the selected phrases using the model.doesnt_match method in word2vec and discard phrases until they all match.
    ### print(model_list[0].doesnt_match(['golf', 'golfer', 'lightweight', 'band', 'mouth', 'play', 'upper', 'water', 'easy_access', 'weather']))

    # Word2Vec
    # Create a list of layers from segmentation.txt but remove the <phrase> tags and replace all of the spaces with underscores of multi-word tagged phrases
    total = 0
    formatted_abstracts = []
    for length in lengths:
        formatted_abstracts.append(phrase_formatter(lines[total:total + length]))
        total += length
    
    # Split the abstracts in a given layer into sentences and join them to one list per layer
    layers_of_sentences = []
    for layer in formatted_abstracts:
        layers_of_sentences.append(sentence_splitter(layer))

    # Load the respective word2vec model or train one to be used in the future
    path = '../word2vec_models/'
    if not os.path.exists(path):
        os.mkdir(path)
        print('No trained word2vec model can be found at the specified path!')
    else:
        if not os.path.exists(path + MODEL + '.model'):
            print('No trained word2vec model can be found at the specified path!')
        else:
            model = models.Word2Vec.load(path + MODEL + '.model')

            # Implementing option 1.
            # Generate the most similar words of each of the selected phrases in a given layer
            final_similar_phrases = []
            for i in range(len(final_selected_phrases)):
                final_similar_phrases.append(generate_similar_phrases(final_selected_phrases[i], model, stopwords))

            with open('../output_data/tmp/selected_similar_phrases.json', 'w') as json_out:
                json.dump(final_similar_phrases, json_out, indent = 4)

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
    return sorted_list[-(TOP_K_SELECTED + BUFFER):]

def filter_stopwords(buffered_top_phrases_layer, stopwords):
    '''
    Remove any phrases that are defined as stopwords from the layer
    Return the filtered list with the buffer removed
    '''
    # Check the buffered amount of selected phrases against the provided stopwords
    removal_indices = []
    for i in range(len(buffered_top_phrases_layer)):
        if len(buffered_top_phrases_layer[i]) == 1:
            # Single word list so remove the entire list if stopword
            for word in stopwords:
                if buffered_top_phrases_layer[i][0] == word[:-1]:
                    removal_indices.append(i)
                    print('The selected phrase "' + word[:-1] + '" was indetified as a stopword and removed.')
                    break
        else:
            # Either remove the entire list or remove an entry from the list
            length = len(buffered_top_phrases_layer[i])
            sub_removal_indices = []
            for j in range(length):
                for word in stopwords:
                    if buffered_top_phrases_layer[i][j] == word[:-1]:
                        sub_removal_indices.append(j)
                        print('The selected phrase "' + word[:-1] + '" was indetified as a stopword and removed.')
                        break
            if len(sub_removal_indices) == length:
                removal_indices.append(i)
            else:
                sub_removal_indices.reverse()
                for j in sub_removal_indices:
                    del buffered_top_phrases_layer[i][j]

    # Delete the identified stopwords from the list while ensuring at least K are returned
    removal_indices.reverse()
    for i in removal_indices:
        del buffered_top_phrases_layer[i]
    return buffered_top_phrases_layer[-TOP_K_SELECTED:]

def unstem_phrases(buffered_top_phrases_layer, unstemmed_layer):
    '''
    Replace the stem with its original phrases
    Return a list of the original phrases
    '''
    # Extract the phrases into a list
    phrase_list = []
    for i in range(len(buffered_top_phrases_layer)):
        phrase_list.append(buffered_top_phrases_layer[i]['phrase'])

    original_phrases = []
    for stem in phrase_list:
        original_dict = list(filter(lambda temp_pair: temp_pair['stem'] == stem, unstemmed_layer))
        original_phrases.append(original_dict[0]['phrase'])
    return original_phrases

def phrase_formatter(layer_of_abstracts):
    '''
    Remove the <phrase> tags and replace all of the spaces with underscores of multi-word tagged phrases in the abstracts
    Return the formatted abstracts
    '''
    formatted_abstracts = []
    for abstract in layer_of_abstracts:
        phrase_list = []
        soup = BeautifulSoup(abstract, 'lxml')
        for phrase in soup.find_all(['phrase']):
            phrase_list.append(phrase.get_text())
        formatted_phrase_list = []
        for phrase in phrase_list:
            formatted_phrase_list.append(phrase.replace(' ', '_'))
        for i in range(len(phrase_list)):
            abstract = abstract.replace('<phrase>' + phrase_list[i] + '</phrase>', formatted_phrase_list[i])
        formatted_abstracts.append(abstract.lower())
    return formatted_abstracts

def sentence_splitter(layer_of_abstracts):
    '''
    Create a list of sentences from the abstracts
    Return the list of sentences
    '''
    layer_of_sentences = []
    for abstract in layer_of_abstracts:
        layer_of_sentences += re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', abstract)
    return layer_of_sentences

def generate_similar_phrases(layer, model, stopwords):
    '''
    Generate the most similar words of each of the selected phrases
    Return a list of dictionaries containing the phrase and the similar phrases
    '''
    similar_phrase_layer = []
    additional_stopwords = ['(', ')', '\'', '\'\'', '.', ',']
    for phrase_list in layer:
        similar_phrase_list = []
        for phrase in phrase_list:
            try:
                for similar_phrase_tuple in model.wv.most_similar(phrase.replace(' ', '_')):
                    similar_phrase_list.append(similar_phrase_tuple[0])
            except KeyError as e:
                print(e)
        # Filter stopwords from the similar_phrase_list
        stopword_indexes = []
        for i in range(len(similar_phrase_list)):
            for word in stopwords:
                if similar_phrase_list[i] == word[:-1] or similar_phrase_list[i] in additional_stopwords:
                    stopword_indexes.append(i)
                    break
        stopword_indexes.reverse()
        for i in stopword_indexes:
            del similar_phrase_list[i]
        # Return the inserted _s back to ' 's
        final_similar_phrases = []
        for phrase in similar_phrase_list:
            final_similar_phrases.append(phrase.replace('_', ' '))
        # Add the phrase dictionary to the layer list
        similar_phrase_layer.append({
            'phrase': phrase_list,
            'similar_phrases': final_similar_phrases
        })
    return similar_phrase_layer        

if __name__ == '__main__':
    main()