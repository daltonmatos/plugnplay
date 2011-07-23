
from glob import glob
from os.path import join, basename
import sys

from .manager import *


__version__ = "0.2"

__all__ = ['Interface', 'Plugin']


man = Manager()

plugin_dirs = []

'''
  Marker for public interfaces
'''
class Interface(object):
  
  @classmethod
  def implementors(klass):
    return man.implementors(klass)


class PluginMeta(type):
  
  def __new__(metaclass, classname, bases, attrs):
    new_class = super(PluginMeta, metaclass).__new__(metaclass, classname,\
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
  for dir in dirs:
    plugin_dirs.append(dir)
  
def load_plugins():
  for dir in plugin_dirs:
    sys.path.append(dir)
    py_files = glob(join(dir, '*.py'))
    
    #Remove ".py" for proper importing
    modules = [basename(file[:-3]) for file in py_files]
    for mod_name in modules:
      imported_module = __import__(mod_name, globals=globals(),\
          locals=locals())
      sys.modules[mod_name] = imported_module
