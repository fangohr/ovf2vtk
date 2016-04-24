import os

import sys
sys.path.append('..')

import numpy as np

from ovf2vtk import omfread_new as nomf

from ovf2vtk import omfread_original

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
filenames = [os.path.join('..', 'Examples', 'cantedvortex.omf'),
             os.path.join('..', 'Examples', 'ellipsoidwrap.omf'),
             os.path.join('..', 'Examples', 'h2hleftedge.ohf'),
             os.path.join('..', 'Examples', 'yoyoleftedge.ohf'),
             os.path.join('..', 'Examples', 'stdprob3v-reg.omf'),
             os.path.join('..', 'Examples', 'stdproba.omf'),
             os.path.join('..', 'Examples', 'smallDataText.omf'),
             os.path.join('..', 'Examples', 'plateDataText.omf'),
             os.path.join('..', 'Examples', 'spiralDataText.omf')]

filenames_data_types = [b'binary4', b'binary4', b'binary8', b'binary8',
                        b'binary4', b'binary4', b'ascii', b'ascii', b'ascii']

# list of node values for each corresponding filename in 'filenames'
filenames_nodes = [(32, 32, 32), (24, 8, 4), (160, 40, 4), (500, 6, 2),
                   (15, 15, 15), (50, 100, 1), (5, 3, 1), (3, 2, 1),
                   (1, 1, 13)]

# lists giving bytes and lines values to corresponding file in 'filenames'
bytes = [874, 850, 874, 754, 797, 518, 488, 505, 468]
lines = [34, 34, 34, 34, 30, 29, 28, 28, 28]

# ascii filenames and properties
ascii_files = filenames[6:]
ascii_nodes = filenames_nodes[6:]
ascii_bytes = bytes[6:]

# list of files that are completely read before encountering data.
non_files = [os.path.join('..', 'Examples', 'small.omf'),
             os.path.join('..', 'Examples', 'plate.omf'),
             os.path.join('..', 'Examples', 'spiral.omf')]

# lists giving bytes and lines values to corresponding file in 'non_files'
non_bytes = [1205, 580, 804]
non_lines = [47, 37, 44]

# list of files whose data is read but is not ascii or binary format
non_binary_ascii = [os.path.join('..', 'Examples', 'smallData.omf'),
                    os.path.join('..', 'Examples', 'plateData.omf'),
                    os.path.join('..', 'Examples', 'spiralData.omf')]

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
        nomf.parse_for_keywords(keywords, line, act)
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
            act = nomf.analyze(filename, verbose)
            assert type(act) == dict
            # expected result
            exp = omfread_original.analyze(filename, verbose)
            assert act == exp


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
        try:
            nomf.what_data(non_files[i])
            x = 0
        except SystemExit:
            x = 1
        assert x == 1

    # test function determines a file that is not binary or ascii correctly.
    """The what_data() function looks for data type 'Binary' or 'Text'. These
    files have data type 'text' and therefore arent recognised and the function
    should return this fact."""
    for file in non_binary_ascii:
        try:
            nomf.what_data(file)
            x = 0
        except SystemExit:
            x = 1
        assert x == 1

    # test function determines correct data type of files.
    actual_data_types = []
    # test expected effects of setting verbose=1
    for i in range(len(filenames)):
        # check returned object is a dictionary with 3 keys.
        dic = nomf.what_data(filenames[i])
        assert type(dic) == dict
        assert len(dic) == 3
        actual_data_types.append(dic['type'])
    assert actual_data_types == filenames_data_types


def test_read_structured_ascii_oommf_data():
    """the actual function takes as inputs, the filename, its byte at which
    data begins, and its nodes values in a tuple. Returns an array of the
    vectorfield."""

    # test ascii files that don't end data with '# End: Data Text'.
    # These files instead have '# test'.
    # contain same data as equivalent files small/spiral/plate.omf
    # function should recognise incorrect format.
    ascii_test_files = [os.path.join('..', 'Examples', 'smalltest.omf'),
                        os.path.join('..', 'Examples', 'platetest.omf'),
                        os.path.join('..', 'Examples', 'spiraltest.omf')]
    test_bytes = bytes[6:]
    test_nodes = filenames_nodes[6:]
    for i in range(len(ascii_test_files)):
        try:
            nomf.read_structured_ascii_oommf_data(ascii_test_files[i],
                                                  test_bytes[i],
                                                  test_nodes[i])
            x = 0
        except Exception:
            x = 1
        assert x == 1

    # test function detects if a vector has more or less than 3 components
    # use example file created
    example_file = os.path.join('..', 'Examples', 'smalltest2.omf')
    try:
        nomf.read_structured_ascii_oommf_data(example_file, 488, (5, 3, 1))
        x = 0
    except Exception:
        x = 1
    assert x == 1

    # test if too much/too little data is detected and correct output is...
    # ...returned.
    # Files created that have too little/too much data
    unexp_data = [os.path.join('..', 'Examples', 'smallmuchdata.omf'),
                  os.path.join('..', 'Examples', 'platemuchdata.omf'),
                  os.path.join('..', 'Examples', 'spiralmuchdata.omf'),
                  os.path.join('..', 'Examples', 'smalllittledata.omf'),
                  os.path.join('..', 'Examples', 'platelittledata.omf'),
                  os.path.join('..', 'Examples', 'spirallittledata.omf')]
    unexp_bytes = bytes[6:] * 2
    unexp_nodes = filenames_nodes[6:] * 2
    for i in range(len(unexp_data)):
        node_product = unexp_nodes[i][0]*unexp_nodes[i][1]*unexp_nodes[i][2]
        try:
            nomf.read_structured_ascii_oommf_data(unexp_data[i],
                                                  unexp_bytes[i],
                                                  unexp_nodes[i])
            x = 0
        except Exception:
            x = 1
        assert x == 1

    # test expected output if ascii file correct format.
    for i in range(len(ascii_files)):
        node_product = ascii_nodes[i][0]*ascii_nodes[i][1]*ascii_nodes[i][2]
        # expected result
        exp = omfread_original.read_structured_ascii_oommf_data(ascii_files[i],
                                                                ascii_bytes[i],
                                                                ascii_nodes[i])
        # actual result
        act = nomf.read_structured_ascii_oommf_data(ascii_files[i],
                                                    ascii_bytes[i],
                                                    ascii_nodes[i])
        # check ouput is a numpy array of correct length
        assert type(act) == np.ndarray
        assert len(act) == node_product
        # check data identical to original version
        assert act.all() == exp.all()
        # check correct print output


def test_read_structured_binary_oommf_data():
    """the actual function takes, as inputs, the filename; its byte at which
    data begins; its nodes values in a tuple; and the datatype (binary4,
    binary8 or ascii). Returns an array of the vectorfield.
    Utilises 'read_verification_tag' function."""

    # test if ascii file given, exception is raised and print statement sent
    for i in range(len(ascii_files)):
        try:
            nomf.read_structured_binary_oommf_data(ascii_files[i],
                                                   ascii_bytes[i],
                                                   ascii_nodes[i], b'ascii')
            x = 0
        except NotImplementedError:
            x = 1
        assert x == 1

    # test that an unknown data type is detected.
    for i in range(len(filenames)):
        try:
            nomf.read_structured_binary_oommf_data(filenames[i], bytes[i],
                                                   filenames_nodes[i],
                                                   filenames_data_types[i] +
                                                   'unknown')
            x = 0
        except Exception:
            x = 1
        assert x == 1

    # test that incorrect verification tag is detected for binary4 and...
    # ...binary8 files. Uses edited versions of files from 'filenames'...
    # ...which have tags 7.27159209092e+31 and 4.91466545592e+252...
    # ...rather than 1234567.0 and 123456789012345.0 respectively.
    b4_b8_files = [os.path.join('..', 'Examples', 'cantedvortextest.omf'),
                   os.path.join('..', 'Examples', 'ellipsoidwraptest.omf'),
                   os.path.join('..', 'Examples', 'h2hleftedgetest.ohf'),
                   os.path.join('..', 'Examples', 'yoyoleftedgetest.ohf'),
                   os.path.join('..', 'Examples', 'stdprob3v-regtest.omf'),
                   os.path.join('..', 'Examples', 'stdprobatest.omf')]
    for i in range(len(b4_b8_files)):
        try:
            nomf.read_structured_binary_oommf_data(b4_b8_files[i], bytes[i],
                                                   filenames_nodes[i],
                                                   filenames_data_types[i])
            x = 0
        except AssertionError:
            x = 1
        assert x == 1

    # test function output is as expected.
    # actual result
    for i in range(6):
        file = filenames[i]
        byte = bytes[i]
        nodes = filenames_nodes[i]
        data = filenames_data_types[i]
        act = nomf.read_structured_binary_oommf_data(file, byte, nodes, data)
        # check result is a numpy array of correct length and shape
        assert type(act) == np.ndarray
        assert len(act) == filenames_nodes[i][0] * filenames_nodes[i][1] *\
            filenames_nodes[i][2]
        assert [int(dim) for dim in act.shape] == [len(act), 3]
        # check data matches that of of orginal function
        exp = omfread_original.read_structured_binary_oommf_data(file, byte,
                                                                 nodes, data)
        assert act.all() == exp.all()


def test_read_structured_oommf_data():
    """ function takes a file, the byte at which data starts, the nodes of the
    data and the data type, returns a vectorfield."""
    for i in range(len(filenames)):
        file = filenames[i]
        byte = bytes[i]
        nodes = filenames_nodes[i]
        data = filenames_data_types[i]
        # actual result
        act = nomf.read_structured_oommf_data(file, byte, nodes, data)
        # all files retuned as numpy arrays
        assert type(act) == np.ndarray
        assert len(act) == nodes[0] * nodes[1] * nodes[2]
        assert [int(dim) for dim in act.shape] == [len(act), 3]

        # check binary4, binary8 files return expected data values
        if i < 6:
            exp = nomf.read_structured_binary_oommf_data(file, byte, nodes,
                                                         data)
        # check ascii files return expected data values
        else:
            exp = nomf.read_structured_ascii_oommf_data(file, byte, nodes)
        assert exp.all() == act.all()

        # test function detects unexpected datatype
        try:
            nomf.read_structured_oommf_data(file, byte, nodes, data+'unknown')
            x = 0
        except Exception:
            x = 1
        assert x == 1


def test_read_structured_omf_file():
    """Takes a file as an input and returns the vecorfield of data it contains
    """
    for i in range(len(filenames)):
        file = filenames[i]
        byte = bytes[i]
        nodes = filenames_nodes[i]
        data = filenames_data_types[i]
        # actual result
        act = nomf.read_structured_omf_file(file)
        # all files should be retuned as numpy arrays
        assert type(act) == np.ndarray
        assert len(act) == nodes[0] * nodes[1] * nodes[2]
        assert [int(dim) for dim in act.shape] == [len(act), 3]

        # check binary4, binary8 files return expected data values
        if i < 6:
            exp = nomf.read_structured_binary_oommf_data(file, byte, nodes,
                                                         data)
        # check ascii files return expected data values
        else:
            exp = nomf.read_structured_ascii_oommf_data(file, byte, nodes)
        assert exp.all() == act.all()
