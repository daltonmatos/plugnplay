import hashlib
import sys

# We have to do this so we can use HashChecker without
# Installing this example with python setup install
#dirname = os.path.dirname(os.path.abspath(__file__))
#up_dir =  os.path.dirname(dirname)
#sys.path.append(up_dir)

from interfaces import HashChecker
import plugnplay


class MD5(plugnplay.Plugin):
  implements = [HashChecker]

  def _readFile(self, fName):
      try:
        return open(fName, encoding='utf-8').read().encode('utf-8')
      except TypeError:
          return open(fName).read().encode('utf-8')

  def check(self, file1, file2):
    """
    implement the check method enforced in the Interface
    """
    md5_1 = hashlib.md5(self._readFile(file1)).hexdigest()
    md5_2 = hashlib.md5(self._readFile(file2)).hexdigest()
    if md5_1 == md5_2:
      sys.stdout.write("MD5sum OK: %s\n" % md5_1)
      return True
    else:
      return False


