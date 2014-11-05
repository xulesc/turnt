#!/usr/bin/python
import os
from collections import defaultdict

#virtenv = os.environ['OPENSHIFT_PYTHON_DIR'] + '/virtenv/'
#virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
#try:
#    execfile(virtualenv, dict(__file__=virtualenv))
#except IOError:
#    pass
#
# IMPORTANT: Put any additional includes below this line.  If placed above this
# line, it's possible required libraries won't be in your searchable path
#
#import matplotlib.pyplot as plt
#import scipy
#from sklearn.cross_validation import train_test_split
##
import cPickle
#from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.decomposition import TruncatedSVD
##
from tsa import TSA

##
base_dir = '%s/app-deployments/current/repo' %os.getcwd()
#base_dir = '%s' %os.getcwd()
#classifier_file = '%s/model/nb/classifier.pkl' %base_dir
#vectorizer_file = '%s/model/nb/vectorizer.pkl' %base_dir
#lsa_file = '%s/model/nb/lsa.pkl' %base_dir
senti_file = '%s/model/senti.pkl' %base_dir
 
#def load_models():
#    print("loading model")
#    clf = cPickle.load(open(classifier_file, 'rb'))
#    vectorizer = cPickle.load(open(vectorizer_file, 'rb'))
#    lsa = None #cPickle.load(open(lsa_file, 'rb'))
#    senti_model = cPickle.load(open(senti_file, 'rb'))
#    return clf, vectorizer, lsa, senti_model

##
#g_clf, g_vectorizer, g_lsa, g_senti_model = load_models()
g_senti_model = cPickle.load(open(senti_file, 'rb'))
g_tsa = TSA(g_senti_model)
##
        
def scale_zero_to_one(data, polarity):
    max_v_0 = max([d for d, p in zip(data,polarity)  if p == 0])
    min_v_0 = min([d for d, p in zip(data,polarity)  if p == 0])
    max_v_1 = max([d for d, p in zip(data,polarity)  if p == 1])
    min_v_1 = min([d for d, p in zip(data,polarity)  if p == 1])
    ret = []
    for d, p in zip(data, polarity):
        if p == 0:
            ret.append(1.0 * (d - min_v_0) / (max_v_0 - min_v_0))
        if p == 1:
            ret.append(1.0 * (d - min_v_1) / (max_v_1 - min_v_1))
    return ret

def application(environ, start_response):
    ctype = 'text/plain'
    if environ['PATH_INFO'] == '/health':
        response_body = "1"
    elif environ['PATH_INFO'] == '/env':
        response_body = ['%s: %s' % (key, value)
                    for key, value in sorted(environ.items())]
        response_body = '\n'.join(response_body)
    elif environ['PATH_INFO'].find('/tw/') == 0:
        query = environ['PATH_INFO'].replace('/tw/','').strip()
        search_results = g_tsa.get_tweets(query)
        klasses, polarities, confidences = g_tsa.fit_pmi(search_results)         
        out = ['class\txval\tyval\ttweet']
        #p1 = scale_zero_to_one(polarities, klasses)
        for klass, polarity, confidence, tweet in zip(klasses, polarities, confidences, search_results):
            out.append('%d\t%f\t%f\t\'%s\'' %(klass, polarity, confidence, tweet.replace('\n',' ').replace('\r',' ')))
        response_body = '%s\n' %'\n'.join(out)
    else:
        ctype = 'text/html'
        response_body = '''<!doctype html>
<html lang="en">
<head>
</head>
<body>
Twitter sentiment analysis 
</body>
</html>'''

    status = '200 OK'
    response_headers = [('Content-Type', ctype), ('Content-Length', str(len(response_body)))]
    #
    start_response(status, response_headers)
    return [response_body]

#
# Below for testing only
#
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('localhost', 8051, application)
    # Wait for a single request, serve it and quit.
    httpd.handle_request()
