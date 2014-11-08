#!/usr/bin/python

"""
A simple script that generates openbox menu.xml from a more intuitive tree file.

Using a single space as indent a tree hierarchy can be generated showing the menu 
tree. The leaf nodes of the tree is the actual command to be run. The command/action
should be specifed as ITEM_NAME,ACTION_TYPE,COMMAND. A sample input file to this 
program would be:
---------
ToDel
 TestEntry
  TestItem
Development
 Eclipse,Execute,eclipse
Web
 Iceweasel,Execute,iceweasel
--
Office
 Libreoffice,Execute,libreoffice
Multimedia
 VLC,Execute,vlc
--
Shutdown
 Log Out,Execute,openbox --exit
---------

The program expects to read the input lines from the stdin so a typical way to run 
this program would be:
cat menu.lst | ./simplemenugen.py > menu.xml

The menu.xml can then be moved to the openbox config folder.

author: anuj
"""

import sys
from itertools import takewhile
from lxml import etree

SEPARATOR='--'

def get_etree_node(id, label):
  if label == SEPARATOR:
    return etree.Element('separator')
  v = etree.Element('menu')
  v.set('id', '%d' %id)
  v.set('label', label)
  return v
  
def get_etree_leaf(label, action, cmd):
  v_cmd = etree.Element('command')
  v_cmd.text = cmd
  v_action = etree.Element('action')
  v_action.set('name', action)
  v_action.append(v_cmd)
  v_item = etree.Element('item')
  v_item.set('label', label)
  v_item.append(v_action)
  return v_item

def build_tree(lines):
  ind = ' '.__eq__; idcnt = 0
  lines = iter(lines); stack = []; ref = {}
  ##
  root = etree.Element("openbox_menu")
  root_menu_entry = etree.Element("menu")
  root_menu_entry.set('label', 'Openbox 3')
  root_menu_entry.set('id', 'root-menu')
  root.append(root_menu_entry)
  ##
  tree = root_menu_entry
  for line in lines:
    indent = len(list(takewhile(ind, line)))    
    stack[indent:] = [line.lstrip()]    
    ## print stack
    m = tree
    for l in stack:
      v = ref.get(l)
      if v != None and l != SEPARATOR:
        m = v
        continue
      d = l.split(','); tcount = len(d)
      if tcount != 3:
        v = get_etree_node(idcnt, l); idcnt += 1
      else:
        v = get_etree_leaf(d[0], d[1], d[2])
      ref[l] = v
      m.append(v)
      m = v

  return root

lines = [line.replace('\n', '') for line in sys.stdin]
print (etree.tostring(build_tree(lines), pretty_print=True))

  
