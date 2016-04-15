# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 16:09:52 2016

@author: Harry
"""

import os

import sys

import subprocess

from StringIO import StringIO


def test():
    result = StringIO()
    sys.stdout = result
    try:
        os.system('python.exe C:\Users\Harry\Anaconda\Scripts\winovf2vtk.py -V'
                  )
    except SystemExit:
        result_string = result.getvalue()
        assert result_string == """

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


def run_command(command):
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    return p.stdout.readlines()
            