import pandas as pd
import numpy as np
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from bs4 import BeautifulSoup
import csv
import math
import scipy
from scipy.sparse import csr_matrix
import json
eps = 1e-8

def create_parsed_list_in_one_layer(doc):
    doc_parsed_list = []
    for i in range(len(doc)):
        tmpdoc = []
        #do it for each doc[i]
        soup = BeautifulSoup(doc[i], 'lxml')
        for p in soup.find_all(["phrase"]):
            tmpdoc.append(p.get_text())
        #save back to mother
        doc_parsed_list.append(tmpdoc)
    return doc_parsed_list

# # Function to compute tf-idf-ratio score
def union_set(doc_list):#1
    wordSet = set(doc_list[0])
    for i in range(1,len(doc_list)):
        wordSet=wordSet.union(set(doc_list[i]))
    return wordSet

def create_wordDict_list(doc_list,wordSet):  #depends on how many documents we have
    wordDict_list = []
    for i in range(len(doc_list)):
        wordDict_list.append(dict.fromkeys(wordSet,0))
    return wordDict_list

def createPd(wordDict_list):
    return pd.DataFrame(wordDict_list)

def computeIDF(docList):
    import math
    idfDict = {}
    N = len(docList)
    
    idfDict = dict.fromkeys(docList[0].keys(), 0)
    for doc in docList:
        for word, val in doc.items():
            if val > 0:
                idfDict[word] += 1
    
    for word, val in idfDict.items():
        idfDict[word] = math.log10(N / float(val))
        
    return idfDict

def computeTFIDF(tfBow, idfs):
    tfidf = {}
    for word, val in tfBow.items():
        tfidf[word] = val*idfs[word]
    return tfidf

def populate_word_dic(wordDict_list,doc_parsed_list):
    for i in range(len(doc_parsed_list)):
        for word in doc_parsed_list[i]:
            wordDict_list[i][word]+=1
    
def computeTF(wordDict, bow):
    tfDict = {}
    bowCount = len(bow)
    for word, count in wordDict.items():
        tfDict[word] = count/float(bowCount)
    return tfDict

def computetf(wordDict_list,doc_list):
    tf_list = []
    for i in range(len(doc_list)):
        tf_list.append(computeTF(wordDict_list[i],doc_list[i]))
    return tf_list

def computeTF_hypter(wordDict, bow):
    tfDict = {}
    bowCount = 0
    for i in range(len(bow)):
        bowCount += len(bow[i])
    #create a dic that record total number of occurance 
    for j in range(len(wordDict)):
        for word,count in wordDict[j].items():
            if word not in tfDict:
                tfDict[word] = count
            else:
                tfDict[word] = tfDict.get(word) + count
                
    for key in tfDict:
        tfDict[key] = tfDict[key]/bowCount
    return tfDict

def computetf_hyper(wordDict_list,doc_list):
    tf_list = []
#     for i in range(len(doc_list)):
#         tf_list.append(computeTF(wordDict_list,doc_list))
    single_list = computeTF_hypter(wordDict_list,doc_list)
    for _ in range(len(doc_list)):
        tf_list.append(single_list)
    return tf_list

def computeidf(wordDict_list):
    return computeIDF(wordDict_list)

def compute_tf_idf_list(tf_list,idfs):
    tfidf_list = []
    for i in range(len(tf_list)):
        tfidf_list.append(computeTFIDF(tf_list[i],idfs))
        
    return tfidf_list

def df_ifd_generator(doc_parsed_list_uni):
    wordSet = union_set(doc_parsed_list_uni)
    wordDict_list = create_wordDict_list(doc_parsed_list_uni,wordSet)
    populate_word_dic(wordDict_list,doc_parsed_list_uni)
    tflist = computetf_hyper(wordDict_list,doc_parsed_list_uni)
    idflist = computeidf(wordDict_list)
    tfidf_list = compute_tf_idf_list(tflist,idflist)
    return pd.DataFrame(tfidf_list),pd.DataFrame(tflist)

# # Create function to compute ratio
# # First create another df only contains tf for each layer

def compute_ratio_for_current_layer(tfidf_pd_list,tf_pd_list):
    #step1. choose a layer as target layer, set the rest layer as layers used to compute ratio
    #step2. loop through every phrase in target layer
        #2.1for current phrase
            #find the max tf of this phrase in other layer
                #if phrase not exist in other layer, ratio = A
                #else ratio = A/B, where B is max tf of this phrase from other layer
        #2.2create the scoore for current phrase in current layer
    #step3.return all result
    for i in range(len(tfidf_pd_list)):
        tfidflist_used_for_ratio = []
        tflist_used_for_ratio = []
        for j in range(len(tfidf_pd_list)):
            if j!=i:
                tfidflist_used_for_ratio.append(tfidf_pd_list[j])
                tflist_used_for_ratio.append(tf_pd_list[j])
        #other layer except for layer i has been found
        #proceed to step2.1
        #create a list contains all key in current layer
        key_list = tfidf_pd_list[i].keys()
        for loc in range(len(key_list)):
            #if phrase not exist in both other layers
            #create a index list that contains the index which layer has curretn loc
            index_list_contains_current_phrase = []
            for pos in range(len(tfidflist_used_for_ratio)):
                if key_list[loc] in tfidflist_used_for_ratio[pos]:
                    index_list_contains_current_phrase.append(pos)
            #if phrase  exist in other layers:
#             print('curretn key is ',key_list[loc], ' current index list is',index_list_contains_current_phrase )
        
            if len(index_list_contains_current_phrase) != 0:
                #find the max tf of this phrase
                tmpmax = 0
                for exist_pos in range(len(index_list_contains_current_phrase)):
                    cur_max = np.max(tflist_used_for_ratio[index_list_contains_current_phrase[exist_pos]][key_list[loc]].values)
                    if cur_max > tmpmax:
                        tmpmax = cur_max
#                 print('what is i', i, ' what is key', key_list[loc])
                #update current tfidf value
                tfidf_pd_list[i][key_list[loc]] = (tfidf_pd_list[i][key_list[loc]] +eps )/(tmpmax+eps)
            else:
                #no document contains phrase a in current layer
#                 print('hahah')
                tfidf_pd_list[i][key_list[loc]] = (tfidf_pd_list[i][key_list[loc]] +eps )/(0+eps)
    return tfidf_pd_list

def generate_top_k_pd(ratio_list):
    list_store_top_layer_record = []
    for i in range(len(ratio_list)):
        #find key list
        tmp_dic = {}
        key_list_new = ratio_list[i].keys()
        for j in range(len(key_list_new)):
            #find the max val for curretn key in current layer
            tmp_dic[key_list_new[j]] =  np.max(ratio_list[i][key_list_new[j]].values)
        list_store_top_layer_record.append(pd.Series(tmp_dic))
    return list_store_top_layer_record

# # Generate tf-idf pandas
with open('./output_data/tmp/meta_scraped_text.json', 'r') as lengths_file:
    lengths = json.load(lengths_file)
with open('./output_data/tmp/segmentation.txt', 'r') as scraped_input_file:
    lines = scraped_input_file.readlines()

doc_parsed_list1 = create_parsed_list_in_one_layer(lines[0:lengths[0]])
doc_parsed_list2 = create_parsed_list_in_one_layer(lines[lengths[0]:lengths[0] + lengths[1]])
doc_parsed_list3 = create_parsed_list_in_one_layer(lines[lengths[0] + lengths[1]:])

pd1,tflist1_pd= df_ifd_generator(doc_parsed_list1)
pd2,tflist2_pd= df_ifd_generator(doc_parsed_list2)
pd3,tflist3_pd= df_ifd_generator(doc_parsed_list3)

tfidf_pd_list = []
tfidf_pd_list.append(pd1)
tfidf_pd_list.append(pd2)
tfidf_pd_list.append(pd3)
tf_pd_list = []
tf_pd_list.append(tflist1_pd)
tf_pd_list.append(tflist2_pd)
tf_pd_list.append(tflist3_pd)

ratio_list = compute_ratio_for_current_layer(tfidf_pd_list,tf_pd_list)

final = generate_top_k_pd(ratio_list)

# # find top k for layer1
# # Save results to json file
top_k_selected = 10
a = final[0].nlargest(top_k_selected)
b = final[1].nlargest(top_k_selected)
c = final[2].nlargest(top_k_selected)

keys = []
temp_keys = []
temp = a.keys()
for i in range(len(temp)):
    temp_keys.append(temp[i])
keys.append(temp_keys)
temp_keys = []
temp = b.keys()
for i in range(len(temp)):
    temp_keys.append(temp[i])
keys.append(temp_keys)
temp_keys = []
temp = c.keys()
for i in range(len(temp)):
    temp_keys.append(temp[i])
keys.append(temp_keys)

with open('./output_data/tmp/selected_phrases.json', 'w') as json_out:
    json.dump(keys, json_out, indent = 4)