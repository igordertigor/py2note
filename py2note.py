#!/usr/bin/env python

import re
import sys
import os


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
        l = l.rstrip('\n')

        # Strip initial indent
        if len(l) > 0:
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


if __name__ == '__main__':
    if len(sys.argv) == 1:
        raise ValueError("Needed filename to process")

    ifname = sys.argv[1]
    s = open(ifname, 'r').readlines()

    rst = ProcessedLineList()
    relevant_block = False
    added_text = True
    for l in s:
        if relevant_block:
            rst.append(l)
        else:
            relevant_block = check_start(l)

    base, ext = os.path.splitext(ifname)
    ofname = base+'.rst'
    print "using output filename", ofname
    f = open(ofname, 'w')
    f.write("\n".join(rst))
    f.close()
