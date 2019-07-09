# -*- coding: utf-8 -*-
import datetime as dt
import re

"""
set string { ... } to list 
"""
def to_list(text):
    return text.replace('{','').replace('}','').split(',')

"""
convert year, month, day 
"""
def to_time(text):
    res = ''
    if len(text.split(' ')) > 1:
        res = text.split(' ')[0]
    elif len(text.split('T')) > 1:
        res = text.split('T')[0]
        
    return dt.datetime.strptime(res, '%Y-%m-%d')

"""
TF-IDF dataframe apply function for text value
"""
def pre_process(text):
    text = text.lower()
    text = re.sub("<!--?.*?-->","",text)
    
    ipv4_address = re.compile('^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$|^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\:\d*')
#     ipv4_address = re.compile('\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}\:\d*|\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}|\b\w\w+\b')
    ip = re.match(ipv4_address, text)
    
    if ip is not None:
        return text
    else:
        text = re.sub("(\\d|\\W)+"," ",text)
    
    return text


def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)


def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """get the feature names and tf-idf score of top n items"""
#     print(feature_names)
    #use only topn items from vector
    sorted_items = sorted_items[:topn]
    
    score_vals = []
    feature_vals = []
    
    # word index and corresponding tf-idf score
    for idx, score in sorted_items:
        
        #keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])
 
    #create a tuples of feature,score
    #results = zip(feature_vals,score_vals)
    results= {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]]=score_vals[idx]
    
    return results

     
