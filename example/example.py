#!/usr/bin/env python


def myfunction(x):
    """We can have a docstring here"""
    return x**2

if __name__ == "__main__":
    # Example usage of py2note
    # ========================
    #
    # This file illustrates the use of py2note with a simple code example.
    # We can write extensive documentation in comments here in the file and
    # use any rst-directive that we need. For example, we can use the math
    # directive,
    #
    # .. math::
    #       F(x) = \int_{-\infty}^x f(x) \,\mathrm{d}x
    #
    # to create formulas. In contrast to the way they look in the code, these
    # formulas are set using the respective rst-processor and can look quite
    # fine. Yet, we can also write code

    x = 2.
    y = x + 3

    # Finally, we can obviously use any function that we defined before the
    # starting statement, such as

    print myfunction(x)

    # Furthermore, continued lines will be recognized and printed as continued
    # docstrings

    for i in xrange(5):
        print i

    # Now, one other point is that in some cases, we want to include one of the
    # above functions in the resulting rst-document. For example, we might
    # feel that knowing about myfunction is really crucial, we might want to
    # include its docstring:
    #
    # .. func_doc:: myfunction
    #
    # In some cases, it isn't so much the docstring, but it's rather the
    # implementation that matters. In that case, we can also include the
    # source code:
    #
    # .. func_code:: myfunction
    #
    # You can now run py2note on this file to generate an rst file and
    # afterwards, you can for example convert the rst file to a pdf using
    # rst2pdf::
    #
    #   rst2pdf example.rst
