#!/usr/bin/env python

import re
import sys
import os

if len(sys.argv) == 1:
    raise ValueError, "Needed filename to process"

ifname = sys.argv[1]
s = open(ifname, 'r').readlines()

rst = []
relevant_block = False
added_text = True
for l in s:
    if not relevant_block:
        m = re.match(
            r"^if\s+__name__\s*==\s*[\"']__main__[\"']\s*:\s*$",
            l)
        if m:
            relevant_block = True
        continue

    # Strip the last newline
    l = l.rstrip("\n")

    # First strip indent
    if len(l) > 0:
        l = l[4:]
    else:
        continue

    # Now check if we are have a comment:
    if l[0] == '#':
        if not added_text:
            rst.append('')
        l = l[2:]
        rst.append(l)
        added_text = True
    else:
        # This is executable code. We want to set it as a doctest.

        # First important point: Check if we come from a textblock
        if added_text:
            rst.append("")

        # Important for this: Detect continued lines
        l = l.rstrip()
        if l[0] == " ":
            rst.append("... " + l)
        else:
            rst.append(">>> " + l)
        added_text = False

base,ext = os.path.splitext(ifname)
ofname = base+'.rst'
print "using output filename", ofname
f = open(ofname, 'w')
f.write("\n".join(rst))
f.close()
