import unittest
import plugnplay
from os.path import dirname, join, abspath
from mock import Mock


class LoadingTest(unittest.TestCase):

    def setUp(self):
        self.basepath = dirname(abspath(__file__))
        self.full_path = join(self.basepath, 'plugin/')
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
        self.assertFalse(plugnplay.normalize_path(self.full_path) + '.someplugin' in sys.modules)

        plugnplay.set_plugin_dirs(self.full_path)
        plugnplay.load_plugins()

        self.assertTrue(plugnplay.normalize_path(self.full_path) + '.someplugin' in sys.modules)
        import someplugin  # Test de importing of the new plugin
        self.assertTrue(someplugin.SomePlugin is not None)
        p = someplugin.SomePlugin()
        self.assertTrue(isinstance(p, someplugin.SomePlugin))

    def test_load_plugin_with_error(self):
        import sys
        plugindir = join(self.basepath, 'wrong-plugins/')
        plugnplay.set_plugin_dirs(plugindir)
        mock_logger = Mock()
        plugnplay.load_plugins(logger=mock_logger)
        self.assertEquals(1, mock_logger.debug.call_count)
        call_args = mock_logger.debug.call_args
        self.assertEquals("Error loading plugin: myplugin",  call_args[0][0])
        self.assertTrue('exc_info' in call_args[1])
        self.assertTrue(call_args[1]['exc_info'] is not None)
        self.assertTrue('myplugin' not in sys.modules)
        self.assertTrue(plugnplay.normalize_path(plugindir) + '.otherplug' in sys.modules)

    def test_normalize_path(self):
        self.assertEquals('some.module.path', plugnplay.normalize_path('/some/module/path'))
        self.assertEquals('other.module.path', plugnplay.normalize_path('./other/module/path'))
        self.assertEquals('some.module.path', plugnplay.normalize_path('../..//some//module/path'))
        self.assertEquals('some.module.path', plugnplay.normalize_path('/some/../module/path/'))

    def test_load_same_name_different_folders(self):
        import sys
        dir1 = join(self.basepath, 'plugin/dir1')
        dir2 = join(self.basepath, 'plugin/dir2')
        plugnplay.set_plugin_dirs(dir1, dir2)
        plugnplay.load_plugins()

        dir1_norm = plugnplay.normalize_path(dir1)
        dir2_norm = plugnplay.normalize_path(dir2)

        self.assertTrue(dir1_norm + '.otherplugin' in sys.modules)
        self.assertTrue(dir2_norm + '.otherplugin' in sys.modules)

        mod1 = sys.modules[dir1_norm + '.otherplugin']
        print mod1
        self.assertTrue(mod1.MyPlugin.dir1)

        mod2 = sys.modules[dir2_norm + '.otherplugin']
        print mod2
        self.assertTrue(mod2.MyPlugin.dir2)
