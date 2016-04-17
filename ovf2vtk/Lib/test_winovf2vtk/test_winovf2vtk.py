
import subprocess

import ovf2vtk

from ovf2vtk import winovf2vtk

"""all the tests developed for the winovf2vtk.py script for ovf2vtk stored in
one place. By Harry Wilson. Last updated 15/04/16"""

# ****************************** Global Variables ***************************

# list of keys that can be implemented in command line
keys = ['-V', '--version', '-v', '--verbose', '-h', '--help',
        '--surface-effects', '--datascale=0.0', '--posscale=0.0', '-b',
        '--binary', '-t', '--text', '--ascii', '--add xy', '--add xy',
        '--add yz', '--add xz', '--add Mx', '--add My', '--add Mz',
        '--add divrot', '--add Ms', '--add all', '-a xy', '-a yz', '-a xz',
        '-a Mx', '-a My', '-a Mz', '-a divrot', '-a Ms', '-a all']

infiles = ['C:\Users\Harry\Documents\Examples\cantedvortex.omf',
           'C:\Users\Harry\Documents\Examples\ellipsoidwrap.omf',
           'C:\Users\Harry\Documents\Examples\stdprob3v-reg.omf',
           'C:\Users\Harry\Documents\Examples\stdproba.omf',
           'C:\Users\Harry\Documents\Examples\h2hleftedge.ohf',
           'C:\Users\Harry\Documents\Examples\yoyoleftedge.ohf',
           'C:\Users\Harry\Documents\Examples\smallDataText.omf',
           'C:\Users\Harry\Documents\Examples\plateDataText.omf',
           'C:\Users\Harry\Documents\Examples\spiralDataText.omf']

outfiles = ['C:\Users\Harry\Documents\Examples\cantedvortex.vtk',
            'C:\Users\Harry\Documents\Examples\ellipsoidwrap.vtk',
            'C:\Users\Harry\Documents\Examples\h2hleftedge.vtk',
            'C:\Users\Harry\Documents\Examples\yoyoleftedge.vtk',
            'C:\Users\Harry\Documents\Examples\stdprob3v-reg.vtk',
            'C:\Users\Harry\Documents\Examples\stdproba.vtk',
            'C:\Users\Harry\Documents\Examples\smallDataText.vtk',
            'C:\Users\Harry\Documents\Examples\plateDataText.vtk',
            'C:\Users\Harry\Documents\Examples\spiralDataText.vtk']

# product of Nx,Ny,Nz for each corresponding infile
cells = [32768, 768, 3375, 5000, 25600, 6000, 15, 6, 13]

# % of cells filled for each corresponding infile
cells_filled = ['100.00', '57.29', '100.00', '99.60', '100.00', '100.00',
                '100.00', '100.00', '100.00']

# scale for each corresponding infile
scale = ['1.000000', '1.000000', '1.000000', '1.000000', '349370.681891',
         '270851.375948', '1.500000', '21.954498', '1.000000']

# nodes for each corresponding infile
nodes = [(32, 32, 32), (24, 8, 4), (15, 15, 15), (50, 100, 1),
         (160, 40, 4), (500, 6, 2), (5, 3, 1), (3, 2, 1), (1, 1, 13)]

# floatsize for the first six infiles (binary files)
floatsizes = [4, 4, 4, 4, 8, 8]

# list giving startbyte values to corresponding file in 'infiles'
bytes = [874, 850, 797, 518, 874, 754, 488, 505, 468]

V_version_str = "This is version {}.".format(ovf2vtk.__version__)

v_verbose_str = ["running in verbose mode", """infile  =  {}
outfile =  {}
additions=  [('{}', '')]
options =  {}
datascale= 0.0
posscale= 0.0""", "Number of cells (Nx={},Ny={},Nz={})",
                 """Expect floats of length {} bytes.
Expect to find data in file {}  at position {} .
verification_tag is okay (=> reading byte order correctly)"""]

ascii_str = ["Hint: Reading ASCII-OOMMF file is slow (that could be changed) \
and the files are large. Why not save data as binary?"]

banner_str = "running in verbose mode\n" + 70 * "-" + "\novf2vtk --- \
converting ovf files to vtk files" + "\n" + """Hans Fangohr, Richard Boardman,\
 University of Southampton\n""" + 70 * "-"

in_out_str = """({}% of {} cells filled)
Will scale data down by {}
saving file ({})
finished conversion (execution time"""

vtk_str = """VtkData.__init__.skipping:
\tstriping header string to a length =255"""

# *********************************** Tests *********************************


def test_winovf2vtk_no_inputs():
    """test that the expected docstring is returned with the execution of...
    the program only, and no added keys or files to convert.
    useful code found at http://stackoverflow.com/questions/4760215/...
    running-shell-command-from-python-and-capturing-the-output"""
    # compute actual result
    command = 'python.exe C:\Users\Harry\Anaconda\Scripts\winovf2vtk.py'
    p = subprocess.Popen(command, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    doc = p.stdout.readlines()
    # remove '\r\n' characters
    new_doc = []
    for i in range(len(doc)):
        line = doc[i].strip('\r\n')
        new_doc.append(line)
    # compute expected result
    # zero parameters, therefore error message
    exp = winovf2vtk.__doc__ + "\nERROR: An input file (and an output file \
need to be specified)."
    exp = exp.splitlines()
    assert new_doc == exp


def test_winovf2vtk_keys_no_parameters():
    """test that the expected output is displayed when the command line
    includes a key, but no files to convert."""
    for val in range(len(keys)):
        # compute actual result
        command = "python.exe C:\Users\Harry\Anaconda\Scripts\
\winovf2vtk.py" + " {}".format(keys[val])
        p = subprocess.Popen(command, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        doc = p.stdout.readlines()
        # remove '\r\n' characters
        new_doc = []
        for i in range(len(doc)):
            line = doc[i].strip('\r\n')
            new_doc.append(line)
        # compute expected result for each key separately
        if val < 2:
            exp = ["This is version {}.".format(ovf2vtk.__version__)]
        elif 1 < val < 4:
            exp = "running in verbose mode\n" + winovf2vtk.__doc__ + "\nERROR:\
 An input file (and an output file need to be specified)."
            exp = exp.splitlines()
        elif 3 < val < 6:
            exp = winovf2vtk.__doc__ + "\n"
            exp = exp.splitlines()
        elif val > 5:
            exp = winovf2vtk.__doc__ + "\nERROR: An input file (and an output \
file need to be specified)."
            exp = exp.splitlines()
        assert exp == new_doc


def test_winovf2vtk_keys_one_parameter():
    """test that the expected output is displayed when the command line
    includes a key and one parameter but no files to convert."""
    for val in range(len(keys)):
        # compute actual result with one input file
        command = "python.exe C:\Users\Harry\Anaconda\Scripts\
\winovf2vtk.py" + " {} cantedvortex.omf".format(keys[val])
        p = subprocess.Popen(command, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        doc = p.stdout.readlines()
        # remove '\r\n' characters
        new_doc = []
        for i in range(len(doc)):
            line = doc[i].strip('\r\n')
            new_doc.append(line)
        # compute expected result for each key separately
        if val < 2:
            exp = ["This is version {}.".format(ovf2vtk.__version__)]
        elif 1 < val < 4:
            exp = "running in verbose mode\n" + winovf2vtk.__doc__ + \
                """\nERROR: An input file AND an output file need to \
be specified.
specify output file"""
            exp = exp.splitlines()
        elif 3 < val < 6:
            exp = winovf2vtk.__doc__ + "\n"
            exp = exp.splitlines()
        elif val > 5:
            exp = winovf2vtk.__doc__ + """\nERROR: An input file AND an\
 output file need to be specified.
specify output file"""
            exp = exp.splitlines()
        assert exp == new_doc


def test_winovf2vtk_no_keys_two_parameters():
    """test that the expected output is displayed when the command line
    includes two parameters: the infile and outfile"""

    # test two parameters with no keys
    for i in range(len(infiles)):
        # actual result
        command = "python.exe C:\Users\Harry\Anaconda\Scripts\
\winovf2vtk.py" + " {} {}".format(infiles[i], outfiles[i])
        p = subprocess.Popen(command, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        doc = p.stdout.readlines()
        # remove '\r\n' characters
        new_doc = []
        for j in range(len(doc)):
            line = doc[j].strip('\r\n')
            new_doc.append(line)
        # expected result
        # binary4 and binary8 files
        if i < 6:
            exp = 70 * "-" + \
                "\novf2vtk --- converting ovf files to vtk files" + "\n" + \
                """Hans Fangohr, Richard Boardman, University of \
Southampton\n""" + 70 * "-" + "\n" + \
                """({}% of {} cells filled)
Will scale data down by {}
saving file ({})
finished conversion (execution time
VtkData.__init__.skipping:
\tstriping header string to a length =255""".format(cells_filled[i], cells[i],
                                                    scale[i], outfiles[i])
            exp = exp.splitlines()

        # ascii files
        elif i > 5:
            exp = 70 * "-" + \
                "\novf2vtk --- converting ovf files to vtk files" + "\n" + \
                """Hans Fangohr, Richard Boardman, University of \
Southampton\n""" + 70 * "-" + "\n" + \
                """Hint: Reading ASCII-OOMMF file is slow (that could be\
 changed) and the files are large. Why not save data as binary?
({}% of {} cells filled)
Will scale data down by {}
saving file ({})
finished conversion (execution time
VtkData.__init__.skipping:
\tstriping header string to a length =255""".format(cells_filled[i], cells[i],
                                                    scale[i], outfiles[i])
            exp = exp.splitlines()
        # can't predict execution time
        new_doc[-3] = new_doc[-3][:35]
        assert exp == new_doc


def test_winovf2vtk_keys_two_parameters():
    """test that the expected output is displayed when the command line
    includes a key and two parameters: the infile and outfile"""
    for i in range(len(keys)):
        for j in range(len(infiles)):
            # actual result
            command = "python.exe C:\Users\Harry\Anaconda\Scripts\
\winovf2vtk.py" + " {} {} {}".format(keys[i], infiles[j], outfiles[j])
            p = subprocess.Popen(command, stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT)
            doc = p.stdout.readlines()
            str_doc = str(doc)

            # compute expected results
            # '-V file.omf file.vtk'
            if i < 2:
                assert "This is version {}.".format(ovf2vtk.__version__) in \
                    str_doc

            # '-v asciifile.omf asciifile.vtk'
            if 1 < i < 4 and j < 6:
                options = {keys[i]: None}
                assert banner_str in str_doc
                assert v_verbose_str[1].format(infiles[j], outfiles[j],
                                               keys[i], options) in str_doc
                assert v_verbose_str[2].format(nodes[j][0], nodes[j][1],
                                               nodes[j][2]) in str_doc
                assert v_verbose_str[3] in str_doc
                assert in_out_str in str_doc
                assert vtk_str in str_doc
                exp = "running in verbose mode\n" + 70 * "-" + \
                    "\novf2vtk --- converting ovf files to vtk files" + \
                    "\n" + """Hans Fangohr, Richard Boardman, University of \
Southampton\n""" + 70 * "-" + "\n" + \
                    """infile  =  {}
outfile =  {}
additions=  [('{}', '')]
options =  {}
datascale= 0.0
posscale= 0.0
Number of cells (Nx={},Ny={},Nz={})
Expect floats of length {} bytes.
Expect to find data in file {}  at position {} .
verification_tag is okay (=> reading byte order correctly)
({}% of {} cells filled)
Will scale data down by {}
saving file ({})
finished conversion (execution time
VtkData.__init__.skipping:
\tstriping header string to a length =255""".format(infiles[j], outfiles[j],
                                                    keys[i], options,
                                                    nodes[j][0], nodes[j][1],
                                                    nodes[j][2], floatsizes[j],
                                                    infiles[j], bytes[j],
                                                    cells_filled[j], cells[j],
                                                    scale[j], outfiles[j])
                exp = exp.splitlines()
                # can't predict execution time
                new_doc[-3] = new_doc[-3][:35]
                assert exp == new_doc

            # '-v asciifile.omf asciifile.vtk'
            if i < 1 < 4 and j > 6:
                options = {keys[i]: None}
                exp = "running in verbose mode\n" + 70 * "-" + \
                    "\novf2vtk --- converting ovf files to vtk files" + \
                    "\n" + """Hans Fangohr, Richard Boardman, University of \
Southampton\n""" + 70 * "-" + "\n" + \
                    """infile  =  {}
outfile =  {}
additions=  [('{}', '')]
options =  {}
datascale= 0.0
posscale= 0.0
Number of cells (Nx={},Ny={},Nz={})
Hint: Reading ASCII-OOMMF file is slow (that could be changed) and the files \
are large. Why not save data as binary?
({}% of {} cells filled)
Will scale data down by {}
saving file ({})
finished conversion (execution time
VtkData.__init__.skipping:
\tstriping header string to a length =255""".format(infiles[j], outfiles[j],
                                                    keys[i], options,
                                                    nodes[j][0], nodes[j][1],
                                                    nodes[j][2],
                                                    cells_filled[j], cells[j],
                                                    scale[j], outfiles[j])
                exp = exp.splitlines()
                # can't predict execution time
                new_doc[-3] = new_doc[-3][:35]
                assert exp == new_doc
            if 3 < i < 6:
                exp = winovf2vtk.__doc__ + "\n"
                exp = exp.splitlines()
                assert exp == new_doc
