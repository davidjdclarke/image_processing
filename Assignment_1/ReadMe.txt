Hi There Mr/Mrs TA!

Not sure if you're reading this but here are a few notes on the lab:

1.  The structure that you guys laid out for the code is in my opinion awful!  Why were there multiple files? Why didn't
we just make a single Image Class that could hold all of the details (the type, the file extension, the location etc...)
AND have built in functions .save(), .convert_to_greyscale() etc...

2.  I had issues with the file io.py.  For some reason python was having issues importing this file.  I changed the name
to io_file.py and this resolved the issues.  Not sure if this creates any issues on your end, but I did refractor the project
so hopefully all name changes were applied.  I had no issues running the validate.py file on my machine.

3.  What is the deal with the validate file?  Is that how you check functionality, is it just to check formatting??? Can
you please add something into the lab manual just overviewing what it does.

4.  There was ONE 'flake8' issue I didn't resolve because it was an important piece of code that it had issue with.
(assignment/to_greyscale.py:136:5: E722 do not use bare 'except').  This except clause was set to catch an error with the
os.mknod() command, I think it had an issue that the catch case was too general, but it for what I was using it for it
really was sufficient (in my opinion).

5.  Last, the to_greyscale.py file only can save a copy to the current directory (for some reason it was having issues
creating files in sub-directories).  Since that functionality was not expressed I'll assume that it is ok.  IF, someone
had a use case where they wanted it to be set up like that, then they could just add the to_greyscale.py file to their
PATH and then call it from within the target directory.

Cheers,

David Clarke
ELE 882 (W2021): Assignment 1
January 20, 2021