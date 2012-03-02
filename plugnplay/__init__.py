
from glob import glob
from os.path import join, basename
import sys

from .manager import *


__version__ = "0.3"

__all__ = ['Interface', 'Plugin']


man = Manager()

plugin_dirs = []


class Interface(object):
    '''
    Marker for public interfaces
    '''

    @classmethod
    def implementors(cls):
        return man.implementors(cls)


class PluginMeta(type):

    def __new__(metaclass, classname, bases, attrs):
        new_class = super(PluginMeta, metaclass).__new__(metaclass, classname, \
            bases, attrs)

        new_class_instance = new_class()
        if 'implements' in attrs:
            for interface in attrs['implements']:
                man.add_implementor(interface, new_class_instance)


        return new_class

# Yes, it's not pretty but works ate the same time with
# python2 and python3.
Plugin = PluginMeta('Plugin', (object, ), {})

def set_plugin_dirs(*dirs):
    for d in dirs:
        plugin_dirs.append(d)


def load_plugins(logger = None):
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
