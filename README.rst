py2note
=======

Convert python comments to rst notes file.

If you do data analysis with python, you often want to write extensive notes
about the what and why of the steps that you're following. Typically, this kind
of explanations would go into comments in the python file. An alternative way
to deal with this (and often used to document code) is `ipython notebook
<http://ipython.org/>`_. Although I find ipython an incredibly valuable tool, I
hardly ever use it's notebook feature. It somehow doesn't conform with my
workflow. I typically try things in ipython and then write a proper analysis in
a python file. In many cases, I have a separate latex or rst file to document
what I'm doing in the python file. This is a bit annoying and I would like to
keep both of them in the same file. Of course, this could be resolved with
python comments, but those are not always nicely readable. py2note resolves
this problem and allows you to convert python files to rst-notes.

Calling py2note
---------------

If you have py2note executable and in your path, you can call it as::

    py2note <myanalysis.py>

From this, py2note will create a file myanalysis.rst that you can use with
typical rst-aware software. When converting, your analysis will be set as
docstrings (although the results are not printed, yet). So you could (with a
lot of errors) even run the rst-file itself.

py2note will not convert the entire file into rst. It will rather search for a
line of the form::

    if __name__ == "__main__":

and only treat the parts of the file that come ofter this statement. This way,
you can hide the implementation from the actual final analysis.

Example
-------

In the folder example, we have a little code example.

TODO
----

- other starting sequences
- functionality to include function documentations from before the main block
