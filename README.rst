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


And an example of one such observer would be:

::

   from myproject.interfaces import CopyListener

   class MD5Check(Plugin):
     implements = [CopyListener,]

     def copy_finished(self, file1, file2):
        md5_1 = hash.md5(file1.read()).hexdigest()
        md5_2 = hash.md5(file2.read()).hexdigest()
        if md5_1 is not md5_2:
          # Do something very useful! =)


Conclusion
**********

Did you like this project? Very nice, so help me write it! Fork the repo and 
send me some pull requests! Or talk to me directly if you have some great ideas to implement!


Thanks,

Dalton Barreto


