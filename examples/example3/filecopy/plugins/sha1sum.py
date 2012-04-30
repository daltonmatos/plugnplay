import hashlib
import sys


from interfaces import HashChecker
import plugnplay


class SHA1(plugnplay.Plugin):
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
        """
        implement the check method enforced in the Interface
        """
        sha1_1 = hashlib.sha1(self._readFile(file1)).hexdigest()
        sha1_2 = hashlib.sha1(self._readFile(file2)).hexdigest()
        if sha1_1 == sha1_2:
            sys.stdout.write("SHA-1 OK: %s\n" % sha1_1)
            return True
        else:
            return False


