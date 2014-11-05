# -*- coding: utf-8 -*-
"""
Created on Sat Jun 14 18:37:21 2014

@author: xule
"""

##
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  5 09:12:15 2014

@author: anuj
"""
## change matplotlib to use X-backend 
#import matplotlib
#matplotlib.use('Agg')

import csv
from time import time
import cPickle

from sklearn import preprocessing
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.naive_bayes import GaussianNB
#from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import auc

from collections import defaultdict

trg_file = 'straining.1600000.processed.noemoticon.utf8.csv'
senti_data = 'model/SentiWordNet_3.0.0_20130122.txt'
## MODEL FILES ##
classifier_file = 'model/nb/classifier.pkl' 
vectorizer_file = 'model/nb/vectorizer.pkl'
lsa_file = 'model/nb/lsa.pkl'
senti_file = 'model/senti.pkl'
##
min_max_scaler = preprocessing.MinMaxScaler()
csv_reader = lambda x: csv.reader(open(x, 'rb'), delimiter=',', quotechar='"')
def read_data(reader, X_col = 5, Y_col = 0):
    return zip(*map(lambda x: (x[X_col], int(x[Y_col])/4), reader))
    
def prep_fv(Xin, vectorizer, lsa):
    return vectorizer.fit_transform(Xin).todense()

def cm_score(cm):
    a, b = cm[0]; c, d = cm[1]
    precision = 1.0 * a / (a + b)
    npv = 1.0 * d / (c + d)
    sensitivity = 1.0 * a / (a + c)
    specificity = 1.0 * d / (b + d)
    acc = 1.0 * (a + d) / (a + b + c + d)
    return 'precision = %f, npv = %f, sensitivity = %f, specificity = %f, acc = %f'%(precision,npv,sensitivity,specificity,acc)
    
##
t0 = time()
clf = GaussianNB()
vectorizer = TfidfVectorizer(max_df=0.5, max_features=100, stop_words='english', use_idf=True)
lsa = TruncatedSVD(2)
## TRAINING ##
print("Training")
X_trg, Y_trg = read_data(csv_reader(trg_file))
X = prep_fv(X_trg, vectorizer, lsa)
#pl.boxplot(X)
clf.fit(X, Y_trg)
## Saving ##
print("Saving model")
cPickle.dump(clf, open(classifier_file, 'wb'))  
cPickle.dump(vectorizer, open(vectorizer_file, 'wb'))  
cPickle.dump(lsa, open(lsa_file, 'wb'))  
## Loading ##
print("Loading model")
clf = cPickle.load(open(classifier_file, 'rb'))
vectorizer = cPickle.load(open(vectorizer_file, 'rb'))
lsa = cPickle.load(open(lsa_file, 'rb'))
## TESTING ##
print("Testing")
X_tst, Y_tst = read_data(csv_reader(trg_file))
T = prep_fv(X_tst, vectorizer, lsa)
cm = confusion_matrix(clf.predict(T), Y_tst)
print(cm_score(cm))
# Compute Precision-Recall and plot curve
probas_ = clf.predict_proba(T)
precision, recall, thresholds = precision_recall_curve(Y_tst, probas_[:, 1])
area = auc(recall, precision)
print("Area Under Curve: %0.2f" % area)
##
senti_model = defaultdict(list)
for line in open(senti_data, 'r'):
    if line.find('#') == 0:
        continue
    data = line.split('\t')
    if len(data[0].strip()) == 0:
        continue
    p_score = float(data[2])
    n_score = float(data[3])
    words = map(lambda a: a[:a.index('#')], data[4].split(' '))
    for word in words:
        senti_model[word].append([p_score, n_score])
cPickle.dump(senti_model, open(senti_file, 'wb'))  

##
#Integer utermPaperCount = positiveUniverseTermCounts.get(term);
#if (utermPaperCount != null) {
#    final double a = Math.exp(Math.log(termPaperCount)
#            - Math.log(paperUniverseCount));
#    final double b = Math.exp(Math.log(termPaperCount)
#            + Math.log(commonPaperCount) - 2
#            * Math.log(paperUniverseCount));
#    final double d = Math.exp(Math.log(a - b) - 0.5 * Math.log(b));
#    final double f = (Math.log(termPaperCount) / Math.log(2) + Math
#            .log(paperUniverseCount) / Math.log(2))
#            - (Math.log(utermPaperCount) / Math.log(2) + Math
#                    .log(commonPaperCount) / Math.log(2));
#    if (Math.abs(d) > 0.15)
#        positivePMI += d * f;
#    log.trace("positivePMI: " + positivePMI);
#    continue;
#}

##
