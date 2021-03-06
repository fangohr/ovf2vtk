import os

import sys
sys.path.append('..')

import subprocess

import ovf2vtk

# set version variqble
version = ovf2vtk.__version__.__version__

from ovf2vtk import winovf2vtk as win


"""all the tests developed for the winovf2vtk.py script for ovf2vtk stored in
one place. By Harry Wilson. Last updated 15/04/16"""

# ****************************** Global Variables ***************************

# check whether Python 2 or Python 3:
sysvers = sys.version_info[0]

# list of keys that can be implemented in command line
keys = ['-V', '--version', '-v', '--verbose', '-h', '--help',
        '--surface-effects', '--datascale=0.0', '--posscale=0.0', '-b',
        '--binary', '-t', '--text', '--ascii', '--add xy', '--add xy',
        '--add yz', '--add xz', '--add Mx', '--add My', '--add Mz',
        '--add divrot', '--add Ms', '--add all', '-a xy', '-a yz', '-a xz',
        '-a Mx', '-a My', '-a Mz', '-a divrot', '-a Ms', '-a all']

infiles = [os.path.join('..', 'Examples', 'cantedvortex.omf'),
           os.path.join('..', 'Examples', 'ellipsoidwrap.omf'),
           os.path.join('..', 'Examples', 'stdprob3v-reg.omf'),
           os.path.join('..', 'Examples', 'stdproba.omf'),
           os.path.join('..', 'Examples', 'h2hleftedge.ohf'),
           os.path.join('..', 'Examples', 'yoyoleftedge.ohf'),
           os.path.join('..', 'Examples', 'smallDataText.omf'),
           os.path.join('..', 'Examples', 'plateDataText.omf'),
           os.path.join('..', 'Examples', 'spiralDataText.omf')]

outfiles = [os.path.join('..', 'Examples', 'cantedvortex.vtk'),
            os.path.join('..', 'Examples', 'ellipsoidwrap.vtk'),
            os.path.join('..', 'Examples', 'h2hleftedge.vtk'),
            os.path.join('..', 'Examples', 'yoyoleftedge.vtk'),
            os.path.join('..', 'Examples', 'stdprob3v-reg.vtk'),
            os.path.join('..', 'Examples', 'stdproba.vtk'),
            os.path.join('..', 'Examples', 'smallDataText.vtk'),
            os.path.join('..', 'Examples', 'plateDataText.vtk'),
            os.path.join('..', 'Examples', 'spiralDataText.vtk')]

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

# ********************* Command line key print statements ******************* #
V_version_str = "This is version {}.".format(version)

v_verbose_str = ["running in verbose mode", "infile =", "outfile =",
                 "args =", "options =", "datascale = 0.0", "posscale = 0.0",
                 "Number of cells", "Expect floats of length",
                 "Expect to find data in file",
                 "verification_tag is okay (=> reading byte order correctly)"]

ascii_str = "Hint: Reading ASCII-OOMMF file is slow (that could be changed) \
and the files are large. Why not save data as binary?"

banner_str = [70 * "-", "ovf2vtk --- converting ovf files to vtk files",
              "Hans Fangohr, Richard Boardman, University of Southampton"]

in_out_str = ["cells filled", "Will scale data down by", "saving file",
              "finished conversion (execution time"]

add_str = "working on"

# *********************************** Tests *********************************


def test_winovf2vtk_no_inputs():
    """test that the expected docstring is returned with the execution of...
    the program only, and no added keys or files to convert.
    useful code found at http://stackoverflow.com/questions/4760215/...
    running-shell-command-from-python-and-capturing-the-output"""
    # compute actual result
    command = 'python ' + os.path.join('..', 'winovf2vtk.py')
    p = subprocess.Popen(command, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, shell=True)
    doc = p.stdout.readlines()
    # remove '\r\n' characters
    new_doc = []
    for i in range(len(doc)):
        line = doc[i].strip(b'\r\n')
        # remove byte character 'b' from beginning of line.
        new_doc.append(line)
    # compute expected result
    # zero parameters, therefore error message
    exp = win.__doc__ + "\nERROR: An input file (and an \
output file need to be specified)."
    exp = exp.splitlines()

    # decode data stored in bytes if using Python 3, then compare lists.
    if sysvers == 3:
        act = []
        for line in new_doc:
            act.append(line.decode('ascii'))
        assert exp == act
    else:
        assert exp == new_doc


def test_winovf2vtk_keys_no_parameters():
    """test that the expected output is displayed when the command line
    includes a key, but no files to convert."""
    for val in range(len(keys)):
        # compute actual result
        command = 'python ' + os.path.join('..', 'winovf2vtk.py') + \
                  " {}".format(keys[val])
        p = subprocess.Popen(command, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, shell=True)
        doc = p.stdout.readlines()
        # remove '\r\n' characters
        new_doc = []
        for i in range(len(doc)):
            line = doc[i].strip(b'\r\n')
            new_doc.append(line)
        # compute expected result for each key separately
        if val < 2:
            exp = ["This is version {}.".format(version)]
        elif 1 < val < 4:
            exp = "running in verbose mode\n" + win.__doc__ + "\nERROR:\
 An input file (and an output file need to be specified)."
            exp = exp.splitlines()
        elif 3 < val < 6:
            exp = win.__doc__ + "\n"
            exp = exp.splitlines()
        else:
            exp = win.__doc__ + "\nERROR: An input file (and an output \
file need to be specified)."
            exp = exp.splitlines()

        # decode data stored in bytes if using Python 3, then compare lists.
        if sysvers == 3:
            act = []
            for line in new_doc:
                act.append(line.decode('ascii'))
            assert exp == act
        else:
            assert exp == new_doc


def test_winovf2vtk_keys_one_parameter():
    """test that the expected output is displayed when the command line
    includes a key and one parameter but no files to convert."""
    for val in range(len(keys)):
        # compute actual result with one input file
        command = 'python ' + os.path.join('..', 'winovf2vtk.py') + \
            " {} cantedvortex.omf".format(keys[val])
        p = subprocess.Popen(command, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, shell=True)
        doc = p.stdout.readlines()
        # remove '\r\n' characters
        new_doc = []
        for i in range(len(doc)):
            line = doc[i].strip(b'\r\n')
            new_doc.append(line)
        # compute expected result for each key separately
        if val < 2:
            exp = ["This is version {}.".format(version)]
        elif 1 < val < 4:
            exp = "running in verbose mode\n" + win.__doc__ + \
                """\nERROR: An input file AND an output file need to \
be specified.
specify output file"""
            exp = exp.splitlines()
        elif 3 < val < 6:
            exp = win.__doc__ + "\n"
            exp = exp.splitlines()
        else:
            exp = win.__doc__ + """\nERROR: An input file AND an\
 output file need to be specified.
specify output file"""
            exp = exp.splitlines()

        # decode data stored in bytes if using Python 3, then compare lists.
        if sysvers == 3:
            act = []
            for line in new_doc:
                act.append(line.decode('ascii'))
            assert exp == act
        else:
            assert exp == new_doc


def test_winovf2vtk_no_keys_two_parameters():
    """test that the expected output is displayed when the command line
    includes two parameters: the infile and outfile"""

    # test two parameters with no keys
    for i in range(len(infiles)):
        # actual result
        command = 'python ' + os.path.join('..', 'winovf2vtk.py') +\
            " {} {}".format(infiles[i], outfiles[i])
        p = subprocess.Popen(command, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, shell=True)
        doc = p.stdout.readlines()
        # remove '\r\n' characters
        new_doc = []
        for j in range(len(doc)):
            line = doc[j].strip(b'\r\n')
            new_doc.append(line)
        str_doc = str(new_doc)

        # expected result
        # binary4 and binary8 files
        if i < 6:
            for item in banner_str:
                assert item in str_doc
            for item in in_out_str:
                assert item in str_doc

        # ascii files
        elif i > 5:
            for item in banner_str:
                assert item in str_doc
            for item in in_out_str:
                assert item in str_doc
            assert ascii_str in str_doc


def test_winovf2vtk_keys_two_parameters():
    """test that the expected output is displayed when the command line
    includes a key and two parameters: the infile and outfile"""
    for i in range(len(keys)):
        for j in range(len(infiles)):
            # actual result
            command = 'python ' + \
                      os.path.join('..', 'winovf2vtk.py') +\
                      " {} {} {}".format(keys[i], infiles[j], outfiles[j])
            p = subprocess.Popen(command, stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT, shell=True)
            doc = p.stdout.readlines()
            # remove '\r\n' characters
            new_doc = []
            for k in range(len(doc)):
                line = doc[k].strip(b'\r\n')
                new_doc.append(line)
            str_doc = str(new_doc)

            # compute expected results
            # '-V file.omf file.vtk'
            if i < 2:
                assert "This is version {}.".format(version) in \
                    str_doc

            # e.g. '-v binaryfile.omf binaryfile.vtk'
            if 1 < i < 4 and j < 6:
                for item in v_verbose_str:
                    assert item in str_doc
                for item in banner_str:
                    assert item in str_doc
                for item in in_out_str:
                    assert item in str_doc

            # e.g. '-v asciifile.omf asciifile.vtk'
            elif 1 < i < 4 and j > 6:
                for item in v_verbose_str[:8]:
                    assert item in str_doc
                for item in banner_str:
                    assert item in str_doc
                assert ascii_str in str_doc
                for item in in_out_str:
                    assert item in str_doc

            # e.g. --h infile outfile
            elif 3 < i < 6:
                exp = win.__doc__ + "\n"
                exp = exp.splitlines()
                # decode data if using Python3, then compare lists.
                if sysvers == 3:
                    act = []
                    for line in new_doc:
                        act.append(line.decode('ascii'))
                    assert exp == act
                else:
                    assert exp == new_doc

            # e.g. datascale/posscale/surface-effects/b/t binaryin binaryout
            elif 5 < i < 14 and j < 6:
                for item in banner_str:
                    assert item in str_doc
                for item in in_out_str:
                    assert item in str_doc

            # e.g. datascale/posscale/surface-effects/b/t asciiin asciiout
            elif 5 < i < 14 and j > 6:
                for item in banner_str:
                    assert item in str_doc
                for item in in_out_str:
                    assert item in str_doc
                assert ascii_str in str_doc

            # e.g. -a Ms binaryinfile.omf binaryoutfile.vtk
            elif i > 13 and j < 6:
                for item in banner_str:
                    assert item in str_doc
                for item in in_out_str:
                    assert item in str_doc
                assert add_str in str_doc

            # e.g. -a Ms asciiinfile.omf asciioutfile.vtk
            elif i > 13 and j > 6:
                for item in banner_str:
                    assert item in str_doc
                for item in in_out_str:
                    assert item in str_doc
                assert add_str in str_doc
                assert ascii_str in str_doc


def test_winovf2vtk_example_cmd_lines():
    """function that takes example cmd lines not tested by above tests, and
    asserts print statements containing ACTUAL VALUES are outputted."""

    examples = "python " + os.path.join('..', 'winovf2vtk.py') + \
        " -V --ascii {} {}".format(infiles[0], outfiles[0]),\
        "python " + os.path.join('..', 'winovf2vtk.py') + \
        " --datascale=0.5 --posscale 1.0 \
--add Ms -a divrot --add yz -v {} {}".format(infiles[6], outfiles[6]),\
        "python " + os.path.join('..', 'winovf2vtk.py') +\
        " -h --binary {} {}" .format(infiles[-1], outfiles[-1]),\
        "python " + os.path.join('..', 'winovf2vtk.py') +\
        " --add all --verbose --ascii --surface-effects {} {}"\
        .format(infiles[1], os.path.join('..', 'Examples', 'example.vtk')),\
        "python " + os.path.join('..', 'winovf2vtk.py') +\
        " -a Mx --add My -b \
--datascale=0.0 --surface-effects {} {} Test".format(infiles[7], outfiles[7])

    for i in range(len(examples)):
        # actual result
        p = subprocess.Popen(examples[i], stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, shell=True)
        doc = p.stdout.readlines()
        # remove '\r\n' characters
        new_doc = []
        for k in range(len(doc)):
            line = doc[k].strip(b'\r\n')
            new_doc.append(line)

        # test if -V present, only version string is displayed
        if i == 0:
            exp = ["This is version {}.".format(version)]

        # test several keys, ascii infile, ascii outfile
        elif i == 1:
            args = [('--datascale', '0.5'), ('--posscale', '1.0'),
                    ('--add', 'Ms'), ('-a', 'divrot'), ('--add', 'yz'),
                    ('-v', '')]
            options = {'--posscale': '1.0', '--add': 'yz', '-v': None,
                       '-a': 'divrot', '--datascale': '0.5'}
            exp = "running in verbose mode\n" + 70 * "-" + \
                "\novf2vtk --- converting ovf files to vtk files" + \
                "\n" + """Hans Fangohr, Richard Boardman, University of \
Southampton\n""" + 70 * "-" + "\n" + \
                """infile = {}
outfile = {}
args = {}
options = {}
datascale = 0.5
posscale = 1.0
Number of cells (Nx=5,Ny=3,Nz=1)
Hint: Reading ASCII-OOMMF file is slow (that could be changed) \
and the files are large. Why not save data as binary?
(100.00% of 15 cells filled)
working on ('--add', 'Ms')
working on ('-a', 'divrot')
-->Nz==1, special 2d case, will only compute z-component of curl
working on ('--add', 'yz')
saving file ({})
finished conversion (execution time
""".format(infiles[6], outfiles[6], args, options, outfiles[6])

            exp = exp.splitlines()
            # can't predict execution time
            new_doc[-1] = new_doc[-1][:35]

        # test if --help key present, just program documentation is outputted
        elif i == 2:
            exp = win.__doc__ + "\n"
            exp = exp.splitlines()

        # test several keys + binary outfile and infile with different name
        elif i == 3:
            args = [('--add', 'all'), ('--verbose', ''), ('--ascii', ''),
                    ('--surface-effects', '')]
            options = {'--ascii': None, '--add': 'all',
                       '--surface-effects': None, '--verbose': None}
            exp = "running in verbose mode\n" + 70 * "-" + \
                "\novf2vtk --- converting ovf files to vtk files" + \
                "\n" + """Hans Fangohr, Richard Boardman, University of \
Southampton\n""" + 70 * "-" + "\n" + \
                "infile = {}".format(infiles[1]) + "\n" + \
                """outfile = """ \
                + os.path.join('..', 'Examples', 'example.vtk') + "\n" + \
                """args = {}
options = {}
datascale = 0.0
posscale = 0.0
Number of cells (Nx=24,Ny=8,Nz=4)
Expect floats of length 4 bytes.
Expect to find data in file {} at position 850.
verification_tag is okay (=> reading byte order correctly)
(57.29% of 768 cells filled)
Will scale data down by 1.000000
switching to ascii vtk-data
working on ('--add', 'Ms')
working on ('--add', 'Mx')
working on ('--add', 'My')
working on ('--add', 'Mz')
working on ('--add', 'xy')
working on ('--add', 'yz')
working on ('--add', 'xz')
working on ('--add', 'divrot')""".format(args, options, infiles[1]) +\
                "\n" + \
                """saving file (""" \
                + os.path.join('..', 'Examples', 'example.vtk') + ")\n" + \
                """finished conversion (execution time
"""

            exp = exp.splitlines()
            # can't predict execution time
            new_doc[-1] = new_doc[-1][:35]

        # test several keys and ascii files with an extra parameter
        # assert extra parameter ignored
        else:
            exp = 70 * "-" + \
                "\novf2vtk --- converting ovf files to vtk files" + \
                "\n" + """Hans Fangohr, Richard Boardman, University of \
Southampton\n""" + 70 * "-" + "\n" + \
                """Hint: Reading ASCII-OOMMF file is slow (that could be \
changed) and the files are large. Why not save data as binary?
(100.00% of 6 cells filled)
Will scale data down by 21.954498
working on ('-a', 'Mx')
working on ('--add', 'My')
saving file ({})
finished conversion (execution time""".format(outfiles[7])

            exp = exp.splitlines()
            # can't predict execution time
            new_doc[-1] = new_doc[-1][:35]

        if i != 1:
            # decode data stored in bytes if using Python 3, then compare lists
            if sysvers == 3:
                act = []
                for line in new_doc:
                    act.append(line.decode('ascii'))
                # the order of the 'options' dic fluctuates. Cannot predict.
                # try new tests.
                if i == 1:
                    assert act[9:] == exp[9:]
                    assert act[:8] == exp[9:]
                    terms = ["'--posscale': '1.0'", "'--add': 'yz'",
                             "'-v': None", "'-a': 'divrot'",
                             "'--datascale': '0.5'"]
                    for term in terms:
                        assert term in act[8]
                elif i == 3:
                    assert act[9:] == exp[9:]
                    assert act[:8] == exp[:8]
                    terms = ["'--ascii': None", "'--add': 'all'",
                             "'--surface-effects': None", "'--verbose': None"]
                    for term in terms:
                        assert term in act[8]
                else:
                    assert exp == act
            else:
                assert exp == new_doc


def test_winovf2vtk_data():
    """test that the data within the vtk file is as expected for differing
    datascales, posscales, surface-effects, in-plane angles, magnitudes etc."""
    # one binary4, one binary8, one ascii
    files = [os.path.join('..', 'Examples', 'cantedvortex.omf'),
             os.path.join('..', 'Examples', 'ellipsoidwrap.omf'),
             os.path.join('..', 'Examples', 'yoyoleftedge.ohf'),
             os.path.join('..', 'Examples', 'smallDataText.omf'),
             os.path.join('..', 'Examples', 'plateDataText.omf')]
    vtk_files = [os.path.join('..', 'Examples', 'cantedvortex1.vtk'),
                 os.path.join('..', 'Examples', 'ellipsoidwrap1.vtk'),
                 os.path.join('..', 'Examples', 'yoyoleftedge1.vtk'),
                 os.path.join('..', 'Examples', 'smallDataText1.vtk'),
                 os.path.join('..', 'Examples', 'plateDataText1.vtk')]
    orgnl_vtk = [os.path.join('..', 'Examples', 'cantedvortex_orgnl.vtk'),
                 os.path.join('..', 'Examples', 'ellipsoidwrap_orgnl.vtk'),
                 os.path.join('..', 'Examples', 'yoyoleftedge_orgnl.vtk'),
                 os.path.join('..', 'Examples', 'smallDataText_orgnl.vtk'),
                 os.path.join('..', 'Examples', 'plateDataText_orgnl.vtk')]
    cmds = [' --datascale=0 --posscale=0 --add all',
            ' --datascale=1 --posscale=1 -a Ms -a xy -a xz -a divrot',
            ' --datascale=-1.3 --posscale=5 --surface-effects -a Mx -a xy',
            ' --posscale=10 --surface-effects -a all -b',
            ' -a xz -a Ms --datascale=1 -a divrot -t']
    for i in range(len(files)):
            subprocess.Popen(("python " +
                             os.path.join('..', 'winovf2vtk.py') +
                             cmds[i] + " " + files[i] + " " + vtk_files[i]),
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             shell=True)
            # compare created file data with data from file created earlier
            a = open(vtk_files[i], 'rb').readlines()
            b = open(orgnl_vtk[i], 'rb').readlines()
            assert a[2:] == b[2:]