
Intro 
=====

Plugnlay (PnP) is a generic implementtion of the Observer pattern. With a very easy API you can declare extension points in your code and plugnplay will take care of calling all interested parts when this extension points are used.

To declare an interface and all observers of this interface you do not need to call any *register* method or anything like this. All you need to ensure is that the your obvservers are imported by your python interpreter. Since an observer implementation needs a reference to the interface it's implementing, the interface class is imported automatically.


A note on plugin loading order
******************************

https://github.com/daltonmatos/plugnplay/issues/5


A simple example
****************

Here is a very simple example of what you need to do to declare an interface and implement an observer of this interface.

::

  import plugnplay
  
  class MyInterface(plugnplay.Interface):

    def copy_done(self, orig_file, dest_file):
      pass


This is all you need to declare your interface. Just subclass :py:class:`plugnplay.Interface` and **any** method declared in this class will be part of the interface implementation. 

Now we need to declare an observer for the ``MyInterface`` class.

::

  import plugnplay
  from mymodule import MyInterface

  class MyObserver(plugnplay.Plugin):

    implements = [MyInterface, ]

    def copy_done(self, orig_file, dest_file):
      """
        Here comes the implementation
      """
      pass


And for now on, every time you call ``MyInterface.copy_done()`` passing any two parameters, the method ``copy_done()`` of **all** classes that *observes* the ``MyInterface`` class will be called.
