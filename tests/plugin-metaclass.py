# coding: utf-8
import unittest
from plugnplay import Interface, Plugin, Manager
import plugnplay


class SomeInterface(Interface):
    def method(self):
        pass


class SomeInterfaceB(Interface):
    def method_b(self):
        pass


class PluginMetaTest(unittest.TestCase):

    def setUp(self):
        # Refresh the registry
        plugnplay.man = Manager()

    def test_register_class_that_implements_one_or_more_interfaces(self):
        class SomePlugin(Plugin):
            implements = [SomeInterface]

            def method(self):
                pass
        self.assertEquals(1, len(SomeInterface.implementors()))
        self.assertTrue(isinstance(SomeInterface.implementors()[0], SomePlugin))

    def test_register_class_that_implements_more_than_one_interface(self):
        class PluginFoo(Plugin):
            implements = [SomeInterface, SomeInterfaceB]

            # SomeInterface
            def method(self):
                pass

            # SomeInterfaceB
            def method_b(self):
                pass

        self.assertEquals(1, len(SomeInterface.implementors()))
        self.assertEquals(1, len(SomeInterfaceB.implementors()))

        self.assertTrue(isinstance(SomeInterface.implementors()[0], PluginFoo))
        self.assertTrue(isinstance(SomeInterfaceB.implementors()[0], PluginFoo))

    def test_one_interface_implemented_by_two_plugins(self):
        class PlugA(Plugin):
            implements = [SomeInterface]

            def method(self):
                pass

        class PlugB(Plugin):
            implements = [SomeInterface]

            def method(self):
                pass

        self.assertEquals(2, len(SomeInterface.implementors()))
        self.assertTrue(isinstance(SomeInterface.implementors()[0], PlugA))
        self.assertTrue(isinstance(SomeInterface.implementors()[1], PlugB))
