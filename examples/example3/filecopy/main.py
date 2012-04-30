#!/usr/bin/env python
# encoding: utf-8

'''
Here is a simple example demonstrating plugnplay in action.
This example implements the simple program of the main README file. 
It's a copy-file program.
'''

import sys
import os
import shutil

import plugnplay


from interfaces import HashChecker

if len(sys.argv) <= 1:
    sys.stdout.write("Need one parameter, the file to duplicate\n")
    sys.exit(1)

plugnplay.plugin_dirs = ['./plugins',]
plugnplay.load_plugins()

where_to_duplicate = '/tmp/duplicate'

original_file = sys.argv[1]

if not os.path.exists(original_file):
    sys.stdout.write("Original file does not exist: %s\n" % original_file)
    sys.stdout.write("Exiting...\n")
    sys.exit(1)

shutil.copy(original_file, where_to_duplicate)

for listener in HashChecker.implementors():
    sys.stdout.write("Running copy checker %s\n" % repr(listener))
    if not listener.check(original_file, where_to_duplicate):
        sys.stdout.write("Copy failed. Checksum Error\n")
        sys.exit(1)


sys.stdout.write("Copy done!\n")
