"""Collection of routines used to read and parse the ovf file.

Part of ovf2vtk.

Hans Fangohr, hans.fangohr@physics.org

"""

import sys

import struct

try:
    import numpy as Numeric
except ImportError:
    print("This program needs Numpy. Please download and install. \
(http://sourceforge.net/projects/numpy).")
    print ("If you are using Numeric, you can use the \
older version 0.1.17 of ovf2vtk.")
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
    """determines if a keyword is in a line and if so, manipulates it to
    ensure correct format"""
    for x in keywords:
        if line[0:len(x)+2] == "# "+x:
            # removes any end of line character and any leading white space
            dic[x] = line[len(x)+2:].strip()
    return dic


def analyze(filename, verbose=0):
    """Takes a file and returns a dictionary of keyword-value pairs"""
    f = open(filename, "rb")
    lines = []
    dic = {}

    while 1:
        line = f.readline()
        # until eof
        if not line:
            break
        if line[0] == "#":
            dic = parse_for_keywords(keywords, line, dic)
            lines.append(line)
    if verbose:
        print("#Analysing {} : Found {} keywords".format(filename,
                                                         len(dic.keys())))
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
    byte = 0
    ans = {}
    while 1:
        line = f.readline()
        byte += len(line)
        lines += 1
        if not line:               # until eof
            print(str.encode('***Reached end of file before encountering data'))
            print("   Cowardly stopping here")
            print("   Some debug info:")
            print("   Have read {} lines and".format(lines))
            print("             {} bytes.".format(byte))
            sys.exit(1)

        if line[0:len(DATAKEYWORD)] == DATAKEYWORD:
            bits = line.split()
            if bits[3] == "Binary":
                ans["type"] = "binary" + bits[4]
            elif bits[3] == "Text":
                ans["type"] = "ascii"
            else:
                print("Data file {} "
                      "appears neither to be a text or"
                      "a binary file.".format(filename))
                print("Cowardly stopping here.")
                sys.exit(1)
            break
    ans["startbyte"] = byte
    ans["startline"] = lines

    f.close()

    if verbose == 1:
        print("Data in {} start in line {} at byte {} and is {}"
              .format(filename, lines, byte, ans["type"]))
    return ans


def read_structured_ascii_oommf_data(fname, byte, dimensions, verbose=0):
    """fname is the filename to read.
    byte is the byte in that file at which the data starts.
    dimensions = 3-tuple (Nx, Ny, Nz) with the numbers of cells in the mesh

    This function will return one vector for each mesh cell combined in a list
    (in the fashion OOMMF stores data, i.e. (from OOMMF userguide)
    'these are ordered with the x index incremented first, then the y
    index, and the z index last.  This is nominally Fortran order, and
    is adopted here because commonly x will be the longest dimension,
    and z the shortest'

    The returned value is a list of 3-tuples."""

    data = open(fname).read()
    datalines = str.split(data[byte:], '\n')
    vectorfield = []

    # read file until end of data.
    for datum in datalines:
        if datum[0:16] == "# End: Data Text":
            break
        if datum[0] == "#":
            print("I found a # in the first column. Complete row is {}"
                  .format(datum))
            print("I only expected '# End: Data Text'.")
            print("cowardly stopping here")
            raise Exception("FileFormatError, See above for more details")

        vector_str = str.split(datum[0:-1])

        vector = [float(a) for a in vector_str]
        if len(vector) != 3:
            print("vector_str= {}".format(vector_str))
            print("vector    = {}".format(vector))
            print("datum = {}".format(datum))
            raise Exception("Oops, vector_str shold have 3 entries")

        vectorfield.append(vector)

    # expected number of data (Nx*Ny*Nz):
    data_exp = Numeric.prod(dimensions)

    # if the length of the vectorfield doesnt equal expected amount of data.
    if (data_exp - len(vectorfield)):
        print("Hmm, expected nx*ny*ny = {} items, but got {} ."
              .format((data_exp), len(vectorfield)))
        print("Cowardly stopping here.")
        raise Exception("FileFormatError, read too many/too few data")

    print("Hint: Reading ASCII-OOMMF file is slow (that could be changed) \
and the files are large. Why not save data as binary?")

    return Numeric.array(vectorfield)


def read_verification_tag(data, floatsize, byte, verbose):
    """acquires the verification tag from a binary4 (floatsize=4) or binary8
    (floatsize=8) file. Returns the position of the file (in bytes) after
    verification tag read."""

    # verification item (at position -1)
    if floatsize == 4:
        verification_tag, = struct.unpack('!f', data[byte:byte+4])
        if verification_tag == 1234567.0:
            if verbose != 0:
                print("verification_tag is okay (=> reading byte order \
correctly)")
            filepos = byte + 4
        else:
            print("The first item in a binary file is meant to be 1234567.0")
            print("but it is not. Instead, I read {}."
                  .format(verification_tag))
            print("Cowardly stopping here.")
            raise AssertionError

    elif floatsize == 8:
        (verification_tag,) = struct.unpack('!d', data[byte:byte+8])
        if verification_tag == 123456789012345.0:
            if verbose != 0:
                print("verification_tag is okay (=> reading byte order \
correctly)")
            filepos = byte + 8
        else:
            print("The first item in a binary file is meant to be \
123456789012345.0")
            print("but it is not. Instead, I read {}."
                  .format(verification_tag))
            print("Cowardly stopping here.")
            raise AssertionError
    else:
        raise Exception("Not Implemented Error. We only do binary files here")

    return filepos


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
        print("ascii -oommf data not supported here")
        raise NotImplementedError
    else:
        print("unknown datatype (expected  'binary4','binary8' [or 'ascii'],\
 but got {}".format(datatype))
        raise Exception

    if verbose:
        print("Expect floats of length {} bytes.".format(floatsize))
        print("Expect to find data in file {} at position {}.".format(fname,
                                                                      byte))
    # now read file
    data = open(fname, 'rb').read()
    filepos = read_verification_tag(data, floatsize, byte, verbose)

    N = Numeric.prod(dimensions)

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

    if N != len(vectorfield):
        print(N, len(vectorfield))
        raise Exception("Oopps. Miscounted - internal error")

    return Numeric.array(vectorfield)


def read_structured_oommf_data(fname, byte, dimensions, datatype, verbose=0):
    """returns the vectorfield for the correspinding datatype"""
    if datatype == 'ascii':
        return read_structured_ascii_oommf_data(fname, byte, dimensions,
                                                verbose)
    elif datatype == 'binary4' or datatype == 'binary8':
        return read_structured_binary_oommf_data(fname, byte, dimensions,
                                                 datatype, verbose)
    else:
        print("expected ascii or binary4 or binar8 for datatype, \
but got {}".format(datatype))
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
        print("Number of cells (Nx={:d},Ny={:d},Nz={:d})"
              .format(dimensions[0], dimensions[1], dimensions[2]))

    # find byte that contains the first item of data
    ovf_data = what_data(infile)

    # read data starting from there
    vf = read_structured_oommf_data(infile, ovf_data["startbyte"], dimensions,
                                    ovf_data["type"], verbose=debug)

    return vf
