
from glob import glob
from os.path import join, basename
import sys
from types import FunctionType

from .manager import Manager

__version__ = "0.4"

__all__ = ['Interface', 'Plugin']


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


class PluginMeta(type):

    def __new__(metaclass, classname, bases, attrs):
        new_class = super(PluginMeta, metaclass).__new__(metaclass, classname, \
            bases, attrs)

        new_class_instance = new_class()
        if 'implements' in attrs:
            for interface in attrs['implements']:
                man.add_implementor(interface, new_class_instance)

        return new_class


@classmethod
def implementors(cls):
    return man.implementors(cls)

# Yes, it's not pretty but works ate the same time with
# python2 and python3.
Plugin = PluginMeta('Plugin', (object, ), {})
Interface = InterfaceMeta('Interface', (object, ), {'implementors': implementors})


def set_plugin_dirs(*dirs):
    for d in dirs:
        plugin_dirs.append(d)


def load_plugins(logger=None):
    '''
    The logger is any object with a "debug" method. Compatible
    with a logger as returned by the logging package.
    '''
    for d in plugin_dirs:
        sys.path.append(d)
        py_files = glob(join(d, '*.py'))

        #Remove ".py" for proper importing
        modules = [basename(filename[:-3]) for filename in py_files]
        for mod_name in modules:
            try:
                imported_module = __import__(mod_name, globals=globals(), \
                    locals=locals())
                sys.modules[mod_name] = imported_module
            except:
                if logger:
                    logger.debug("Error loading plugin: {0}".format(mod_name), exc_info=sys.exc_info())
