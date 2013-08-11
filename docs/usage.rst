

Defining a Plugnplay Interface
==============================

A plugable interface is just a regular class that has :py:class:`plugnplay.Interface` as its superclass. Any method decalred in this class will be able to be used to call the interface implementors, eg:

::

    class MyInterface(plugnplay.Interface):

      def one_method(self, a, b):
        pass

This defines a plugnplay interface. It means that everytime you call ``MyInterface.one_method(1, 2)``, all implementors of this interface will have this same method called, in sequence.

Note that this declaration is only a marker, the method of the ``MyInterface`` class **will not** be called, it's pure documentational, so whoever looks at this interface knows whitch methods they have to implement.

.. newinversion:: 0.5.3

Any staticmethod will be also included as part of the interface declaration, so if you have an interface like this:

::

    class MyInterface(plugnplay.Interface):

      @staticmethod
      def my_other_method(a, b):
        pass

When calling ``MyInterface.my_other_method(1, 2)`` all the implementors will also be called. This method is specially useful if you happen to use a python IDE and this IDE starts complaining about you passing the wrong number of parameters when calling the interface method.
