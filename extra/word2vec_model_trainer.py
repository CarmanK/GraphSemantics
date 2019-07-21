import os
from nltk.tokenize import word_tokenize
from gensim import models
from bs4 import BeautifulSoup
import re

MODEL = 'Patents' # The directory that contains the trained word2vec model

def main():
    with open('./output_data/tmp/training_segmentation.txt', 'r') as segmentation_file:
        lines = segmentation_file.readlines()

    # Create a list of layers from training_segmentation.txt but remove the <phrase> tags and replace all of the spaces with underscores of multi-word tagged phrases
    formatted_abstracts = []
    formatted_abstracts.append(phrase_formatter(lines))

    # Split the abstracts in a given layer into sentences and join them to one list per layer
    layers_of_sentences = []
    for layer in formatted_abstracts:
        layers_of_sentences.append(sentence_splitter(layer))

    # Train the word2vec model
    model_list = []
    for layer in layers_of_sentences:
        model_list.append(model_trainer(layer))

    # Save the model
    path = 'output_data/models/' + MODEL
    if not os.path.exists('output_data/models'):
        os.mkdir('output_data/models')
    model_list[0].save(path + '.model')

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

def model_trainer(layer):
    '''
    Train a word2vec model on a given layer
    Return the trained model
    '''
    tokenized_corpus = [word_tokenize(sentence) for sentence in layer]
    return models.Word2Vec(tokenized_corpus, min_count = 1, size = 100, workers = 8)

if __name__ == '__main__':
    main()