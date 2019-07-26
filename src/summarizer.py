#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
# import os
# try:
# 	os.chdir(os.path.join(os.getcwd(), 'jupter'))
# 	print(os.getcwd())
# except:
# 	pass

# Haodong wrote this file as you can easily tell it is not my style code...

#%%
import pandas as pd
import numpy as np
import csv
import math
from bs4 import BeautifulSoup
from gensim.summarization.bm25 import get_bm25_weights
from rank_bm25 import BM25Okapi
import json
from termcolor import colored
import re
import itertools
from functools import reduce

#%% [markdown]
# # Read the json file from kevin



#%%
def generate_list_of_phrase(p_list):
    ans = []
    for i in range(len(p_list)):
        if p_list[i]['phrase'] not in ans:
            ans.append(p_list[i]['phrase'])
    return ans

def create_sentece_list(unique_phrase_list):
    list_of_phrase_list = []
    for i in range(len(unique_phrase_list)):
        tmplist =[]
        for j in range(len(p_list)):
            if p_list[j] in unique_phrase_list[i]:
                tmplist.append(p_list[j])
        list_of_phrase_list.append(tmplist)
    return list_of_phrase_list

def p_list_fixed_points(layer_num):
    ans = []
    for i in range(layer_num):
        p_list = list(pd.read_json('../output_data/tmp/selected_similar_phrases.json',typ='series')[i])
        for j in range(len(p_list)):
            if p_list[j] not in ans:
                ans.append(p_list[j])
    return ans

#%% [markdown]
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

# #%%
# #create the article pool now
# article_list = data_df_layer_1['article'].values
# #for each article, find all sentence
# article_list[0]
# sentence_dic = {}
# list_sentence = []
# s_count = 0 #sentence index
# for i in range(len(article_list)):
#     #for every sentence, if not in sentence_list, push sentence in list
#     tmp_sentence_list = article_list[i].split(".")
#     for j in range(len(tmp_sentence_list)):
# #         if tmp_sentence_list[j] not in article_list:
#         sentence_dic[s_count] = tmp_sentence_list[j]
#         list_sentence.append(tmp_sentence_list[j])
#         s_count +=1
# list_sentence = np.unique(list_sentence)


#%%
def create_sentence_pool(article_list):
#     article_list = data_df_layer_1['article'].values
    #for each article, find all sentence
    article_list[0]
    sentence_dic = {}
    list_sentence = []
    s_count = 0 #sentence index
    for i in range(len(article_list)):
        #for every sentence, if not in sentence_list, push sentence in list
        tmp_sentence_list = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', article_list[i])
        for j in range(len(tmp_sentence_list)):
#          if tmp_sentence_list[j] not in article_list:
            sentence_dic[s_count] = tmp_sentence_list[j]
            list_sentence.append(tmp_sentence_list[j])
            s_count +=1
    return np.unique(list_sentence)

#%%
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
        # print('lengh of touched phrase', len(cur_touched_phrase))
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
        # print('now total touched length', len(touched_phrase_list))
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
        # print('num of iteration now is', count)

    return answer_sentence_list


#%%
#%%

def contains_word(s, w):
    return (' ' + w + ' ') in (' ' + s + ' ')


def set_cover(sentence_list,unique_phrase_list,p_list):
    #at each iteration
        #find the sentence that cover most number of unvisted phrase
        #mark those phrase as visited (pop)
        #mark the sentence as visited (pop)
    answer_sentence_list = []
    touch_count_dic = []
    count = 0
    isempty = False
    while len(p_list) > 0 and isempty==False:
        #create a data structure to save how many unvisited phrase the current sentence touched
        touch_count_dic = {} #key as num of phrase touched, value is a list of index of sentence
        global_max_count = 0
        for i in range(len(sentence_list)):
            #compute num of touched
            tmpcount = 0
            for j in range(len(p_list)):
#                 if 1 in [c in sentence_list[i] for c in p_list[j]]:
                if 1 in [c in sentence_list[i].lower() for c in p_list[j]['phrase']]:
#                 if p_list[j] in sentence_list[i]:
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
#             if 1 in [c in selected_max_sentence for c in p_list[loc]] and p_list[loc] not in visited_list:
            if 1 in [c in selected_max_sentence.lower() for c in p_list[loc]['phrase']] and p_list[loc]['phrase'] not in visited_list:
#             if p_list[loc] in selected_max_sentence and p_list[loc] not in visited_list:
                visited_list.append(p_list[loc]['phrase'])

#             if 1 in [contains_word(selected_max_sentence,c) for c in p_list[loc]['similar_phrases']] and p_list[loc]['similar_phrases'] not in visited_list:
#                 visited_list.append(p_list[loc]['similar_phrases'])


        #delete all visited list
        # print('!!!! visted list is', len(visited_list))
        # print('cur list is ', p_list)
#         print('waht is visited list', visited_list)
#         print('what is p_list',p_list)
#         print('what is sentence now', selected_max_sentence)
        if len(visited_list) == 0:
            isempty=True
            break

        newplist = ge_phrase_list_in_setcover(p_list)
        newpp_list = []
        while len(visited_list) > 0:
            curitem = visited_list[0]
            newplist = ge_phrase_list_in_setcover(p_list)
            curindex = newplist.index(curitem)
    #             p_list.remove(visited_list[pos2])
            # print('len of visited list', len(visited_list))
            if curitem not in newplist:
                curindex = -1
            if curindex != -1:
                del p_list[curindex]
                visited_list.remove(curitem)
            else:
                visited_list.remove(curitem)
        #delete one by one

        #<--------part need to be done one by one ....>

        # print('so this is it', len(p_list))

        # print('what is selectedf sentence', selected_max_sentence)
        answer_sentence_list.append(selected_max_sentence)
        #remove the current sentencn
        sentence_list.pop(selected_max_sentence_index)
#         print('length of sentence list is', len(sentence_list))
#         print('len of remainng list', p_list)
    return answer_sentence_list

def ven_diagram(list_sentence,unique_phrase_list,p_list):
    #generate the list of list
    list_of_list_com = []
    counter = len(p_list)
    while counter > 0:
        list_of_list_com.append(list(itertools.combinations(p_list,counter)))
        counter-=1

    #venn cover
    len_p_list = len(p_list)#len of p_list
    #find the sentence that matches current cover
    ans = []
    for i in range(len(list_of_list_com)):
        for j in range(len(list_of_list_com[i])):
            #find the phrase list that not in com_list
            cur_list = list(list_of_list_com[i][j])
            not_in_list = []
            for pos in range(len(p_list)):
                if p_list[pos] not in cur_list:
                    not_in_list.append(p_list[pos])

            #find the sentence that cover all phrase in list_of_list_com[i][j] and not covered in not_in_list
            for p in  range(len(list_sentence)):
                flag_good = True
                flag_good_filter = True
                for q in range(len(cur_list)):
                    if cur_list[q] not in list_sentence[p]:
                        flag_good = False
                        break
                for g in range(len(not_in_list)):
                    if not_in_list[g] in list_sentence[p]:
                        flag_good_filter = False
                        break
                #pass all exam
                #push current setence to result
                if flag_good==True and flag_good_filter==True and list_sentence[p] not in ans:
                    ans.append(list_sentence[p])

        print('combination:',len_p_list,' choose ',len_p_list - i,' current lengh of ans is', len(ans))

    return ans




#%%
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
        print(str(i + 1), ': ', answer[i] +'\n')


def new_annot(answer,p_list,sim_list):
    for i in range(len(answer)):
        for j in range(len(p_list[0])):
            #first check if that exist
            if 1 in [contains_word(answer[i],c) for c in p_list[0][j]]:
                #find the index
                index = np.argmax([c in answer[i] for c in p_list[0][j]])
#             if p_list[0][j] in answer[i]:
                #find the starting index
                start = answer[i].find(p_list[0][j][index])
                end = start + len(p_list[0][j][index])
                answer[i] = answer[i][0:start] + colored(p_list[0][j][index],'red') + answer[i][end:]

            if 1 in [contains_word(answer[i],c) for c in sim_list[0][j]]:
                #find the index
                index = np.argmax([c in answer[i] for c in sim_list[0][j]])
#             if p_list[0][j] in answer[i]:
                #find the starting index
                start = answer[i].find(sim_list[0][j][index])
                end = start + len(sim_list[0][j][index])
                answer[i] = answer[i][0:start] + colored(sim_list[0][j][index],'green') + answer[i][end:]


        if len(p_list) >= 2:
            for j in range(len(p_list[1])):
                if 1 in [contains_word(answer[i],c) for c in p_list[1][j]]:
                    #find the index
                    index = np.argmax([c in answer[i] for c in p_list[1][j]])
    #             if p_list[0][j] in answer[i]:
                    #find the starting index
                    start = answer[i].find(p_list[1][j][index])
                    end = start + len(p_list[1][j][index])
                    answer[i] = answer[i][0:start] + colored(p_list[1][j][index],'green') + answer[i][end:]


        if len(p_list) >=3:
            for j in range(len(p_list[2])):
                if 1 in [contains_word(answer[i],c) for c in p_list[2][j]]:
                    #find the index
                    index = np.argmax([c in answer[i] for c in p_list[2][j]])
    #             if p_list[0][j] in answer[i]:
                    #find the starting index
                    start = answer[i].find(p_list[2][j][index])
                    end = start + len(p_list[2][j][index])
                    answer[i] = answer[i][0:start] + colored(p_list[2][j][index],'blue') + answer[i][end:]


    for i in range(len(answer)):
        print(str(i + 1), ': ', answer[i] +'\n')


#scoring system
 # of phrases covered
 # of pairs of phrases covered
 # of layers covered




#scoring system
 # of phrases covered
 # of pairs of phrases covered
 # of layers covered

def filter_sentence(full_output,list_phrase,list_sim_phrase):
    final_ans = []
    #save sentence that beencoved from multip layer phrase and sentence that covered by at least 3 phrase in
    for i in range(len(full_output)):
        #iter through every sentence
        flag_list = [0]*len(list_phrase)
        for j in range(len(list_phrase)):
            #at current
            for pos in range(len(list_phrase[j])):
                if 1 in [c in full_output[i] for c in list_phrase[j][pos]]:
                #if list_phrase[j][pos] in full_output[i]:
                    flag_list[j] = 1
                    break
        if flag_list.count(1) >=2:

            if full_output[i] not in final_ans:
                final_ans.append(full_output[i])

        count_list =[0]*len(list_phrase)
        for j2 in range(len(list_phrase)):
            counter = 0
            for pos2 in range(len(list_phrase[j])):
                if 1 in [c in full_output[i] for c in list_phrase[j2][pos2]]:
                #if list_phrase[j2][pos2] in full_output[i]:
                    counter+=1
            count_list[j2] = counter

#         print('what is count_list', count_list)
        if np.max(count_list) >=2:
            if full_output[i] not in final_ans:
                final_ans.append(full_output[i])

        sim_count_list = [0] * len(list_sim_phrase)
        for j3 in range(len(list_sim_phrase)):
            counter = 0
            for pos3 in range(len(list_sim_phrase[j])):
                if 1 in [c in full_output[i] for c in list_sim_phrase[j3][pos3]]:
                    counter+=1
            sim_count_list[j3] = counter

        if np.max(sim_count_list) >= 3:
            print('sentence added to final sentence list based on similar phrase list if not added before ')
            if full_output[i] not in final_ans:
                final_ans.append(full_output[i])


    return final_ans
#%%
def ge_phrase_list_in_setcover(p_list):
    ans = []
    for i in range(len(p_list)):
        ans.append(p_list[i]['phrase'])
    return ans

def ge_similar_phrase_list_in_setcover(p_list):
    ans = []
    for i in range(len(p_list)):
        ans.append(p_list[i]['similar_phrases'])
    return ans

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

#%%
def main_func_new():
    with open('../output_data/tmp/abstracts.txt', 'r') as scraped_file:
            lines = scraped_file.readlines()
    # with open('./output_data/tmp/meta_scraped_text.json', 'r') as lengths_file:
    #         lengths = json.load(lengths_file)
    lengths = [len(lines)] # Temporary fix

    # Phrase Selection
    # Create a list of all of the parsed phrases for all of the layers
    total = 0
    layer_list = []
    for length in lengths:
        layer_list.append(lines)
        # layer_list.append(lines[total:total + length])
        # total += length

#     with open('./output_data/tmp/article_pool.json', 'r') as input_file:
#         phrase_list = json.load(input_file)
    layer_num = len(layer_list)  #how many layer
    # print('how many layer', layer_num)
    full_output = []
    #<change on 07032019>
    list_phrase = []
    allsentence = []
    list_sim_phrase = []
    unique_phrase_list = []
    #<change on 07032019>
    for i in range(layer_num):
#         data_df_layer_1 = pd.DataFrame(phrase_list[i])
#         unique_phrase_list = np.unique(data_df_layer_1['phrase'].values)
        #p_list = list(pd.read_json('./output_data/tmp/selected_phrases.json',typ='series')[i])
#         list_of_phrase_list =  create_sentece_list(unique_phrase_list)
        p_list = p_list_fixed_points(layer_num)
        #<change on 07032019 >
        list_phrase.append(generate_list_of_phrase(list(pd.read_json('../output_data/tmp/selected_similar_phrases.json',typ='series')[i])))
        #<change on 07032019 >
        list_sentence = create_sentence_pool(layer_list[i])
        #run

        list_sim_phrase.append(ge_similar_phrase_list_in_setcover(list(pd.read_json('../output_data/tmp/selected_similar_phrases.json',typ='series')[i])))

        answer = set_cover(list(list_sentence),list(unique_phrase_list),p_list.copy())
        full_output.append(answer)
        #change 07032019
        allsentence += answer
        #change 07032019
        # print('current layer is: ',i )
        #annotating_function(answer.copy(),p_list)
        # print('length of current p_list ', len(p_list))

    #<------change on 0703/2019------------->
    #filter the selected sentence



    #<------change on 0703/2019------------->
#     with open('./output_data/summaries.json', 'w') as outfile:
#             json.dump(full_output, outfile, indent = 4)
    # print('len of sentence', len(allsentence))
    # a =  filter_sentence(allsentence,list_phrase,list_sim_phrase)
    with open('../output_data/summaries.json', 'w') as outfile:
        json.dump(allsentence, outfile, indent = 4)

    new_annot(allsentence,list_phrase,list_sim_phrase)



main_func_new()
#%%



#%%



#%%
