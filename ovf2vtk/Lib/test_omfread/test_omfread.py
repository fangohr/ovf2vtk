
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

# list of files that are either binary or ascii format
filenames = ['C:\Users\Harry\Documents\Examples\cantedvortex.omf',
             'C:\Users\Harry\Documents\Examples\ellipsoidwrap.omf',
             'C:\Users\Harry\Documents\Examples\h2hleftedge.ohf',
             'C:\Users\Harry\Documents\Examples\yoyoleftedge.ohf',
             'C:\Users\Harry\Documents\Examples\stdprob3v-reg.omf',
             'C:\Users\Harry\Documents\Examples\stdproba.omf',
             'C:\Users\Harry\Documents\Examples\smallDataText.omf',
             'C:\Users\Harry\Documents\Examples\plateDataText.omf',
             'C:\Users\Harry\Documents\Examples\spiralDataText.omf']

filenames_data_types = ['binary4', 'binary4', 'binary8', 'binary8',
                        'binary4', 'binary4', 'ascii', 'ascii', 'ascii']

# list of node values for each corresponding filename in 'filenames'
filenames_nodes = [(32, 32, 32), (24, 8, 4), (160, 40, 4), (500, 6, 2),
                   (15, 15, 15), (50, 100, 1), (5, 3, 1), (3, 2, 1),
                   (1, 1, 13)]

# lists giving bytes and lines values to corresponding file in 'filenames'
bytes = [874, 850, 874, 754, 797, 518, 488, 505, 468]
lines = [34, 34, 34, 34, 30, 29, 28, 28, 28]

# list of files that are completely read before encountering data.
non_files = ['C:\Users\Harry\Documents\Examples\small.omf',
             'C:\Users\Harry\Documents\Examples\plate.omf',
             'C:\Users\Harry\Documents\Examples\spiral.omf']

# lists giving bytes and lines values to corresponding file in 'non_files'
non_bytes = [1205, 580, 804]
non_lines = [47, 37, 44]

# list of files whose data is read but is not ascii or binary format
non_binary_ascii = ['C:\Users\Harry\Documents\Examples\smallData.omf',
                    'C:\Users\Harry\Documents\Examples\plateData.omf',
                    'C:\Users\Harry\Documents\Examples\spiralData.omf']

# possible verbose values
verboses = [0, 1]


def test_parse_for_keywords():
    """parse_for_keywords() determines if there is a keyword in a file line,
    and if so, gets that keyword into the correct format and maps it in a
    dict."""
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
    """analyze() takes a filename as an input and returns a dict of keywords
    within that file."""
    # test to see if refactored function will produce same results as original
    for filename in filenames:
        for verbose in verboses:
            # actual result
            act = omfread.analyze(filename, verbose)
            assert type(act) == dict
            # expected result
            exp = original_omfread.analyze(filename, verbose)
            assert act == exp
            # test if print statement occurs when verbose=1
            # help with code taken from...
            # ...https://wrongsideofmemphis.wordpress.com/2010/03/01/
            # store-standard-output-on-a-variable-in-python/
            if verbose == 0:
                result = StringIO()
                sys.stdout = result
                omfread.analyze(filename, verbose)
                result_string = result.getvalue()
                assert result_string == ''
            if verbose == 1:
                result = StringIO()
                sys.stdout = result
                omfread.analyze(filename, verbose)
                result_string = result.getvalue()
                assert result_string == "#Analysing {} : Found {} keywords\n"\
                                        .format(filename, len(exp))


def test_what_data():
    """what_data() takes a file as an input, reads the file until the data
    begins, and determines whether the file is in ascii, binary4 or binary8
    format, or none of these. If file is read before data begins -> system
    exit."""

    # test if file is completely read before encountering data, test...
    # ...function starts printing statements.
    """these files are completely read before data because the keyword is
    "# Begin: Data" whereas in these files it is written as "Begin: data". If
    this is changed the files are read however none of them are in ascii or
    binary format"""
    for i in range(len(non_files)):
        result = StringIO()
        sys.stdout = result
        try:
            omfread.what_data(non_files[i])
            x = 0
        except SystemExit:
            x = 1
        assert x == 1
        result_string = result.getvalue()
        assert result_string == """***Reached end of file before\
 encountering data
   Cowardly stopping here
   Some debug info:
   Have read {} lines and
             {} bytes.\n""".format(non_lines[i], non_bytes[i])

    # test function determines a file that is not binary or ascii correctly.
    """The what_data() function looks for data type 'Binary' or 'Text'. These
    files have data type 'text' and therefore arent recognised and the function
    should return this fact."""
    for file in non_binary_ascii:
        result = StringIO()
        sys.stdout = result
        try:
            omfread.what_data(file)
            x = 0
        except SystemExit:
            x = 1
        assert x == 1
        result_string = result.getvalue()
        # check it starts printing correct statements.
        assert result_string == """Data file {} appears neither to be a text\
 ora binary file.
Cowardly stopping here.\n""".format(file)

    # test function determines correct data type of files.
    actual_data_types = []
    # test expected effects of setting verbose=1
    for i in range(len(filenames)):
        # check returned object is a dictionary with 3 keys.
        dic = omfread.what_data(filenames[i])
        assert type(dic) == dict
        assert len(dic) == 3
        actual_data_types.append(dic['type'])
        for verbose in verboses:
            result = StringIO()
            sys.stdout = result
            omfread.what_data(filenames[i], verbose)
            result_string = result.getvalue()
            if verbose:
                assert result_string == 'Data in {} start in line {} at\
 byte {} and is {}\n'.format(filenames[i], lines[i], bytes[i],
                             filenames_data_types[i])
            else:
                assert result_string == ''
    assert actual_data_types == filenames_data_types


def test_read_structured_ascii_oommf_data():
    """the actual function takes as inputs, the filename, its byte at which
    data begins, and its nodes values in a tuple. Returns an array of the
    vectorfield."""
    
    
