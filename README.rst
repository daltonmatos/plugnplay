Plug n' Play
************

Plug n' PLay (PnP) is a Generic plug-in system inspired by Trac's (http://trac.edgewall.org)
internal component management. With PnP you can turn any program into a pluggable software very easily. 

You just have to define the Interfaces and let others implement them. When your code is running 
you can dynamically retrieve who are the classes that implement a certain Interface, and call 
the specific methods.

A simple example
****************

Think this way: You have e very simple program that just copy files around.

Say you want to check if the copy was OK by calculating the MD5 hash of the 
two files (the original and the copy). You can do this implementing the MD5 check 
inside your main code, that's OK too, but when you need to add another check 
(e.g. calculate the SHA-1 of the files) you will have to modify your code so 
it can call two methods, the MD5 checker and the SHA-1 checker.

With PnP you write only the main piece of the program, the part that does only the copying, 
and the hash checkers you can implement whenever you want, *without* any modification 
to the main code.
 
PnP is roughly a implementation of the Observer pattern (http://en.wikipedia.org/wiki/Observer_pattern). 
 
The code for this example
*************************

Ok, too much talk, now some code. A pseudo-code to the example above would be:

:: 
     
     class CopyListener(Interface): 
        def copy_finished(self, original_file, new_file):
          pass



The main code would be:

::

   PnP.load_plugins("/some/path/with/python/files") # egg files in the future?.
   copy_file(file1, file2)

   # Would return all python classes that 
   # implement CopyListerner interface
   copy_listeners = CopyListener.implementors()

   # Call each of the listeners telling the copy finished
   for listener in copy_listeners:
     listener.copy_finished(file1, file2)


And an example of one such listener would be:

::

   from myproject.interfaces import CopyListener

   class MD5Check(Plugin):
     implements = [CopyListener,]

     def copy_finished(self, file1, file2):
        md5_1 = hash.md5(file1.read()).hexdigest()
        md5_2 = hash.md5(file2.read()).hexdigest()
        if md5_1 is not md5_2:
          # Do something very useful! =)


New in version 0.5.1
********************


Fixes
-----

Fix for issue #14 where plugnplay was getting in the way of the python interperter. Now all modules loaded dinamically by plugnplay are prefixed with "pnp." when added to ``sys.modules``.


New in version 0.5.0
********************

Features
--------

``MyInterface.implementors()`` now can receive a callback function and any number of arguments or keyword arguments. This callback will be called for each implementor, only implementors for which ``callback(implementor)`` returns ``True`` will be included on the resulting filtered list. Any extra arguments passed to ``MyInterface.implementors()`` will be passed through to the callback function. Here is a Simple example:

::

    class MyInterface(plugnplay.Interface):
      pass

    class ImplementorOne(plugnplay.Plugin):
      implements = [MyInterface, ]

    class ImplementorFour(plugnplay.Plugin):
      implements = [MyInterface, ]

    # The filter callback function
    def _filter_implementors(implementor, name_size=15):
      return len(implementor.__class__.__name__) == name_size

    filtered_implementors = MyInterface.implementors(_filter_implementors, name_size=14)
    filtered_implementors_1 = MyInterface.implementors(_filter_implementors, 14)

In this case, both ``filtered_implementors`` and ``filtered_implementors_1`` will be the same: It will be a ``list`` containing an instance of ``ImplementorOne``. Since the example callback has a keyword argument we can also call ``MyInterface.implementors(_filter_implementors)`` and you will have a list returned with an instance of ``ImplementorFour``.

Fixes
-----

Fixed issue #5: Now all plugins are loaded in alphabetical order. The sorting is made among all plugin filenames in all plugin dirs that were added with ``set_plugin_dirs()`` function. As an example, consider this plugindirs structure:

::

    myplugins/
    |-- dir1
    |   |-- aplug.py
    |   `-- cplug.py
    |-- dir2
    |   |-- bplug.py
    |   |-- dplug.py
    |   `-- pplug.py
    `-- aplug.py
    `-- zplug.py

Assuming you added your plugin folders in this order: ``myplugins, myplugins/dir1`` and ``myplugins/dir2``, your plugins will be loaded in this order: ``aplug.py, dir1/aplug.py, dir2/bplug.by, dir1/cplug.py, dir2/dplug.py, dir2/pplug.py, zplug.py``. Not that this **does not** dictates the order of execution of the implementors of a given interface (when you call ``MyInterface.implementors()``).

 * Fix issue #13. Plugnplay should create instances only of classes which implements at least one ``plugnplay.Interface``.

New in version 0.4.2
********************

Small fix when installing plugnplay. The README.rst file was not being included in th final sdist package.

New in version 0.4.1
********************

An important bugfix: There was a problem when the plugins were inside a regular python package. Thanks to Hugo Ribeiro (https://github.com/hugosenari) who reported it. The problem caused the implementors of an interface not to be correctly recorded for later retrieval in the code.
More details: Issue #6 (https://github.com/daltonmatos/plugnplay/issues/6).

New in version 0.4
******************

Since plugnplay version 0.4 you can call your Interface method directly, like this:

:: 

    CopyListener.copy_finished(file1, file2)

This line will call the ``copy_finished`` method of all objects that implement the ``CopyListener`` interface.
This is speciallt iseful when you just want to call all listeners, but do not have any interest on their return value.


Conclusion
**********

Did you like this project? Very nice, so help me write it! Fork the repo and 
send me some pull requests! Or talk to me directly if you have some great ideas to implement!


Thanks,

Dalton Barreto


