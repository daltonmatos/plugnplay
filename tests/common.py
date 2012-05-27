import unittest

from plugnplay.manager import Manager
from plugnplay import canonical_name, normalize_path


class CommonTests(unittest.TestCase):

    def test_canonical_name(self):
        assert "plugnplay.manager.Manager" == canonical_name(Manager)

    def test_normalize_path(self):
        assert "tmp.a.c.b" == normalize_path('/tmp/a/c/b')
        assert None == normalize_path(None)
