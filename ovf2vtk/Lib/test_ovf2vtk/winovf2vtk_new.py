#!C:\Users\Harry\Anaconda\python.exe

"""

----------------------------------------------------------------------------

ovf2vtk: convert OOMMF vector-field file into vtk-vector field file

SYNTAX: ovf2vtk [OPTIONS] infile outfile

OPTIONS:

        [--add xy ]
            adding a scalar component to the outfile showing the
            inplane angle of the magnetisation for the xy -plane.
        [--add yz ]
            as --add xy but for the yz-plane.
        [--add xz ]
            as --add xy but for the xz-plane.
        [--add Mx ]
           adds scalar fields containing the x-component of M to the file
        [--add My ]
           adds scalar fields containing the y-component of M to the file
        [--add Mz ]
           adds scalar fields containing the z-component of M to the file
        [--add divrot]
           * adds a vector field containing the DIVergence of the magnetisation
           * adds a vector field containing the vorticity (=curl=ROT) of the
             magnetisation
           * adds also components of this vorticity field as scalars
        [--surface-effects]
           shows divergence and vorticity at sample surfaces (default is off)
        [--add Ms]
           adds a scalar field containing the magnitude of the magnetisation
           (this can be employed to visualise the shape of the object using
             an isosurface.)
        [--add all ]
           add all of the above
        [--binary -b]
           write binary vtk-file (this is the default, needs PyVTK>0.4)
        [--ascii -t]
           write text-vtk file
        [--help -h]
           display this text
        [--verbose -v]
           be more verbose
        [--datascale X]
           express field in units of X. Example: if the field M is
           magnetisation, and X=10e6, then the data in the vtk file
           will be M/X.
           If X==0, then the data will be normalised (i.e. X=max(M))
           Default is X=0.
        [--posscale X]
           express positions in units of X. See --datascale for example.
           If X==0, then grid point indices will be used as positions.
           Default is X=0.
        [--version -V]
           Displays version number

COMMENTS:   --add can be abbreviated to -a

EXAMPLE:

 1. If the data file (for example data.ovf) is small, then the easiest
 option is to generate all additional fields available:

 ovf2vtk --add all data.ovf data.vtk

 This will create the data.vtk file, and should cover the needs of
 most users.

 2. If the data file (data.ovf) is large, then it may be advisable
 to only store the observables in data.vtk one is actually interested in.
 This line demonstrates this:

 ovf2vtk --add Mx --add My --add Mz data.ovf data.vtk

BUGS etc

    Please report bugs, problems and other feedback to Hans Fangohr
    (hans.fangohr@physics.org)

"""

__CVS__header__ = "$Header: /var/local/cvs/micromagnetics/mm0/released\
/ovf2vtk/bin/ovf2vtk,v 1.7 2006-12-30 22:07:50 fangohr Exp $"

__CVS__date__ = "$Date: 2006-12-30 22:07:50 $"
__CVS__version__ = "$Revision: 1.7 $"


import sys

import getopt

import time

import os

try:
    import pyvtk
except ImportError:
    print "This program needs pyvtk. Please download and install from \
(http://cens.ioc.ee/projects/pyvtk/)"
    raise ImportError("Couldn't import pyvtk -- cannot proceed.")


try:
    import numpy as Numeric
except ImportError:
    print "This program needs Numpy. Please download and install. \
(http://sourceforge.net/projects/numpy)."
    print "If you are using Numeric, \
you can use the older version 0.1.17 of ovf2vtk."
    raise ImportError("Couldn't import Numpy -- cannot proceed.")


# try:
#    import Numeric
# except ImportError:
#    print "This program needs Numpy. Please download and install.
#    (http://sourceforge.net/projects/numpy)."
#    raise ImportError,"Couldn't import Numpy -- cannot proceed."
#


# import ovf2vtk
import ovf2vtk

# import tools toread omf file
from ovf2vtk.omfread import read_structured_omf_file, analyze

# import tools to compute further observables
from ovf2vtk.analysis import plane_angles, divergence_and_curl, magnitude, \
    components

# this is the  list of keywords used by --add all
add_features = ["Ms", "Mx", "My", "Mz", "xy", "yz", "xz", "divrot"]


# =============================================================================
# =
# = ovf2vtk
# =
# =============================================================================


def ovf2vtk_main():
    start_time = time.time()

    banner_doc = 70 * "-" + \
        "\novf2vtk --- converting ovf files to vtk files" + "\n" + \
        "Hans Fangohr, Richard Boardman, University of Southampton\n"""\
        + 70 * "-"

    # extract command line arguments
    additions, params = getopt.getopt(sys.argv[1:], 'Vvhbta:',
                                      ["verbose", "help", "add=", "binary",
                                       "text", "ascii", "surface-effects",
                                       "version", "datascale=", "posscale="])

    # Note (fangohr 30/12/2006 20:52): the use of getopt is historic,
    # and so is the use of the name 'additions'.

    # default value
    surfaceEffects = False
    datascale = 0.0  # 0.0 has special meaning -- see help text
    posscale = 0.0   # 0.0 has special meaning -- see help text

    # provide data from getopt.getopt (additions) in form of hash table
    options = {}
    for item in additions:
        if item[1] == '':
            options[item[0]] = None
        else:
            options[item[0]] = item[1]
    keys = options.keys()

    if "--surface-effects" in keys:
        surfaceEffects = True

    if "--posscale" in keys:
        posscale = float(options["--posscale"])

    if "--datascale" in keys:
        datascale = float(options["--datascale"])

    if "-v" in keys or "--verbose" in keys:
        print "running in verbose mode"
        debug = True
    else:
        debug = False

    if "-h" in keys or "--help" in keys:
        print __doc__
        sys.exit(0)

    if "-V" in keys or "--version" in keys:
        print "This is version {:s}.".format(ovf2vtk.__version__)
        sys.exit(0)

    if len(params) == 0:
        print __doc__
        print "ERROR: An input file (and an output file need to be specified)."
        sys.exit(1)
    else:
        infile = params[0]

    if len(params) == 1:
        print __doc__
        print "ERROR: An input file AND an output file need to be specified."
        print "specify output file"
        sys.exit(1)
    else:
        outfile = params[1]

    # okay: it seems the essential parameters are given.
    # Let's check for others:

    print banner_doc

    if debug:
        print "infile  = ", infile
        print "outfile = ", outfile
        print "additions= ", additions
        print "options = ", options
        print "datascale=", datascale
        print "posscale=", posscale

    # read data from infile
    vf = read_structured_omf_file(infile, debug)

    # compute magnitude for all cells
    Ms = magnitude(vf)

    # Compute number of cells with non-zero Ms (rpb01r)
    Ms_num_of_nonzeros = Numeric.sum(Numeric.not_equal(Ms, 0.0))
    print "({:5.2f}% of {:d} cells filled)"\
        .format(100.0*Ms_num_of_nonzeros/len(Ms), len(Ms))

    # read metadata in data file
    ovf_run = analyze(infile)

    # scale magnetisation data as required:
    if datascale == 0.0:
        scale = max(Ms)
        print "Will scale data down by {:f}".format(scale)
    else:
        scale = datascale
    vf = Numeric.divide(vf, scale)

    datatitle = ovf_run["Title:"]+"/{:g}".format(scale)

    #
    # need x, y and z vectors for vtk format
    #

    # taking actual spacings for dx, dy and dz results generally in
    # poor visualisation results (in particular for thin films, one
    # would like to have some magnification in z-direction).  Also:vtk
    # is not happy with positions on the 10e-9 scale, so one better
    # scales this to something closer to unity.

    # extract dimensions from file
    dimensions = (int(ovf_run["xnodes:"]),
                  int(ovf_run["ynodes:"]),
                  int(ovf_run["znodes:"]))

    if posscale != 0.0:  # scale data by given factor

        # find dx, dy, dz in SI units:
        Lx = abs(float(ovf_run["xmax:"])-float(ovf_run["xmin:"]))
        Ly = abs(float(ovf_run["ymax:"])-float(ovf_run["ymin:"]))
        Lz = abs(float(ovf_run["zmax:"])-float(ovf_run["zmin:"]))

        dx = Lx / float(ovf_run["xnodes:"])
        dy = Ly / float(ovf_run["ynodes:"])
        dz = Lz / float(ovf_run["znodes:"])

        # find scale factor that OOMMF uses for xstepsize and xnodes,
        # etc. (Don't know how to get this directly.)
        xscale = dx * float(ovf_run["xstepsize:"])
        yscale = dy * float(ovf_run["ystepsize:"])
        zscale = dz * float(ovf_run["zstepsize:"])

        # extract x, y and z positions from ovf file.
        xbasevector = [None] * dimensions[0]  # create empty vector
        for i in range(dimensions[0]):
            # data is stored for 'centre' of each cuboid, therefore (i+0.5)
            xbasevector[i] = float(ovf_run["xbase:"]) +\
                (i+0.5) * float(ovf_run["xstepsize:"])*xscale

        ybasevector = [None] * dimensions[1]
        for i in range(dimensions[1]):
            ybasevector[i] = float(ovf_run["ybase:"]) + (i+0.5) * \
                float(ovf_run["ystepsize:"]) * yscale

        zbasevector = [None] * dimensions[2]
        for i in range(dimensions[2]):
            zbasevector[i] = float(ovf_run["zbase:"]) + (i+0.5) *\
                float(ovf_run["zstepsize:"]) * zscale

        # finally, convert list to numerix (need to have this consistent)
        xbasevector = Numeric.array(xbasevector)/float(posscale)
        ybasevector = Numeric.array(ybasevector)/float(posscale)
        zbasevector = Numeric.array(zbasevector)/float(posscale)

    else:  # posscale == 0.0
        #
        # this generally looks better:
        #
        xbasevector = Numeric.arange(dimensions[0])
        ybasevector = Numeric.arange(dimensions[1])
        zbasevector = Numeric.arange(dimensions[2])

    #
    # write ascii or binary vtk-file (default is binary)
    #
    vtk_data = 'binary'

    if '--ascii' in keys or '-t' in keys or '--text' in keys:
        vtk_data = 'ascii'
        if debug:
            print "switching to ascii vtk-data"
    if '--binary' in keys or '-b' in keys:
        vtk_data = 'binary'
        if debug:
            print "switching to binary vtk-data"

    #
    # and now open vtk-file
    #
    vtkfilecomment = "Output from ovf2vtk (version {:s}), {:s}, infile={:s}. "\
        .format(ovf2vtk.__version__, time.asctime(), infile)
    vtkfilecomment += "Calling command line was '{:s}' executed in '{:s}'"\
        .format(" ".join(sys.argv), os.getcwd())

    vtk = pyvtk.VtkData(pyvtk.RectilinearGrid(xbasevector.tolist(),
                                              ybasevector.tolist(),
                                              zbasevector.tolist()),
                        vtkfilecomment,
                        pyvtk.PointData(pyvtk.Vectors(vf.tolist(), datatitle)),
                        format=vtk_data)

    #
    # now compute all the additional data such as angles, etc
    #

    # check whether we should do all
    keys = map(lambda x: x[1], additions)
    if "all" in keys:
        additions = []
        for add in add_features:
            additions.append(("--add", add))

    # when ovf2vtk was re-written using Numeric, I had to group
    # certain operations to make them fast. Now some switches are
    # unneccessary. (fangohr 25/08/2003 01:35)
    # To avoid executing the
    # same code again, we remember what we have computed already:

    done_angles = 0
    done_comp = 0

    for add in additions:
        if add[0] == "-a" or add[0] == "--add":
            print "working on", add

            data = []

            # compute observables that need more than one field value
            # i.e. div, rot
            if add[1][0:6] == "divrot":  # rotation = vorticity, curl

                (div, rot, rotx, roty, rotz, rotmag) = \
                    divergence_and_curl(vf, surfaceEffects, ovf_run)

                comment = "curl, x-comp"
                vtk.point_data.append(pyvtk.Scalars(rotx.tolist(), comment,
                                                    lookup_table='default'))
                comment = "curl, y-comp"
                vtk.point_data.append(pyvtk.Scalars(roty.tolist(), comment,
                                                    lookup_table='default'))
                comment = "curl, z-comp"
                vtk.point_data.append(pyvtk.Scalars(rotz.tolist(), comment,
                                                    lookup_table='default'))
                comment = "curl, magnitude"
                vtk.point_data.append(pyvtk.Scalars(rotmag.tolist(), comment,
                                                    lookup_table='default'))
                comment = "curl"
                vtk.point_data.append(pyvtk.Vectors(rot.tolist(), comment))

                comment = "divergence"
                vtk.point_data.append(pyvtk.Scalars(div.tolist(), comment,
                                                    lookup_table='default'))

            elif add[1] in ["Mx", "My", "Mz", "Ms"]:              # components
                if not done_comp:
                    done_comp = 1

                    comments = "x-component", "y-component", "z-component"

                    for data, comment in zip(components(vf), comments):
                        vtk.point_data.append(pyvtk.Scalars(data.tolist(),
                                                            comment,
                                                            lookup_table='\
default'))

                    # magnitude of magnitisation
                    Mmag = magnitude(vf)
                    vtk.point_data.append(pyvtk.Scalars(Mmag.tolist(),
                                                        "Magnitude",
                                                        lookup_table='\
default'))

            elif add[1] in ["xy", "xz", "yz"]:
                if not done_angles:
                    done_angles = 1

                    # in-plane angles
                    comments = ("xy in-plane angle", "yz in-plane angle",
                                "xz in-plane angle")

                    for data, comment in zip(plane_angles(vf), comments):
                        vtk.point_data.append(pyvtk.Scalars(data.tolist(),
                                                            comment,
                                                            lookup_table='\
default'))

            else:
                print "only xy, xz, Mx, My, Mz, divergence, Ms, or 'all' \
allowed after -a or --add"
                print "Current choice is", add
                print __doc__
                sys.exit(1)

    #
    # eventually, write the file
    #
    print "saving file ({:s})".format(outfile)
    vtk.tofile(outfile, format=vtk_data)

    print "finished conversion (execution time {:5.3s} seconds)"\
        .format(str(time.time()-start_time))

# ==============================================================================
# =
# = main
# =
# ==============================================================================

if __name__ == "__main__":
    ovf2vtk_main()
