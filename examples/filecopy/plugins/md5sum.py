
import sys
import os

# We have to do this so we can use HashChecker without
# Installing this example with python setup install
dirname = os.path.dirname(os.path.abspath(__file__))
up_dir =  os.path.dirname(dirname)
sys.path.append(up_dir)

from interfaces import HashChecker
from plugnplay import Plugin, man

import hashlib

class MD5(Plugin):
  implements = [HashChecker]


  def check(self, file1, file2):
    md5_1 = hashlib.md5(file(file1).read()).hexdigest()
    md5_2 = hashlib.md5(file(file2).read()).hexdigest()
    if md5_1 == md5_2:
      print "MD5sum OK: %s" % md5_1
      return True
    else:
      return False



