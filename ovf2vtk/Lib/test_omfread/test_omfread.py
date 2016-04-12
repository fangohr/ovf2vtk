
from ovf2vtk import omfread

import sys

from StringIO import StringIO

import original_omfread

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
    lines = ['# xmax: 4\n', '# xmin: 5\n', 'xbase: 5\n', 'ybase: 3\n',
             '# boundary: 10', '# valueunit: 8', 'znodes: 8', 'meshunit: 4',
             '# ymax:   34', '# valuemultiplier:  475\n']
    # compute actual result
    act = {}
    for line in lines:
        omfread.parse_for_keywords(keywords, line, act)
    # expected result, dic orders keys in alphabetical order'.
    exp = {'boundary:': '10', 'valuemultiplier:': '475', 'valueunit:': '8',
           'xmax:': '4', 'xmin:': '5', 'ymax:': '34'}
    assert exp == act


def test_analyze():
    verbs = [0, 1]
    # test to see if refactored function will produce same results as original
    for filename in filenames:
        for verb in verbs:
            # actual result
            act = omfread.analyze(filename, verbose=verb)
            # expected result
            exp = original_omfread.analyze(filename, verbose=verb)
            assert act == exp
            # test if print statement occurs when verbose=1
            # help with code taken from...
            # ...https://wrongsideofmemphis.wordpress.com/2010/03/01/
            # store-standard-output-on-a-variable-in-python/
            if verb == 0:
                result = StringIO()
                sys.stdout = result
                omfread.analyze(filename, verbose=0)
                result_string = result.getvalue()
                assert result_string == ''
            if verb == 1:
                result = StringIO()
                sys.stdout = result
                omfread.analyze(filename, verbose=1)
                result_string = result.getvalue()
                assert result_string == "#Analysing {} : Found {} keywords\n"\
                                        .format(filename, len(exp))
