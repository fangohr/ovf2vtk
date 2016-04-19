"""Collection of routines used to read and parse the ovf file.

Part of ovf2vtk.

Hans Fangohr, hans.fangohr@physics.org

"""

import sys

import struct

try:
    import numpy as Numeric
except ImportError:
    print "This program needs Numpy. Please download and install. \
(http://sourceforge.net/projects/numpy)."
    print "If you are using Numeric, you can use the \
older version 0.1.17 of ovf2vtk."
    raise ImportError("Couldn't import Numpy -- cannot proceed.")


__version__ = "$Revision: 1.6 $"

# keyword list from ovf-file:
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
            "End: Head:", "Begin: Data:", "OOMMF:",
            "Segment count:", "Begin: Segme"]


def parse_for_keywords(keywords, line, dic={}):
    for x in keywords:
        if line[0:len(x)+2] == "# "+x:
            dic[x] = line[len(x)+2:]
            # remove end of line character if it is there
            if dic[x][-1] == "\n":
                dic[x] = dic[x][0:-1]
            # remove any leading white space
            while dic[x][0] == " ":
                dic[x] = dic[x][1:]
    return dic


def analyze(filename, verbose=0):
    f = open(filename, "rb")
    lines = []
    dic = {}

    while 1:
        line = f.readline()
        if not line:               # until eof
            break
        if line[0] == "#":
            dic = parse_for_keywords(keywords, line, dic)
            lines.append(line)
    if verbose:
        print "#Analysing", filename, ": Found", len(dic.keys()), "keywords"
    f.close()
    return dic


def what_data(filename, verbose=0):
    DATAKEYWORD = "# Begin: Data"

    """returns a dictionary:
    startbyte = integer (bytes from beginning of file)
    startline = integer (lines from beginning of file)
    type      = 'binary4','binary8','ascii'
    """
    f = open(filename, "rb")
    lines = 0
    bytes = 0
    ans = {}
    while 1:
        line = f.readline()
        bytes = bytes + len(line)
        lines = lines + 1
        if not line:               # until eof
            print "***Reached end of file before encountering data"
            print "   Cowardly stopping here"
            print "   Some debug info:"
            print "   Have read", lines, "lines and"
            print "            ", bytes, "bytes."
            sys.exit(1)

        if line[0:len(DATAKEYWORD)] == DATAKEYWORD:
            bits = line.split()
            if bits[3] == "Binary":
                ans["type"] = "binary" + bits[4]
            else:
                if bits[3] == "Text":
                    ans["type"] = "ascii"
                else:
                    print "Data file", filename, \
                          "appears neither to be a text or"\
                          "a binary file."
                    print "Cowardly stopping here."
                    sys.exit(1)
            break
    ans["startbyte"] = bytes
    ans["startline"] = lines

    f.close()

    if verbose == 1:
        print "Data in", filename, "start in line", lines, "at byte",\
              bytes, "and is", ans["type"]

    return ans


def read_structured_ascii_oommf_data(fname, byte, dimensions, verbose=0):

    """fname is the filemane to read
    byte is the byte in that file at which the data starts
    dimensions = 3-tuple (nx, ny, nz) with the numbers of cells in the mesh

    This function will return one vector for each mesh cell combined in a list
    (in the fashion OOMMF stores data, i.e. (from OOMMF userguide)
    'these are ordered with the x index incremented first, then the y
    index, and the z index last.  This is nominally Fortran order, and
    is adopted here because commonly x will be the longest dimension,
    and z the shortest'

    The returned value is a list of 3-tuples. """

    data = open(fname).read()

    datalines = str.split(data[byte:], '\n')

    vectorfield = []

    for datum in datalines:
        if datum[0:16] == "# End: Data Text":
            break
        if datum[0] == "#":
            print "I found a # in the first column. Complete row is", datum
            print "I only expected '# End: Data Text'."
            print "cowardly stopping here"
            raise Exception("FileFormatError, See above for more details")

        vector_str = str.split(datum[0:-1])

        vector = map(lambda a: float(a), vector_str)
        if len(vector) != 3:
            print "vector_str=", vector_str
            print "vector    =", vector
            print "datum =", datum
            raise Exception("Oops, vector_str shold have 3 entries")

        vectorfield.append(vector)

    # expected number of data:
    data_exp = dimensions[0]*dimensions[1]*dimensions[2]

    if (data_exp - len(vectorfield)):
        print "Hmm, expected nx*ny*ny =", data_exp, "items, but got",\
              len(vectorfield), "."
        print "Cowardly stopping here."
        raise Exception("FileFormatError, read too many/too few data")

    print "Hint: Reading ASCII-OOMMF file is slow (that could be changed) \
and the files are large. Why not save data as binary?"

    return Numeric.array(vectorfield)


def read_structured_binary_oommf_data(fname, byte, dimensions, datatype,
                                      verbose=0):
    """fname is the filename to read
    byte is the byte in that file at which the (binary) data starts
    datatype = 'binary4','binary8','ascii'
    dimensions = 3-tuple (nx, ny, nz) with the numbers of cells in the mesh

    This function will return one tuple for each mesh cell combined in a list
    (in the fashion OOMMF stores data, i.e. (from OOMMF userguide)
    'these are ordered with the x index incremented first, then the y
    index, and the z index last.  This is nominally Fortran order, and
    is adopted here because commonly x will be the longest dimension,
    and z the shortest'

    The returned value is a list of 3-tuples. """

    if datatype == "binary4":
        floatsize = 4
    elif datatype == "binary8":
        floatsize = 8
    elif datatype == "ascii":
        print "ascii -oommf data not supported here"
        raise NotImplementedError("ascii-oommf data not supported here")
    else:
        print "unknow datatype (expected  'binary4','binary8' [or 'ascii'],\
 but got ", datatype
        raise Exception

    if verbose:
        print "Expect floats of length", floatsize, "bytes."
        print "Expect to find data in file", fname, " at position", byte, "."

    # now read file
    data = open(fname, 'rb').read()

    # verification item (at position -1)
    if floatsize == 4:
        verification_tag, = struct.unpack('!f', data[byte:byte+4])

        if verification_tag == 1234567.0:
            if verbose != 0:
                print "verification_tag is okay \
(=> reading byte order correctly)"
            filepos = byte + 4

        else:
            print "The first item in a binary file is meant to be 1234567.0"
            print "but it is not. Instead, I read ", verification_tag, "."
            print "Cowardly stopping here."
            raise AssertionError

    elif floatsize == 8:
        (verification_tag,) = struct.unpack('!d', data[byte:byte+8])

        if verification_tag == 123456789012345.0:
            if verbose != 0:
                print "verification_tag is okay \
(=> reading byte order correctly)"
            filepos = byte + 8
        else:
            print "The first item in a binary file is \
meant to be 123456789012345.0"
            print "but it is not. Instead, I read ", verification_tag, "."
            print "Cowardly stopping here."
            raise AssertionError
    else:
        raise Exception("Not Implemented Error. We only do binary files here")

    Nx, Ny, Nz = dimensions

    N = Nx * Ny * Nz

    # do reading in one go:
    if floatsize == 4:
        vector = struct.unpack('!'+'fff'*N, data[filepos: filepos + 3*4*N])
        filepos += 3*4*N
    elif floatsize == 8:
        vector = struct.unpack('!'+'ddd'*N, data[filepos: filepos + 3*8*N])
        filepos += 3*8*N
    else:
        raise Exception("Hmmm. This should not happen. Reference 1")

    vectorfield = Numeric.reshape(Numeric.array(vector), (N, 3))

    if not N == len(vectorfield):
        print N, len(vectorfield)
        raise Exception("Oopps. Miscounted - internal error")

    return Numeric.array(vectorfield)


def read_structured_oommf_data(fname, byte, dimensions, datatype, verbose=0):
    if datatype == 'ascii':
        return read_structured_ascii_oommf_data(fname, byte, dimensions,
                                                verbose)
    elif datatype == 'binary4' or datatype == 'binary8':
        return read_structured_binary_oommf_data(fname, byte, dimensions,
                                                 datatype, verbose)
    else:
        print "expected ascii or binary4 or binar8 for datatype, \
but got", datatype
        raise Exception("Oopps. Something wrong here!")


def read_structured_omf_file(infile, debug=False):
    """Takes file name and returns vector field of data
    stored in omf-file format in that filename.

    This is the recommended interface.
    """

    # learn about infile
    ovf_run = analyze(infile)

    dimensions = (int(ovf_run["xnodes:"]),
                  int(ovf_run["ynodes:"]),
                  int(ovf_run["znodes:"]))

    if debug:
        print "Number of cells (Nx={:d},Ny={:d},Nz={:d})"\
            .format(dimensions[0], dimensions[1], dimensions[2])

    # find byte that contains the first item of data
    ovf_data = what_data(infile)

    # read data starting from there
    vf = read_structured_oommf_data(infile, ovf_data["startbyte"], dimensions,
                                    ovf_data["type"], verbose=debug)

    return vf
