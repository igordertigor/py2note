#!/usr/bin/env python

import re
import sys
import os
import StringIO
import inspect
import contextlib


@contextlib.contextmanager
def stdoutIO(stdout=None):
    """Context manager from
    http://stackoverflow.com/questions/3906232/python-get-the-print-output-in-an-exec-statement
    """
    old = sys.stdout
    if stdout is None:
        stdout = StringIO.StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


def check_start(l):
    """Check if this is the starting marker"""
    m = re.match(
        r"^if\s+__name__\s*==\s*[\"']__main__[\"']\s*:\s*$",
        l)
    if m:
        return True
    else:
        return False


class ProcessedLineList(list):

    def __init__(self, evaluator, *args, **kwargs):
        """This list takes unprocessed code lines and converts them into a list
        of rst strings"""
        self.evaluator = evaluator
        super(ProcessedLineList, self).__init__(*args, **kwargs)
        self.added_text = True
        self.codeblock = ""

    def append(self, l, execute=True):
        """Append a line from the source file to the rst

        :Parameters:
            l:          source file line
            execute:    is this executable code (this is typically assumed, but
                            could not be true if we are dealing with a function
                            definition

        :Note:
            It is important to note, that a single source code line can
            result in 0, 1, or more lines in the output file. Typically, we
            ignore empty lines (so an empty input line will typically result in
            no line being appended). Furthermore, code blocks are prepended by
            an empty line, which can result in multiple lines being appended.
            Finally, the output of executed code is included in the file and
            could therefore in any number of lines.
        """
        # Strip the last newline character
        l = l.rstrip(' \n')

        # Strip initial indent
        if len(l):
            l = l[4:]
        else:
            return

        # Check if we have a comment
        if l[0] == '#':
            if not self.added_text:
                self.flush_codeblock()
                super(ProcessedLineList, self).append('')
            l = l[2:]
            self.added_text = True
            return super(ProcessedLineList, self).append(l)
        else:
            # We have executable code here set it as a doctest
            if self.added_text:
                super(ProcessedLineList, self).append('')

            # Detect continued lines
            l = l.rstrip()
            self.added_text = False
            if l[0] == ' ':
                if execute:
                    self.codeblock += l + '\n'
                return super(ProcessedLineList, self).append('... ' + l)
            else:
                self.flush_codeblock()
                if execute:
                    self.codeblock += l + '\n'
                return super(ProcessedLineList, self).append('>>> ' + l)

    def flush_codeblock(self):
        """If the codeblock contains code, execute it and reinitialize"""
        if len(self.codeblock):
            out = self.evaluator(self.codeblock)
            if len(out):
                super(ProcessedLineList, self).append(out)
        self.codeblock = ""

    def direct_append(self, l):
        """Append a line to the list without processing"""
        super(ProcessedLineList, self).append(l)


class CodeExecutor(dict):

    def __init__(self, fname):
        """This object executes code in the context of a given file

        :Parameters:
            fname:  name of the file that provides the context
        """
        exec 'import sys' in self
        exec 'sys.path.insert(0,".")' in self
        execfile(fname, self)

    def __call__(self, codeblock):
        """Call codeblock and return standard output

        :Parameters:
            codeblock:  a block of executable python code (string)
        """
        with stdoutIO() as s:
            try:
                exec codeblock in self
            except Exception, e:
                sys.stderr.write("Problem executing code:\n")
                sys.stderr.write(l)
                raise e

        return s.getvalue()

    def function_definition(self, fname):
        return inspect.getsource(self[fname]).split('\n')

    def function_documentation(self, fname):
        return self[fname].func_doc.split('\n')

    def function_signature(self, fname):
        f = self[fname]
        s = f.func_name + '(' + ", ".join(f.func_code.co_varnames) + ')'
        return s


def handle_special(l, evl, rst):
    """Check code line l for special values"""
    m = re.search(r'..\sfunc_(code|doc)::\s+(\w+)', l)
    if m is None:
        # Nothing was requested
        return False

    action, fname = m.groups()

    if action == 'code':

        # the user requested a function definition
        code = evl.function_definition(fname)
        for l in code:
            # The function definition should *not* be evaluated!
            rst.append(" "*4 + l + '\n', execute=False)

    elif action == 'doc':

        # The user requested a function documentation
        doc = evl.function_documentation(fname)
        rst.append(' '*4 + '# ' + '**' +
                   evl.function_signature(fname) + '**')
        rst.direct_append("")
        for l in doc:
            if len(l):
                rst.append(" "*4 + "# " + l + '\n')
    return True

if __name__ == '__main__':
    if len(sys.argv) == 1:
        raise ValueError("Needed filename to process")

    ifname = sys.argv[1]
    s = open(ifname, 'r').readlines()

    evl = CodeExecutor(ifname)
    rst = ProcessedLineList(evl)
    relevant_block = False
    for l in s:
        if relevant_block:
            if handle_special(l, evl, rst):
                continue
            rst.append(l)
        else:
            relevant_block = check_start(l)
    rst.flush_codeblock()

    base, ext = os.path.splitext(ifname)
    ofname = base+'.rst'
    print "using output filename", ofname
    f = open(ofname, 'w')
    f.write("\n".join(rst))
    f.close()
