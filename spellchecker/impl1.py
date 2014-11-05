import sys, random
import re, collections, time

TXT_FILE='';
BUF_DIR='';
NWORDS=None;

def words(text): return re.findall('[a-z]+', text) 

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)

#######################################################################################
if __name__ == '__main__':
 TXT_FILE = sys.argv[1]

 t0 = time.clock()
 o_words = words(file(TXT_FILE).read())
 NWORDS = train(o_words)
 #print time.clock() - t0, " seconds build time"
 #print "dictionary size: %d" %len(NWORDS)
 et1 = time.clock() - t0

 t_count = 10
 rl = o_words[0:t_count] #random.sample(o_words, t_count)
 orl = [''.join(random.sample(word, len(word))) for word in o_words]
 t1 = time.clock()
 r_count = 10
 for i in range(0, r_count):
  for w1, w2 in zip(rl, orl):
   correct(w1); correct(w2)
 et2 = (time.clock() - t1)/t_count/r_count/2

 print '%d\t%f\t%f' %(len(NWORDS), et1, et2)


