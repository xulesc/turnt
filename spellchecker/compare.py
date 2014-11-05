#!/usr/bin/python

import impl1
import impl2
import sys, shutil, time
import random

BUF_DIR='/tmp/lmdbsc'

fname = sys.argv[1]
allwords = impl1.words(file(fname).read())
for pctg in range(1, 100, 10):
  owords = random.sample(allwords, pctg * len(allwords) / 100)
  ##
  impl1.NWORDS = impl1.train(owords)
  impl2.BUF_DIR = BUF_DIR
  shutil.rmtree('%s' %BUF_DIR) 
  (c, impl2.NWORDS) = impl2.train(owords)
  ##
  t_count = 100
  rl = random.sample(owords, t_count)
  orl = [''.join(random.sample(word, len(word))) for word in owords]
  t1 = time.clock()
  r_count = 10
  ##
  for i in range(0, r_count):
    for w1, w2 in zip(rl, orl):
      impl1.correct(w1); impl1.correct(w2);
  et_base = (time.clock() - t1)/t_count/r_count/2
  ##
  t1 = time.clock()
  for i in range(0, r_count):
    for w1, w2 in zip(rl, orl):
      impl2.correct(w1); impl2.correct(w2);
  et_lmdb = (time.clock() - t1)/t_count/r_count/2
  ##
  print '%s\t%d\t%f\t%f' %(fname,len(owords), et_base, et_lmdb)

print 'done'
  
