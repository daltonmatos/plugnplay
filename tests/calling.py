import unittest
import plugnplay
from mock import Mock


class SomeIface(plugnplay.Interface):

    def one_method(self, p1, p2):
        pass


class CallTest(unittest.TestCase):

    def test_call_implementors(self):
        plugin_mock = Mock()
        plugnplay.man.add_implementor(SomeIface, plugin_mock)
        SomeIface.one_method(1, 2)
        self.assertEquals(1, plugin_mock.one_method.call_count)
        plugin_mock.one_method.assert_called_with(1, 2)
