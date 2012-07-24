import unittest

from plugnplay.manager import Manager
from plugnplay import canonical_name, normalize_path


class CommonTests(unittest.TestCase):

    def test_canonical_name(self):
        assert "plugnplay.manager.Manager" == canonical_name(Manager)

    def test_normalize_path(self):
        assert "pnp.tmp.a.c.b" == normalize_path('/tmp/a/c/b')
        assert None == normalize_path(None)

    def test_normalize_path_complex(self):
        self.assertEquals('pnp.some.module.path', normalize_path('/some/module/path'))
        self.assertEquals('pnp.other.module.path', normalize_path('./other/module/path'))
        self.assertEquals('pnp.some.module.path', normalize_path('../..//some//module/path'))
        self.assertEquals('pnp.some.module.path', normalize_path('/some/../module/path/'))
