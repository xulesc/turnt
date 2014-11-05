#!/usr/bin/python

import string

veb_loc = "/home/xule/workspace/veb"
tpl_loc = veb_loc + "/template_files"
cfg_loc = veb_loc + "/config_files"

def get_settings_map():
  s = {}
  for x in open(".veb_conf", "r"):
    (k, v) = x.replace('\n', '').split(':')
    s[k] = string.strip(v)
  return s
  
def create_file_from_template(fin, fout, tag_map):
  for l in fin.readlines():
    for k,v in tag_map.iteritems():
      l = l.replace(k,v)
    fout.write(l)

def create_project(loc = None, name = None):
  if loc == None:
    loc = raw_input("Project location: ")
  if name == None:
    name = raw_input("Project name: ")
    
  script = "%s/scripts/create_project_dirs.sh" %(veb_loc)
  cmd = "sh %s %s %s %s %s" %(script, loc, name, tpl_loc, cfg_loc)
  
  import os
  os.system(cmd)  
  
def create_vhdl_module(name = None):
  if name == None:
    name = raw_input("Module name: ")
  
  settings = get_settings_map()
  path = settings['path']
  
  tpl_fh = open(path + "/.templates/vhdl_module.tpl", 'r')
  src_fh = open(path + "/src/" + name + ".vhd", 'w')
  create_file_from_template(tpl_fh, src_fh, {'@module_name@': name})
  
if __name__ == '__main__':
  import sys
  
  if len(sys.argv) < 2:
    print 'All is well. Nothing to do.'
    sys.exit(0)
  
  func = sys.argv[1]
  eval(func + "()")