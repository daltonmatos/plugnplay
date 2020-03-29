

Changelog
=========

0.5.3
*****

Add license file.

0.5.2
*****

Issue [#16](https://github.com/daltonmatos/plugnplay/issues/16) - [Python 3.2] Unable to install 0.5.1 via pip or setup.py
Issue [#18](https://github.com/daltonmatos/plugnplay/issues/18) - Incompatibility with py3k filter() function

0.5.1
*****

Fix for issue #14 where plugnplay was getting in the way of the python interperter. Now all modules loaded dinamically by plugnplay are prefixed with "pnp." when added to ``sys.modules``.


0.5.0
*****


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

Assuming you added your plugin folders in this order: ``myplugins, myplugins/dir1`` and ``myplugins/dir2``, your plugins will be loaded in this order: ``aplug.py, dir1/aplug.py, dir2/bplug.by, dir1/cplug.py, dir2/dplug.py, dir2/pplug.py, zplug.py``. Note that this **does not** dictates the order of execution of the implementors of a given interface (when you call ``MyInterface.implementors()``).

 * Fix issue #13. Plugnplay should create instances only of classes which implements at least one ``plugnplay.Interface``.

0.4.2
*****

Small fix when installing plugnplay. The README.rst file was not being included in the final sdist package.

0.4.1
*****

An important bugfix: There was a problem when the plugins were inside a regular python package. Thanks to Hugo Ribeiro (https://github.com/hugosenari) who reported it. The problem caused the implementors of an interface not to be correctly recorded for later retrieval in the code.
More details: Issue #6 (https://github.com/daltonmatos/plugnplay/issues/6).

0.4.0
*****

Since plugnplay version 0.4 you can call your Interface method directly, like this:

::

    CopyListener.copy_finished(file1, file2)

This line will call the ``copy_finished`` method of all objects that implement the ``CopyListener`` interface.
This is specially useful when you just want to call all observers, but do not have any interest on their return value.
