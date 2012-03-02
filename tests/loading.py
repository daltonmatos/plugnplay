import unittest
import plugnplay
from os.path import dirname, join, abspath
from mock import Mock


class LoadingTest(unittest.TestCase):

    def setUp(self):
        self.basepath = dirname(abspath(__file__))
        self.full_path =  join(self.basepath, 'plugin/')
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

    def test_load_plugin_with_error(self):
        import sys
        plugnplay.set_plugin_dirs(join(self.basepath, 'wrong-plugins/'))
        mock_logger = Mock()
        plugnplay.load_plugins(logger = mock_logger)
        self.assertEquals(1, mock_logger.debug.call_count)
        call_args = mock_logger.debug.call_args
        self.assertEquals("Error loading plugin: myplugin",  call_args[0][0])
        self.assertTrue('exc_info' in call_args[1])
        self.assertTrue(call_args[1]['exc_info'] is not None)
        self.assertTrue('myplugin' not in sys.modules)
        self.assertTrue('otherplug' in sys.modules)
