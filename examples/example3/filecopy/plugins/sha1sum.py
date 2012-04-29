import hashlib
import sys

# We have to do this so we can use HashChecker without
# Installing this example with python setup install
#dirname = os.path.dirname(os.path.abspath(__file__))
#up_dir =  os.path.dirname(dirname)
#sys.path.append(up_dir)

from interfaces import HashChecker
import plugnplay



class SHA1(plugnplay.Plugin):
  implements = [HashChecker]


  def _readFile(self, fName):
      try:
          return open(fName, encoding='utf-8').read().encode('utf-8')
      except TypeError:
          return open(fName).read().encode('utf-8')


  def check(self, file1, file2):
      sha1_1 = hashlib.sha1(self._readFile(file1)).hexdigest()
      sha1_2 = hashlib.sha1(self._readFile(file2)).hexdigest()
      if sha1_1 == sha1_2:
          sys.stdout.write("SHA-1 OK: %s\n" % sha1_1)
          return True
      else:
          return False


