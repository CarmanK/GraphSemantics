#!/usr/bin/env python
# coding: utf-8

# In[39]:


import pandas as pd
import numpy as np
import csv
import math
from bs4 import BeautifulSoup
from gensim.summarization.bm25 import get_bm25_weights
from rank_bm25 import BM25Okapi
import json
from termcolor import colored


# # Read the json file from kevin

# In[40]:


with open('./output_data/tmp/article_pool.json', 'r') as input_file:
    phrase_list = json.load(input_file)


# In[41]:


data_df_layer_1 = pd.DataFrame(phrase_list[2])


# In[42]:


#get the layer number
layer_num = len(phrase_list)


# # Find the pair of unique phrase in layer1

# In[43]:


unique_phrase_list = np.unique(data_df_layer_1['phrase'].values)


# In[44]:


unique_phrase_list


# # Find the unique phrase in layer 1

# In[45]:


p_list = list(pd.read_json('./output_data/tmp/selected_phrases.json',typ='series')[0])


# In[46]:


p_list


# # Create list of list(unique phrase) for current pair

# In[47]:


#loop throught every pair of phrase
list_of_phrase_list = []
for i in range(len(unique_phrase_list)):
    tmplist =[]
    for j in range(len(p_list)):
        if p_list[j] in unique_phrase_list[i]:
            tmplist.append(p_list[j])
    list_of_phrase_list.append(tmplist)


# In[48]:


def create_sentece_list(unique_phrase_list):
    list_of_phrase_list = []
    for i in range(len(unique_phrase_list)):
        tmplist =[]
        for j in range(len(p_list)):
            if p_list[j] in unique_phrase_list[i]:
                tmplist.append(p_list[j])
        list_of_phrase_list.append(tmplist)
    return list_of_phrase_list


# # attention: Every sentence in the articles from the pool is a candidate sentence for the final summary.
# # step: compute a BM25 score for every candidate sentence
# 
# # to compute BM25
# # 1. find all sentence in current layer(done)
# # 2. index all sentence(done)
# # 3. compute score for all current sentence
# # 4. question here-> should we use the sentence with highest score 
# # to cover the phrase? or to cover pair of phrase?
# # If so, after phrase been recoverd, tag the sentence been used,
# # recompute the BM25 in unused sentence pool
# # and iterate all sentece until all phrase been coverd

# In[49]:


#create the article pool now
article_list = data_df_layer_1['article'].values
#for each article, find all sentence
article_list[0]
sentence_dic = {}
list_sentence = []
s_count = 0 #sentence index
for i in range(len(article_list)):
    #for every sentence, if not in sentence_list, push sentence in list
    tmp_sentence_list = article_list[i].split(".")    
    for j in range(len(tmp_sentence_list)):
#         if tmp_sentence_list[j] not in article_list:
        sentence_dic[s_count] = tmp_sentence_list[j]
        list_sentence.append(tmp_sentence_list[j])        
        s_count +=1
list_sentence = np.unique(list_sentence)


# In[50]:


def create_sentence_pool(data_df_layer_1):
    article_list = data_df_layer_1['article'].values
    #for each article, find all sentence
    article_list[0]
    sentence_dic = {}
    list_sentence = []
    s_count = 0 #sentence index
    for i in range(len(article_list)):
        #for every sentence, if not in sentence_list, push sentence in list
        tmp_sentence_list = article_list[i].split(".")
        for j in range(len(tmp_sentence_list)):
#          if tmp_sentence_list[j] not in article_list:
            sentence_dic[s_count] = tmp_sentence_list[j]
            list_sentence.append(tmp_sentence_list[j])
            s_count +=1
    return np.unique(list_sentence)


# In[51]:


def BM25_score(sentence_list,unique_phrase_list,p_list):
    #at each iteration
    #find the sentence that could lead to the highest bm25
        #1.for every pair of phrase, find the max score of that sentence, save that score and the respective sentence,
        #2.pick the highest score, also recover that sentence
        #3.find how many phrase this sentece been touched, tag those phrase, pop those phrase out of phrase list
        #4.if pair of phrase that lead to highest score contains all some at least two of phrase that been poped out,
        #5.pop out that phrase pair in pair list
        #6.finsihed current iteration
        #7.check whether the lenght of phrass list becomes 0 or num of iteration hit max
        #8.if either happens, exit the problem, return the sentence list, and the touched phrase list
        
    
    answer_sentence_list = []
    touched_phrase_list = []
    count = 0
    while len(p_list) > 0 and len(touched_phrase_list) < len(p_list):
        #step1
        #create a data structure to save score for current query(as pair of phrase)
        #in the future, implement the max-heap ds here O(nlogn) push, O(1) peek
        score_list_current_iter = []
        sentence_idx_list = []
        cur_pair_phrase_dic = {}
        for i in range(len(unique_phrase_list)):
            #compute bm25 score use current phrase pair as query
            bm25 = BM25Okapi(sentence_list) #create class of bm25
            doc_scores = bm25.get_scores(unique_phrase_list[i])
            sentence_loc = np.argmax(doc_scores)  #the index num of max-score sentence in the sen_list
            sentence_score = np.max(doc_scores)   #the max score over all score of sentence for current query
            score_list_current_iter.append(sentence_score)
            sentence_idx_list.append(sentence_loc)
            if sentence_score not in cur_pair_phrase_dic:
                cur_pair_phrase_dic[sentence_score] = i
        #step2
        highest_score_index = np.argmax(score_list_current_iter)
        high_sen = sentence_list[sentence_idx_list[highest_score_index]] 
        answer_sentence_list.append(high_sen)
        #step three
        cur_touched_phrase = []  #record how many phrase been touched by this sentence
#         print('current lengh of p_list is', len(p_list))
        list_deleted = []
        for pos in range(len(p_list)):
#             print('current pos is', pos)
#             print('what is that ', p_list[pos])
            if p_list[pos] in high_sen:
                if p_list[pos] not in cur_touched_phrase:
                    cur_touched_phrase.append(p_list[pos])
#                 p_list.remove(p_list[pos])
                #remove phrase list
        #<wait>
#         for i in range(len(cur_touched_phrase)):
#             if cur_touched_phrase[i] in p_list:
#                 p_list.remove(cur_touched_phrase[i])
        #<wait>
#         print('current sentence is', sentence_list[highest_score_index])
#         print('len of unique pair  list', len(unique_phrase_list))
        print('lengh of touched phrase', len(cur_touched_phrase))
#         print('current count is', count)
#         print('lengh of sentence list', len(sentence_list))

#         #if the current pair of phrase that lead to this sentence which has max score contains two phrase in cur_touched_phrase
#         #pop this pair of phrase out of pair of phrase list
#         #return the pair of phrase by useing dic
        curpair = unique_phrase_list[cur_pair_phrase_dic[np.max(score_list_current_iter)]] 
#         #count how many phrase in cur_touched_phrase 
        count_now = 0
        for loc in range(len(cur_touched_phrase)):
            if cur_touched_phrase[loc] in curpair:
                count_now+=1
        if count_now>=2 and curpair in unique_phrase_list:
#             print('hahahahahahhaa six six six')
            unique_phrase_list.remove(curpair)
        count +=1
        #remove phrase list
        #unique_phrase_list.remove(curpair)
        #remove sentence
        sentence_list.remove(high_sen)
        
        #add cur touched list to total touched list
        for inx in range(len(cur_touched_phrase)):
            if cur_touched_phrase[inx] not in touched_phrase_list:
                touched_phrase_list.append(cur_touched_phrase[inx])
        print('now total touched length', len(touched_phrase_list))
        #create a pair phrase function based on the cur_touched_phrase_process
        tmp_phrase_pair = []
        for p in range(len(cur_touched_phrase)):
            for q in range(p,len(cur_touched_phrase)):
                if cur_touched_phrase[p] != cur_touched_phrase[q]:
                    tmp_phrase_pair.append([cur_touched_phrase[p],cur_touched_phrase[q]])
        #iter thorught unique_phrase_list if pair is exist in touched list, dequeue them
        
        deletelist = []
#         print('tmo coutched list is', len(tmp_phrase_pair))
#         print('tmp phrase pari look like ', tmp_phrase_pair)
        for p2 in range(len(tmp_phrase_pair)):
            for q2 in range(len(unique_phrase_list)):
                if tmp_phrase_pair[p2][0] in unique_phrase_list[q2] and tmp_phrase_pair[p2][1] in unique_phrase_list[q2]:
                    if unique_phrase_list[q2] not in deletelist:
                        deletelist.append(unique_phrase_list[q2])
        
#         print('look of deletelist, ', deletelist)
#         print('len of delete list', len(deletelist))
        for p3 in range(len(deletelist)):
            if deletelist[p3] in unique_phrase_list:
                unique_phrase_list.remove(deletelist[p3])
#         print('len of unique list is', len(unique_phrase_list))
        print('num of iteration now is', count)

    return answer_sentence_list


# In[52]:


def set_cover(sentence_list,unique_phrase_list,p_list):
    #at each iteration
        #find the sentence that cover most number of unvisted phrase
        #mark those phrase as visited (pop)
        #mark the sentence as visited (pop)
    answer_sentence_list = []
    touch_count_dic = []
    count = 0
    while len(p_list) > 0:
        #create a data structure to save how many unvisited phrase the current sentence touched
        touch_count_dic = {} #key as num of phrase touched, value is a list of index of sentence
        global_max_count = 0
        for i in range(len(sentence_list)):
            #compute num of touched
            tmpcount = 0
            for j in range(len(p_list)):
                if p_list[j] in sentence_list[i]:
                    tmpcount+=1
            if tmpcount > global_max_count:
                global_max_count = tmpcount
            # save current result in dic
            if tmpcount in touch_count_dic:
                #return the list
                curlist = touch_count_dic.get(tmpcount)
                curlist.append(i)
            else:
                tmplist = []
                tmplist.append(i)
                touch_count_dic[tmpcount] = tmplist
        #use the global max count to return lit of index of sentence that lead to the max current count
        
        list_of_max_index_sentence = touch_count_dic[global_max_count]
        #pick the first one
        selected_max_sentence_index = list_of_max_index_sentence[0]
        selected_max_sentence = sentence_list[selected_max_sentence_index]
        #set cover
        visited_list = []
#         print('what is sentence now', selected_max_sentence)
        
        for loc in range(len(p_list)):
            if p_list[loc] in selected_max_sentence and p_list[loc] not in visited_list:
                visited_list.append(p_list[loc])
        #delete all visited list
        print('!!!! visted list is', len(visited_list))
#         print('what is sentence now', selected_max_sentence)
        for pos2 in range(len(visited_list)):
            p_list.remove(visited_list[pos2])
        answer_sentence_list.append(selected_max_sentence)
        #remove the current sentencn
        sentence_list.pop(selected_max_sentence_index)
#         print('length of sentence list is', len(sentence_list))
#         print('len of remainng list', p_list)
    return answer_sentence_list


# In[53]:


def annotating_function(answer,p_list): #only mark the first occurance of a phrase exist in sentence
    #iter through every answer
    for i in range(len(answer)):
        for j in range(len(p_list)):
            if p_list[j] in answer[i]:
                #find the starting index
                start = answer[i].find(p_list[j])
                end = start + len(p_list[j])
                answer[i] = answer[i][0:start] + colored(p_list[j],'red') + answer[i][end:]
    for i in range(len(answer)):
        print('index :', i, '', answer[i] +'\n')


# In[57]:


def main_func():
    with open('./output_data/tmp/article_pool.json', 'r') as input_file:
        phrase_list = json.load(input_file)
    layer_num = len(phrase_list)  #how many layer
    for i in range(layer_num):
        data_df_layer_1 = pd.DataFrame(phrase_list[i])
        unique_phrase_list = np.unique(data_df_layer_1['phrase'].values)
        p_list = list(pd.read_json('./output_data/tmp/selected_phrases.json',typ='series')[i])
#         list_of_phrase_list =  create_sentece_list(unique_phrase_list)
        list_sentence = create_sentence_pool(data_df_layer_1)
        #run
        answer = set_cover(list(list_sentence),list(unique_phrase_list),p_list.copy())
        #save it to json file
        path = "./output_data/out_2d_layer_" + str(i)

        with open(path, 'w') as outfile:
            json.dump(answer, outfile)
            
        print('current layer is: ',i )
        annotating_function(answer.copy(),p_list)


# In[58]:


main_func()


# In[ ]:





# In[ ]:



