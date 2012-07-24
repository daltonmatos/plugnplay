
from glob import glob
from os.path import join, basename, exists, dirname
import sys
from types import FunctionType

from .manager import Manager

__version__ = "0.5.1"

__all__ = ['Interface', 'Plugin']
PNP_SYS_MODULES_PREFIX = 'pnp'

man = Manager()

plugin_dirs = []


def _is_method(o):
    return type(o) is FunctionType


def method_name(method_name):
    def _auto_caller_template(cls, *args, **kwargs):
        for impl in cls.implementors():
            method = getattr(impl, method_name)
            method(*args, **kwargs)
    return _auto_caller_template


def canonical_name(obj):
    return "{0}.{1}".format(obj.__module__, obj.__name__)


class InterfaceMeta(type):
    '''
    Marker for public interfaces
    '''

    def __new__(metaclass, classname, bases, attrs):
        new_class = super(InterfaceMeta, metaclass).__new__(metaclass, classname, bases, attrs)
        for k, v in new_class.__dict__.iteritems():
            if _is_method(v):
                setattr(new_class, k, classmethod(method_name(k)))

        return new_class

    def __eq__(self, other):
        return canonical_name(self) == canonical_name(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(canonical_name(self))


class PluginMeta(type):

    def __new__(metaclass, classname, bases, attrs):
        new_class = super(PluginMeta, metaclass).__new__(metaclass, classname, \
            bases, attrs)

        if 'implements' in attrs:
            new_class_instance = new_class()
            for interface in attrs['implements']:
                man.add_implementor(interface, new_class_instance)

        return new_class


@classmethod
def implementors(cls, filter_callback=None, *args, **kwargs):
    return man.implementors(cls, filter_callback, *args, **kwargs)

# Yes, it's not pretty but works at the same time with
# python2 and python3.
Plugin = PluginMeta('Plugin', (object, ), {})
Interface = InterfaceMeta('Interface', (object, ), {'implementors': implementors})


def set_plugin_dirs(*dirs):
    for d in dirs:
        plugin_dirs.append(d)


def normalize_path(path):
    if path:
        parts = filter(None, path.replace('.', '').split('/'))
        # Prefix all modules imported by plugnplay with a common value
        return '.'.join([PNP_SYS_MODULES_PREFIX] + parts)
    return None


def _is_python_package(path):
    return exists(join(path, '__init__.py'))


def _import_from_python_package(package_module, module):
    imported_module = __import__(package_module, globals=globals(), \
        locals=locals(), fromlist=[module])
    del sys.modules[package_module]
    return imported_module


def _import_directly(mod_name):
    imported_module = __import__(mod_name, globals=globals(), \
            locals=locals())
    del sys.modules[mod_name]
    return imported_module


def _import_module(d, mod_name, logger=None):
    try:
        if _is_python_package(d):
            _mod_name = "{0}.{1}".format(basename(d), mod_name)
            imported_module = _import_from_python_package(_mod_name, mod_name)
        else:
            imported_module = _import_directly(mod_name)

        sys.modules[normalize_path(d) + "." + mod_name] = imported_module
    except:
        if logger:
            logger.debug("Error loading plugin: {0}".format(mod_name), exc_info=sys.exc_info())


def _append_dir(h, key, value):
    '''
     Acumulate one more "value" in a list, if "h" already has "key"
    '''
    if key in h:
        h[key] += [value]
    else:
        h[key] = [value]


def _collect_plugins():
    '''
     Collect all plugin names, in alphabetical order among all plugin dirs.
     Each element is a string with full path (including filename) of a plugin
     to be loaded.
    '''

    file_names = []
    dir_hash = {}
    for d in plugin_dirs:
        files = [basename(f) for f in glob(join(d, '*.py'))]
        file_names += files
        for f in files:
            _append_dir(dir_hash, f, d)

    for f in sorted(set(file_names)):
        for d in dir_hash[f]:
            yield join(d, f)


def load_plugins(logger=None):
    '''
    The logger is any object with a "debug" method. Compatible
    with a logger as returned by the logging package.
    '''

    for _d in _collect_plugins():
        d = dirname(_d)
        if not _is_python_package(d) and d not in sys.path:
            sys.path.insert(0, d)
        elif dirname(d) not in sys.path:
            sys.path.insert(0, dirname(d))

        py_file = basename(_d)

        # Remove ".py" for proper importing
        module = py_file[:-3]
        _import_module(d, module, logger=logger)
