from plugnplay import Interface

class HashChecker(Interface):

  '''
    Called to check the hash of the two files
    Receive the two files: original and copy
    return True if the copy was OK or False if some error ocurred
  '''
  def check(self, original_file, dup_file):
    pass


