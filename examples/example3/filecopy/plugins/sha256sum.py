import sys

# We have to do this so we can use HashChecker without
# Installing this example with python setup install
#dirname = os.path.dirname(os.path.abspath(__file__))
#up_dir =  os.path.dirname(dirname)
#sys.path.append(up_dir)

from interfaces import HashChecker
import plugnplay

import hashlib

class SHA256(plugnplay.Plugin):
    implements = [HashChecker]


    def _readFile(self, fName):
        """
        Some work around code, to handle python versions that don't all specifying encoding in the open statement
        """
        try:
            return open(fName, encoding='utf-8').read().encode('utf-8')
        except TypeError:   #py2.6 doesn't support encoding= param
            return open(fName).read().encode('utf-8')


    def check(self, file1, file2):
        sha1_1 = hashlib.sha256(self._readFile(file1)).hexdigest()
        sha1_2 = hashlib.sha256(self._readFile(file2)).hexdigest()
        if sha1_1 == sha1_2:
            sys.stdout.write("SHA-2556 OK: %s\n" % sha1_1)
            return True
        else:
            return False


