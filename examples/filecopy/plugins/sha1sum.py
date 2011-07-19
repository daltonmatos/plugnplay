
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

class SHA1(Plugin):
  implements = [HashChecker]


  def check(self, file1, file2):
    sha1_1 = hashlib.sha1(open(file1, encoding='utf-8').read().encode('utf-8')).hexdigest()
    sha1_2 = hashlib.sha1(open(file2, encoding='utf-8').read().encode('utf-8')).hexdigest()
    if sha1_1 == sha1_2:
      sys.stdout.write("SHA-1 OK: %s\n" % sha1_1)
      return True
    else:
      return False


