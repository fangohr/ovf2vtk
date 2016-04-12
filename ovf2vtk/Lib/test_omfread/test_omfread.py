
from ovf2vtk import omfread

import sys

from StringIO import StringIO

"""all the tests developed for the omfread.py script for ovf2vtk stored in
one place. By Harry Wilson. Last updated 09/04/16"""

# *************************** Global Variables ***************************** #


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
