
import subprocess

import ovf2vtk

from ovf2vtk import winovf2vtk

"""all the tests developed for the winovf2vtk.py script for ovf2vtk stored in
one place. By Harry Wilson. Last updated 15/04/16"""

# ****************************** Global Variables ***************************

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
cells_filled = [100.00, 57.29, 100.00, 99.60, 100.00, 100.00, 100.00, 100.00,
                100.00]

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
    # list of keys that can be used. '--add/--binary/--text/--ascii' are...
    # ...not selected here as these are tested later.
    keys = ['-V', '--version', '-v', '--verbose', '-h', '--help',
            '--surface-effects', '--datascale=0.0', '--posscale=0.0']
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
    # list of keys that can be used. '--add/--binary/--text/--ascii' are...
    # ...not selected here as these are tested later.
    keys = ['-V', '--version', '-v', '--verbose', '-h', '--help',
            '--surface-effects', '--datascale=0.0', '--posscale=0.0']
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


def test_winovf2vtk_keys_two_parameters():
    """test that the expected output is displayed when the command line
    includes a key and two paramters: the infile and outfile"""
    
