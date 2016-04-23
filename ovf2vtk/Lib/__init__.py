"""ovf2vtk -- data conversion from OOMMF's ovf/ovf file format to VTK.

This module contains submodules

  omfread  -- reading of ovf files
  analysis -- some post processing.

There is an executable (usually of name ovf2vtk) which imports these modules
and can be used to convert ovf files to vtk from the command prompt.

hans.fangohr@physics.org (fangohr 02/05/2005 14:33)
"""

from __version__ import __version__
