#!/usr/bin/python

from io import StringIO, BytesIO
import urllib, os, errno

def require_dir(path):
  try:
    os.makedirs(path)
  except OSError, exc:
    if exc.errno != errno.EEXIST:
      raise
  
def retrieve_image(fname, d_dir, url):
  ffname = '%s/%s' %(d_dir, fname)
  if os.path.exists(ffname):
    return
  require_dir(d_dir)
  urllib.urlretrieve(url, ffname)
  
