#!/usr/bin/env python

import re
import sys
import os
import StringIO
import inspect


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

    def __init__(self, *args, **kwargs):
        super(ProcessedLineList, self).__init__(*args, **kwargs)
        self.added_text = True

    def append(self, l):
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
                return super(ProcessedLineList, self).append('... ' + l)
            else:
                return super(ProcessedLineList, self).append('>>> ' + l)

    def direct_append(self, l):
        super(ProcessedLineList, self).append(l)


class CodeExecutor(dict):

    def __init__(self, fname):
        execfile(fname, self)

    def __call__(self, l):
        codeOut = StringIO.StringIO()
        codeErr = StringIO.StringIO()

        # Capture output and errors
        sys.stdout = codeOut
        sys.stderr = codeErr

        # Execute code
        exec l[4:] in self

        # Restore stdout and stderr
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        return codeOut.getvalue(), codeErr.getvalue()

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
        return False
    action, fname = m.groups()
    if action == 'code':
        code = evl.function_definition(fname)
        for l in code:
            rst.append(" "*4 + l + '\n')
    elif action == 'doc':
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

    rst = ProcessedLineList()
    evl = CodeExecutor(ifname)
    relevant_block = False
    for l in s:
        if relevant_block:
            if handle_special(l, evl, rst):
                continue
            rst.append(l)
            out, err = evl(l)
            if len(err):
                raise ValueError('Error evaluting code: %s' % (err,))
            if len(out):
                rst.direct_append(out)
        else:
            relevant_block = check_start(l)

    base, ext = os.path.splitext(ifname)
    ofname = base+'.rst'
    print "using output filename", ofname
    f = open(ofname, 'w')
    f.write("\n".join(rst))
    f.close()
