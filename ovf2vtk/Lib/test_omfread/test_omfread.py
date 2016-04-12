
from ovf2vtk import omfread

import sys

from StringIO import StringIO

"""all the tests developed for the omfread.py script for ovf2vtk stored in
one place. By Harry Wilson. Last updated 09/04/16"""

# *************************** Global Variables ***************************** #

keywords = ["Title:",
            "Desc: Applied field (T):",
            "Desc: Iteration:",
            "meshtype:", "meshunit:",
            "xbase:", "ybase:", "zbase:",
            "xstepsize:", "ystepsize:", "zstepsize:",
            "xnodes:", "ynodes:", "znodes:",
            "xmin:", "ymin:", "zmin:", "xmax:", "ymax:", "zmax:",
            "boundary:", "valueunit:", "valuemultiplier:",
            "ValueRangeMinMag:", "ValueRangeMaxMag:",
            "End: Head:", "Begin: Data:", "OOMMF:", "Segment count:",
            "Begin: Segme"]

filenames = ['C:\Users\Harry\Documents\Examples\cantedvortex.omf',
             'C:\Users\Harry\Documents\Examples\ellipsoidwrap.omf',
             'C:\Users\Harry\Documents\Examples\h2hleftedge.ohf',
             'C:\Users\Harry\Documents\Examples\yoyoleftedge.ohf']


def test_parse_for_keywords():
    lines = ['# xmax: 4\n', '# xmin: 5\n', 'xbase: 5\n', 'ybase: 3/n', 
             '# boundary: 10', '# valueunit: 8', 'znodes: 8', 'meshunit: 4'
             '# ymax:   34', '# valuemultiplier:  475/n']
    


def test_analyze():
    # This variable will store everything that is sent to the standard output
    # help with code taken from...
    # ...https://wrongsideofmemphis.wordpress.com/2010/03/01/store-standard-
    # output-on-a-variable-in-python/
    result = StringIO()
    sys.stdout = result
    omfread.analyze('C:\Users\Harry\Documents\Examples\cantedvortex.omf',
                    verbose=1)
    result_string = result.getvalue()
    return result_string
