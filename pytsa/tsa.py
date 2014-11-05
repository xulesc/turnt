# -*- coding: utf-8 -*-
"""
Created on Sat Jun 14 18:15:37 2014

@author: xule
"""

import twitter
from datetime import datetime, timedelta

class TSA:
    def __init__(self, model=None):
        #print('TSA init')
        ##
        self.TWEET_COUNT = 100
        ##
        CONSUMER_KEY='GowqSkW2IuDr1QsZhHLMg1A1M'
        CONSUMER_KEY=CONSUMER_KEY.encode('utf-8')
        CONSUMER_SECRET='oXFDHarXsLUHFnFwl0OQ8XDXMDzKPNdsaqS8RnYB5kkIGWEtep'
        CONSUMER_KEY=CONSUMER_KEY.encode('utf-8')
        ACCESS_TOKEN_KEY='2543125176-oKA26SP90cLRwjbjaS0Dj4xIBY1lWyi5nve66Rm'
        ACCESS_TOKEN_KEY=ACCESS_TOKEN_KEY.encode('utf-8')
        ACCESS_TOKEN_SECRET='VpBHTXgDWLAwLU497ObMjKRPVECR6JvFVVHsr9uQUqw7j'
        ACCESS_TOKEN_SECRET=ACCESS_TOKEN_SECRET.encode('utf-8')
        self.api = twitter.Api(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, access_token_key=ACCESS_TOKEN_KEY, access_token_secret=ACCESS_TOKEN_SECRET)
        ##
        if model != None:
            self.pos_terms = {}; self.neg_terms = {}
            for word, scores in model.iteritems():
                psum = 0; nsum = 0;
                for s in scores:
                    psum += s[0]; nsum += s[1]
                if psum - nsum < 0:
                    self.neg_terms[word] = psum / len(scores)
                else:
                    self.pos_terms[word] = nsum / len(scores)

    def prep_fv(self, Xin, vectorizer, lsa):
        return vectorizer.fit_transform(Xin).todense()
        #return lsa.fit_transform(vectorizer.fit_transform(Xin))
        #return Normalizer(copy=False).fit_transform(lsa.fit_transform(vectorizer.fit_transform(Xin)))

    def get_pmi(self, X, s_model):
        ret = []; p_s = 0; n_s = 0; max_v = 0;
        for sentence in X:
            words = sentence.split(' ')
            for w in words:
                scores = s_model[w]
                for s in scores:
                    p_s += s[0]
                    n_s += s[1]
            pmi = (p_s - n_s) * 1.0 / len(words)
            if abs(pmi) > max_v:
                max_v = abs(pmi)
            ret.append(pmi)  
        return map(lambda x: x/max_v, ret)
    
    def get_polarity(self, X, vectorizer, clf, lsa, senti_model):
        print("tweet count: %d" %len(X))
        T = self.prep_fv(X, vectorizer, lsa)
        return X, clf.predict(T), clf.predict_proba(T)[:, 1], self.get_pmi(X, senti_model)
    
    def get_tweets(self, query):
        #print('getting tweets for: %s' %query)        
        search_results = set()
        for x in range(10):
            u = str(datetime.now() + timedelta(days=-x)).split(' ')[0]
            search = self.api.GetSearch(term=query, lang='en', result_type='recent', count=self.TWEET_COUNT, until=u)
            for s in search:
                words = s.text.encode('utf-8')
                if len((words + ' ').split(' ')) < 3:
                    continue
                search_results.add(words)
        return search_results
                    
    def fit_pmi(self, X):
        ks = []; polarities = []; confs = []
        for x in X:
            p = 0; n = 0; pw = []; nw = []
            for w in x.split(' '):
                s = self.pos_terms.get(w)
                if s != None and s != 0.0:
                    if p == 0:
                        p = 1.0
                    p *= s
                    pw.append(w)
                s = self.neg_terms.get(w)
                if s != None and s != 0.0:
                    if n == 0:
                        n = 1.0
                    n *= s
                    nw.append(w)
            r = 0
            if len(pw) != 0 or len(nw) != 0:
                r = 1.0 * min([len(pw), len(nw)]) / max([len(pw), len(nw)])
            if p-n < 0:
                k = 0
            elif p-n == 0:
                k = -1
            else:
                k = 1
            ks.append(k); polarities.append(p-n); confs.append(r)
        return ks, polarities, confs
##
if __name__ == '__main__':
    tsa = TSA()
    queries = ['gw2', 'microsoft', 'dhoni']
    for query in queries:
        tweets = tsa.get_tweets(query)
        for tweet in tweets:
            print('%s\t%s' %(query,tweet))
##    
