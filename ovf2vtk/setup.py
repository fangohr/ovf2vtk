#!/usr/bin/env python

# setup.py - build and install the ovf2vtk package
#
# Copyright 2002-2009 Hans Fangohr, Richard Boardman
#
# This file is part of ovf2vtk.
#
#
# Authors: Hans Fangohr, Richard Boardman
#
#
"""ovf2vtk -- data conversion from OOMMF's ovf/ovf file format to VTK.

This program reads ovf files keeping vector data from the OOMMF
simulation package, extracts the data, optionally adds derived
observables (mainly curl and divergence) and saves the input data and
any derived entities into VTK files.

Supported file formats are:

input files:

   ovf files(v1.0), rectangular mesh only
   data can be ascii, binary4 or binary 8

output files:

   VTK File Formats Standard 2.0. (This depends on PyVTK.)


Related information:

VTK is the Visualisation ToolKit (http://www.vtk.org/)

OOMMF is the Object Oriented MicroMagnetic Framework
(http://math.nist.gov/oommf/)

Requirements:

   Python (www.python.org)

   PyVTK is used to write Python data structures into VTK data
   file. (http://cens.ioc.ee/projects/pyvtk/)

--> See README for most up-to-date version of this text.
"""

doclines = open('README','r').readlines()

classifiers = """\
Development Status :: 3 - Alpha
Intended Audience :: Developers
Intended Audience :: Education
Intended Audience :: Science/Research
Natural Language :: English
Operating System :: OS Independent
Programming Language :: Python
Topic :: Scientific/Engineering
License :: OSI Approved :: GNU General Public License (GPL)
Topic :: Scientific/Engineering :: Visualization
"""

__CVS__version__ = "$Revision: 1.7 $"

import os


#compute revision_version
major_version = 0
minor_version = 1
import tools.get_revision
revision_version = tools.get_revision.get_revision_version()
__version__='%d.%d.%d'%(major_version,minor_version,revision_version)

#and write into Lib/__version__.py file
f = open(os.path.join('Lib','__version__.py'),'w')
f.write('__version__ = "%s"\n'%(__version__))
f.close()



from distutils.core import setup, Extension

# patch distutils if it can't cope with the "classifiers" or
# "download_url" keywords
import sys
if sys.version < '2.2.3':
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None
    doclines = __doc__.split("\n")

setup(name = "ovf2vtk",
      version = __version__,
      author = "Hans Fangohr, Richard Boardman",
      author_email = "hans.fangohr@physics.org",
      maintainer = "Hans Fangohr",
      maintainer_email = "hans.fangohr@physics.org",
      url = "http://www.soton.ac.uk/~fangohr/software/ovf2vtk",
      license = "GPL",
      description = doclines[0],
      long_description = """
OVF2VTK -- File format conversion from OVF to VTK.

Hans Fangohr
University of Southampton 2002 - 2006

Richard Boardman
University of Southampton 2004

ovf2vtk -- data conversion from OOMMF's ovf/ovf file format to VTK.

This program reads ovf files keeping vector data from the OOMMF
simulation package, extracts the data, optionally adds derived
observables (mainly curl and divergence) and saves the input data and
any derived entities into VTK files.

Supported file formats are:

input files:

   ovf files(v1.0), rectangular mesh only
   data can be ascii, binary4 or binary 8

output files:

   VTK File Formats Standard 2.0. (This depends on PyVTK.)


Related information:

VTK is the Visualisation ToolKit (http://www.vtk.org/)

OOMMF is the Object Oriented MicroMagnetic Framework
(http://math.nist.gov/oommf/)

PyVTK is used to write Python data structures into VTK data
file. (http://cens.ioc.ee/projects/pyvtk/)
      """,
      keywords = ["OOMMF", "VTK", "visualisation", "conversion"],
      platforms = ["any"],
      download_url = "http://www.soton.ac.uk/~fangohr/software/ovf2vtk",
      classifiers = filter(None, classifiers.split("\n")),
      packages = ["ovf2vtk"],
      package_dir = {'ovf2vtk':'Lib'},
      scripts = ["bin/ovf2vtk","bin/winovf2vtk.py"]
      )


