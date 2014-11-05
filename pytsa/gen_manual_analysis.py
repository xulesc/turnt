# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 21:01:07 2014

base
24-June-2014: 
    + drop stop words + use tokenizer + drop URLs: 
        -1: p: 0.535135, r: 0.559322
        0: p: 0.586207, r: 0.122302
        1: p: 0.492958, r: 0.769231
    + apply stemmer: *****REMOVED*****
        p: 0.593596, r: 0.742719, t: 0.502892
        
28-Jun-2014:
    + apply POS
        -1: p: 0.407407, r: 0.310734
        0: p: 0.316456, r: 0.359712
        1: p: 0.419512, r: 0.472527


    
@author: xule
"""

import re

from collections import defaultdict
from nltk.tokenize import RegexpTokenizer

#from nltk.stem.porter import PorterStemmer

senti_wordnet_file = 'model/SentiWordNet_3.0.0_20130122.txt'
#dataset_file = 'gw2_microsoft_dhoni.tsv'
dataset_file = 'testdata.manual.2009.06.14.csv'
#'testdata.manual.2009.06.14.0_4.csv' 
#'training.1600000.processed.noemoticon.utf8.csv'
#out_file = 'gw2_microsoft_dhoni_classified.tsv'
out_file = 'pmi_manual_analysis.tsv'
tokenizer = RegexpTokenizer(r'\w+')

STOPWORDS = ['a','able','about','across','after','all','almost','also','am','among',
'an','and','any','are','as','at','be','because','been','but','by','can',
'cannot','could','dear','did','do','does','either','else','ever','every',
'for','from','get','got','had','has','have','he','her','hers','him','his',
'how','however','i','if','in','into','is','it','its','just','least','let',
'like','likely','may','me','might','most','must','my','neither','no','nor',
'not','of','off','often','on','only','or','other','our','own','rather','said',
'say','says','she','should','since','so','some','than','that','the','their',
'them','then','there','these','they','this','tis','to','too','twas','us',
'wants','was','we','were','what','when','where','which','while','who',
'whom','why','will','with','would','yet','you','your']
STOP_WORDS_DICT = dict((k,2) for k in STOPWORDS)
nltk_to_smodel_mapper = {'ADJ': 'a', 'ADV': 'r', 'N': 'n', 'NP': 'n', 'V': 'v', 'VD': 'v', 'VG': 'v', 'VN': 'v'}

import nltk.data, nltk.tag
tagger = nltk.data.load(nltk.tag._POS_TAGGER)
#stemmer = PorterStemmer()

def get_prec_reca(a, b, c):
    p = 0; r = 0;
    if a + b > 0:
        p = 1.0 * a / (a + b)
    if a + c > 0: 
        r = 1.0 * a / (a + c)
    return [p, r]

def remove_stop_words(wordlist, stopwords=STOPWORDS):
    marked = []
    for t in wordlist:
        if STOP_WORDS_DICT.get(t) == None:
            marked.append(t)
    return marked
    
def match_nltk_to_smodel(nltk_tag):
    if nltk_tag == None:
        return None
    elif nltk_tag[0].lower() == 'v':
        return 'v'
    elif nltk_tag[0].lower() == 'n':
        return 'n'
    elif nltk_tag[0].lower() == 'j':
        return 'a'
    elif nltk_tag[0:2] == 'RB':
        return 'r'
    return None

def sentence_pmi(sentence, s_model):
    n_sentence = re.sub(r'^https?:\/\/.*[\r\n]*', '', sentence, flags=re.MULTILINE)
    o_words = tokenizer.tokenize(n_sentence)
    o_words_pos = tagger.tag(o_words)
    #print o_words_pos
    words = remove_stop_words(map(lambda x : x.lower(), o_words))
    p_w = []; n_w = []; p_s = 0; n_s = 0; 
    for w, pos in zip(words, o_words_pos):
        ##scores = s_model.get(stemmer.stem(w))
        s_pos = match_nltk_to_smodel(pos[1])
        if s_pos == None:
            continue
        scores = s_model[s_pos].get(w)
        #scores = s_model.get(w)
        if scores == None:
            continue
        l_p_s = 0; l_n_s = 0
        for s in scores:
            l_p_s += s[0]
            l_n_s += s[1]
        l_p_s = l_p_s * 1.0 / len(scores)
        l_n_s = l_n_s * 1.0 / len(scores)
        if l_p_s > 0:
            p_s += l_p_s
            p_w.append('%s:%f' %(w,l_p_s))
        if l_n_s > 0:
            n_s += l_n_s
            n_w.append('%s:%f' %(w,l_n_s))
    t = len(p_w) + len(n_w)
    if t > 0:
        p_s = p_s / t
        n_s = n_s / t
    pmi = p_s - n_s
    return [pmi, p_s, n_s, p_w, n_w]

## load the sentinet data
def load_senti_data(infile):
    ret = defaultdict(list)
    for line in open(infile, 'r'):
        if line.find('#') == 0:
            continue
        data = line.split('\t')
        if len(data[0].strip()) == 0:
            continue
        p_score = float(data[2])
        n_score = float(data[3])
        words = map(lambda a: a[:a.index('#')], data[4].split(' '))
        for word in words:
            #ret[stemmer.stem(word.lower())].append([p_score, n_score])
            ret[word.lower()].append([p_score, n_score])
    return ret
    
## load the sentinet data
def load_senti_data_pos(infile):
    ret = defaultdict(lambda: defaultdict(list))
    for line in open(infile, 'r'):
        if line.find('#') == 0:
            continue
        data = line.split('\t')
        if len(data[0].strip()) == 0:
            continue
        ret_pos = ret[data[0]]
        p_score = float(data[2])
        n_score = float(data[3])
        words = map(lambda a: a[:a.index('#')], data[4].split(' '))
        for word in words:
            #ret[stemmer.stem(word.lower())].append([p_score, n_score])
            ret_pos[word.lower()].append([p_score, n_score])
    return ret    
        
## parse data set file and generate output per line
senti_model = load_senti_data_pos(senti_wordnet_file)
#senti_model = load_senti_data(senti_wordnet_file)
out = open(out_file, 'w')
#out.write('t_klass\tp_klass\tpmi\tp_s\tn_s\tp_w\tn_w\ttweet_text\n')
n_tp = 0; n_fp = 0; n_fn = 0
z_tp = 0; z_fp = 0; z_fn = 0
p_tp = 0; p_fp = 0; p_fn = 0
for line in open(dataset_file, 'r'):
    line = line.replace('\n','')
    if len(line) == 0:
        continue
    #data = line.split('\t')
    data = line[1:len(line)-1].split('","')
    #if len(data) != 2:
    if len(data) < 5:
        continue
    ##
    #query = data[0]
    #tweet_text = data[1]
    t_klass = int(data[0])
    if t_klass == 0:
        t_klass = -1
    elif t_klass == 2:
        t_klass = 0
    else:
        t_klass = 1
    query = t_klass
    tweet_text = data[5]
    ##
    pmi, p_s, n_s, p_w, n_w = sentence_pmi(tweet_text, senti_model)
    if pmi < 0:
        p_klass = -1
    elif pmi == 0:
        p_klass = 0
    else:
        p_klass = 1
    #
    if t_klass == -1 and p_klass == -1:
        n_tp += 1
    if t_klass == -1 and p_klass != -1:
        n_fn += 1
    if t_klass != -1 and p_klass == -1:
        n_fp += 1
        
    if t_klass == 0 and p_klass == 0:
        z_tp += 1
    if t_klass == 0 and p_klass != 0:
        z_fn += 1
    if t_klass != 0 and p_klass == 0:
        z_fp += 1
        
    if t_klass == 1 and p_klass == 1:
        p_tp += 1
    if t_klass == 1 and p_klass != 1:
        p_fn += 1
    if t_klass != 1 and p_klass == 1:
        p_fp += 1
    #        
    out.write('%d\t%s\t%s\t%s\t%s\t%f\t%f\t%f\t\n' %(p_klass,query,tweet_text,'-'.join(p_w),'-'.join(n_w),pmi,p_s,n_s))
##    
out.close()
n_prec, n_reca = get_prec_reca(n_tp, n_fp, n_fn)
print '-1: p: %f, r: %f' %(n_prec, n_reca)
z_prec, z_reca = get_prec_reca(z_tp, z_fp, z_fn)
print '0: p: %f, r: %f' %(z_prec, z_reca)
p_prec, p_reca = get_prec_reca(p_tp, p_fp, p_fn)
print '1: p: %f, r: %f' %(p_prec, p_reca)

##
