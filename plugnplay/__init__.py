

from manager import *

__all__ = ['Interface', 'Plugin']


man = Manager()

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
    if attrs.has_key('implements'):
      for interface in attrs['implements']:
        man.add_implementor(interface, new_class_instance)


    return new_class

class Plugin(object):
  __metaclass__ = PluginMeta
