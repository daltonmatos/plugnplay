#!/usr/bin/env python
# encoding: utf-8

'''

== Examples ===

Here is a simple example demonstrating plugnplay in action. 
This example implements the simple program of the main README file. 
It's a copy-file program.

Here is what is needed to run it.
 
 * First install plugnplay globally. You can do this running (at the root of the project)
   sudo python setup.py install
 * cd to the examples/filecopy folder: cd examples/filecopy
 * Then, run the main.py file: 
    python main.py <file-to-copy>
 * You will see this output:
    Copy done!
 * Now, run it with a different command line:
   PLUGIN_DIR=plugins python main.py <file-to-copy>
 * And see that the output is quite different. Thats why the plugins were called.


Now take a look at the code to see how easy is to add another plugin and as an exercise for you 
I will ask you to implement another HashChecker plugin, now for sha-256. Save your new plugin 
inside the plugins folder and re-run the program to see your brand new plugin in action!
   

'''


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
