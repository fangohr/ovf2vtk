#!/usr/bin/env python
"""

This file is executed from ../setup.py only.

Calculate cumulative version from Revision strings.

Copyright 2000 Pearu Peterson all rights reserved,
Pearu Peterson <pearu@ioc.ee>
Minor modification (added explanatory comment and wrapped code into function)
by Hans Fangohr 2005

Permission to use, modify, and distribute this software is given under the
terms of the LGPL.  See http://www.fsf.org

NO WARRANTY IS EXPRESSED OR IMPLIED.  USE AT YOUR OWN RISK.
$Revision: 1.7 $
$Date: 2005-07-13 13:53:25 $
Pearu Peterson


"""

import os

import fileinput

import re


def get_revision_version():
    """goes through all files in lib and sums the last number in the
    CVS revision strings."""
    files = []
    print("Considering these files for release tag:")
    for d in ['Lib', 'bin', ]:
        for f in os.listdir(d):
            if f[-3:] == '.py' or f == 'ovf2vtk':
                fn = os.path.join(d, f)
                if os.path.exists(fn):
                    files.append(fn)
                    print("  ... {} ...".format(fn))
                else:
                    print('File {} does not exists. Skipping.'.format(fn))

    revision_version = 0
    for l in fileinput.input(files):
        m = re.match(r'.*?\$Re[v]ision:\s*\d+[.](?P<rev>\d+)\s*\$', l)
        if m:
            revision_version = revision_version + eval(m.group('rev'))
            fileinput.nextfile()

    print("Done. Version is %s".format(str(revision_version)))

    return revision_version
