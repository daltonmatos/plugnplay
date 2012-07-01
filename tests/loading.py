import unittest
import plugnplay
from os.path import dirname, join, abspath
from mock import Mock
import mock
import sys


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

    def test_find_implementors_different_import(self):
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from interfaces import myinterface
        import interfaces

        class MyImplementor(plugnplay.Plugin):

            implements = [myinterface.MyInterface]

            pass

        self.assertEquals(1, len(myinterface.MyInterface.implementors()))
        self.assertEquals(1, len(interfaces.myinterface.MyInterface.implementors()))

    def test_load_plugins_from_a_python_package(self):
        """
        See github issue #6.
        """
        from allinone.interface import AllInOne
        import allinone
        from allinone import interface
        all_in_one_dir = join(self.basepath, 'allinone')
        plugnplay.set_plugin_dirs(all_in_one_dir)
        logger = Mock()
        plugnplay.load_plugins(logger)

        # Check that we did not try to load a plugin named __init__.
        # See Github issue #9
        self.assertEquals(0, logger.debug.call_count)
        self.assertTrue(dirname(all_in_one_dir) in sys.path, "sys.path not modified correctly")
        self.assertEquals(len(AllInOne.implementors()), 1)
        self.assertEquals(len(allinone.interface.AllInOne.implementors()), 1)
        self.assertEquals(len(interface.AllInOne.implementors()), 1)

    def test_load_plugins_in_alphabetical_order(self):
        import os
        base_dir = os.path.join(self.basepath, 'sortedloading')
        dir1 = os.path.join(base_dir, 'dir1')
        dir2 = os.path.join(base_dir, 'dir2')
        dirs = [base_dir, dir1, dir2]

        plugnplay.set_plugin_dirs(*dirs)
        with mock.patch('plugnplay._import_module') as import_mock:
            plugnplay.load_plugins()
            assert 7 == import_mock.call_count
            #``aplug.py, dir1/aplug.py, dir2/bplug.by, dir1/cplug.py, dir2/dplug.py, dir2/pplug.py, zplug.py``
            call_list = [
                    mock.call(base_dir, 'aplug', logger=None),
                    mock.call(dir1, 'aplug', logger=None),
                    mock.call(dir2, 'bplug', logger=None),
                    mock.call(dir1, 'cplug', logger=None),
                    mock.call(dir2, 'dplug', logger=None),
                    mock.call(dir2, 'pplug', logger=None),
                    mock.call(base_dir, 'zplug', logger=None),
                    ]
            assert call_list == import_mock.call_args_list

    def test_load_filtered_implementors(self):
        class MyInterface(plugnplay.Interface):
            pass

        class FirstImplementor(plugnplay.Plugin):
            implements = [MyInterface, ]

        class SecondImplementor(plugnplay.Plugin):
            implements = [MyInterface, ]

        def _filter_first_implementor(implementor):
            return implementor.__class__.__name__ == 'FirstImplementor'

        filtered_implementor = MyInterface.implementors(_filter_first_implementor)
        assert 1 == len(filtered_implementor)
        assert [plugnplay.man.iface_implementors.get(MyInterface)[0]] == filtered_implementor
