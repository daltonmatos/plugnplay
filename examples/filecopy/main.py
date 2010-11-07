#!/usr/bin/env python
# encoding: utf-8

import sys, os
from shutil import copy
from glob import glob
from interfaces import HashChecker


if len(sys.argv) <= 1:
  print "Need one parameter, the file to duplicate"
  sys.exit(1)


plugins = os.environ.get('PLUGIN_DIR', None)
if plugins:
  files = glob(os.path.join(plugins, '*.py'))
  sys.path.append(plugins) # So we can import files
  for plugin in files:
    __import__(os.path.basename(plugin).strip('.py'))


where_to_duplicate = '/tmp/duplicate'

original_file = sys.argv[1]

if not os.path.exists(original_file):
  print "Original file does not exist: %s" % original_file
  print "Exiting..."
  sys.exit(1)

copy(original_file, where_to_duplicate)

for listener in HashChecker.implementors():
  if not listener.check(original_file, where_to_duplicate):
    print "Copy failed. Checksum Error"
    sys.exit(1)


print "Copy done!"
