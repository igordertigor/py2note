Example usage of py2note
========================

This file illustrates the use of py2note with a simple code example.
We can write extensive documentation in comments here in the file and
use any rst-directive that we need. For example, we can use the math
directive,

.. math::
      F(x) = \int_{-\infty}^x f(x) \,\mathrm{d}x

to create formulas. In contrast to the way they look in the code, these
formulas are set using the respective rst-processor and can look quite
fine. Yet, we can also write code

>>> x = 2.
>>> y = x + 3

Finally, we can obviously use any function that we defined before the
starting statement, such as

>>> an_ignored_function()

Furthermore, continued lines will be recognized and printed as continued
docstrings

>>> for i in xrange(5):
...     print i

Now, one other point is that in some cases, we want to include one of the
above functions in the resulting rst-document. This can be done by using
the rst-autodoc functionality, but requires sphinx as a translator and is
therefore not illustrated here.

You can now run py2note on this file to generate an rst file and
afterwards, you can for example convert the rst file to a pdf using
rst2pdf::

  rst2pdf example.rst