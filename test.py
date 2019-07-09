import json
from collections import Counter
from nltk.tokenize import word_tokenize
import pandas as pd
from gensim import models
from bs4 import BeautifulSoup
import re

# df = pd.read_csv('./input_data/jokes.csv')

# x = df['Question'].values.tolist()
# y = df['Answer'].values.tolist()

# corpus = x + y
# # print(corpus) this is literally just two lists of strings concatenated together to make a biggerl ist of strings and nothing more

# # print(nltk.word_tokenize('kevin'))
# tok_corp = [word_tokenize(sent) for sent in corpus]
# # print(tok_corp)
# # size is dimensionality of the word vectors
# # workers is the number of threads
# # min_count Ignores all words with total frequency lower than this.
# model = models.Word2Vec(tok_corp, min_count = 1, size = 32, workers = 8)
# # print(model)
# print('yo')
# print(model.most_similar('joke'))

#extract phrase from phrase tags
#replace space in phrase with underscore
#replace all <phrase>phrase</phrase> with _phrase_

def phrase_reformater(layer_of_sentences):
    new_sentence_lsit = []
    for sentence in layer_of_sentences:
        phrase_list = []
        soup = BeautifulSoup(sentence, 'lxml')
        for phrase in soup.find_all(['phrase']):
            phrase_list.append(phrase.get_text())
        new_phrase_list = []
        for phrase in phrase_list:
            new_phrase_list.append(phrase.replace(' ', '_'))
        for i in range(len(phrase_list)):
            sentence = sentence.replace('<phrase>' + phrase_list[i] + '</phrase>', new_phrase_list[i])
        new_sentence_lsit.append(sentence)
    # print(new_sentence_lsit)
    return new_sentence_lsit #this is a list of abstracts

def splitter(layer_abstracts):
    layer = []
    for abstract in layer_abstracts:
        temp_list = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', abstract)
        layer += temp_list
    return layer

def maker(layer):
    tok_corp = [word_tokenize(sentence) for sentence in layer]
    model = models.Word2Vec(tok_corp, min_count = 1, size = 32, workers = 8)
    return model

with open('./output_data/tmp/segmentation.txt', 'r') as segmentation_file:
    lines = segmentation_file.readlines()
with open('./output_data/tmp/meta_scraped_text.json', 'r') as lengths_file:
    lengths = json.load(lengths_file)

# format phrases
total = 0
model_to_train = []
for length in lengths:
    model_to_train.append(phrase_reformater(lines[total:total + length]))
    total += length
# print(model_to_train)

# combine abstracts in a layer and split them into a list of sentences instead
layers_sentences = []
for layer in model_to_train:
    layers_sentences.append(splitter(layer))
# print(layers_sentences)

model_stuff = []
for layer in layers_sentences:
    model_stuff.append(maker(layer))

# print(model_stuff[0])
# print(model_stuff[0].most_similar('golf'))
# print(model_stuff[0]['golf'])
# print(model_stuff[0].similar_by_word('golf'))
# print(model_stuff[0].predict_output_word('golf'))
# print(model_stuff[0].doesnt_match(['golf', 'golfer', 'lightweight', 'band', 'mouth', 'play', 'upper', 'water', 'easy_access', 'weather']))
print(model_stuff[0].similarity('golf', 'the'))

# can check phrase similarity before they are filtered and if they are above a certain threshold, throw out that phrase?