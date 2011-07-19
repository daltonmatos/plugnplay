


import unittest
import plugnplay
from os.path import dirname, join, abspath

class LoadingTest(unittest.TestCase):

  def setUp(self):
    self.full_path =  join(dirname(abspath(__file__)), 'plugin/')
    plugnplay.plugin_dirs = []

  def test_add_plugin_path(self):
    plugnplay.set_plugin_dirs(self.full_path)
    self.assertEquals([self.full_path], plugnplay.plugin_dirs)

  def test_add_relative_plugin_dir(self):
    try:
      plugnplay.set_plugin_dirs(['some/relative/path'])
      self.fail("Did not raise exception")
    except Exception:
      pass

  def test_load_external_py_file(self):
    import sys
    self.assertFalse('someplugin' in sys.modules)
    
    plugnplay.set_plugin_dirs(self.full_path)
    plugnplay.load_plugins()

    self.assertTrue('someplugin' in sys.modules)
    import someplugin #Test de importing of the new plugin
    self.assertTrue(someplugin.SomePlugin is not None)
    p = someplugin.SomePlugin()
    self.assertTrue(isinstance(p, someplugin.SomePlugin))

    
