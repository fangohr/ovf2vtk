"""Collection of routines used to post process (magnetisation)
vector data.

Part of ovf2vtk.

Hans Fangohr, hans.fangohr@physics.org


# Some helping functions:
#
# Set of functions used for ovf2vtk. General data format is a rank-2
# matrix with the row corresponding to the data in the vector field, and
# the 3-component column corresponding to the magnetisation vector at
# that place.
#
# Together with an index function (last component varying fastest,
# C-style) and positions vectors x_vec, y_vec and z_vec (for three
# dimensional domains), these data can be mapped to positions in real
# space.
#
# All this makes only sense for rectilinear grids.
#
# (fangohr 25/08/2003 00:18)

"""

try:
    import numpy as Numeric
except ImportError:
    print "This program needs Numpy. Please download and install. \
(http://sourceforge.net/projects/numpy)."
    print "If you are using Numeric, you can use the older version \
0.1.17 of ovf2vtk."
    raise ImportError("Couldn't import Numpy -- cannot proceed.")

__version__ = "$Revision: 1.3 $"


def magnitude(vec_array):
    """expects an array of 3D vectors; array of shape (Nx3),
    returns the magnitude (standard 2-Norm)"""
    # square entries:                  d*d
    # sum over 3-components (axis 1):  add.reduce( d*d, 1)
    # take square root                 sqrt( add.reduce ( d*d, 1 ) )
    return Numeric.sqrt(Numeric.add.reduce(vec_array ** 2, 1))


def convert_flat_fortran_to_3dmatrix(vf, Nx, Ny, Nz):
    """Takes a 1xN array, vf, and converts it to an array of shape
    (Nx, Ny, Nz, 3) -> In Fortan order"""
    return Numeric.resize(vf, (Nz, Ny, Nx, 3))


def convert_fortran_3dmatrix_to_flat(M):
    """Takes array of any shape, returns array of shape (1xN)"""
    return Numeric.array(M).ravel()


def convert_fortran_3dmatrix_to_flat_vector(M):
    """Takes array of any shape, returns array of shape (X, 3)"""
    N = len(Numeric.array(M).ravel())
    return Numeric.resize(M, (N/3, 3))


def convert_between_fortran_and_C(a):
    """assuming Fortran data is stored as M[Nz,Ny,Nx,:,...:] and
    C data as M[Nx,Ny,Nz,:,,...,:] then this function converts from
    one to the other. (fangohr 31/03/2004 23:06)"""
    return Numeric.swapaxes(a, 0, 2)


def components(vec_array):
    """returns the x, y and z components of an array of vectors of shape Nx3"""
    return (vec_array[:, 0], vec_array[:, 1], vec_array[:, 2])


def plane_angles(vec_array):
    """Input is matrix, containing N 3d vectors.
    Returns angles in yx, yz and xz plane for all vectors."""
    x, y, z = components(vec_array)

    # if any Ms is smaller that 1e-6, then set to zero to eliminate noise
    cutoff = 1e-6

    Ms = magnitude(vec_array)

    x2 = Numeric.choose(Numeric.less(Ms, cutoff), (x, 0.0))
    y2 = Numeric.choose(Numeric.less(Ms, cutoff), (y, 0.0))
    z2 = Numeric.choose(Numeric.less(Ms, cutoff), (z, 0.0))

    xy = Numeric.arctan2(y2, x2)
    yz = Numeric.arctan2(z2, y2)
    xz = Numeric.arctan2(z2, x2)
    return xy, yz, xz


def convert_matrix_shape_to_clean(cleanM, M, wipe, Nx, Ny, Nz):
    """Takes a matrix of shape (Nx, Ny, Nz) or (Nx, Ny, Nz, 3) and returns a
    matrix of size (Nx+wipe, Ny+wipe, Nz+wipe) or
    (Nx+wipe, Ny+wipe, Nz+wipe, 3). This allows the function
    'clean_surfaces' to initiate"""

    assert cleanM.shape[0:2] == M.shape[0:2], "Internal error"

    if len(cleanM.shape) == 3:
        cleanM_is_scalar = True
        cleanM_is_vector = False

    elif len(cleanM.shape) == 4:
        cleanM_is_scalar = False
        cleanM_is_vector = True

    else:
        raise NotImplementedError("""Can only deal with scalar and vectors\
 (in 3d positional matrix)""")

    if cleanM_is_scalar:
        cleanM_large = Numeric.zeros((Nx+2*wipe, Ny+2*wipe, Nz+2*wipe), 'd')
    if cleanM_is_vector:
        cleanM_large = Numeric.zeros((Nx+2*wipe, Ny+2*wipe, Nz+2*wipe, 3), 'd')

    return cleanM_large


def clean_surfaces(cleanM, M, wipe=0, eps=1e-3, zerovalue=0.0):
    """sets all values in obs to zero value for which abs(M)<eps. If wipe > 0,
       then all positions up to 'wipe' indices away from the M<eps entry are
       set to zerovalue as well.

    Example: hide divergence effects at surface:

       * clean_surfaces(div, M, wipe=1, eps=1e-5)

    This is only of relevance if there is 'vacuum' in the simulation cell
    (i.e. an aero with Ms=0). The computation of the divergence and the curl
    will produce large values across the interface from Ms!=0 to Ms=0. This
    distracts from the more interesting data inside the Ms!=0 volume. We
    therefore simply wipe out the outermost layer of div and curl data that is
    affected by this.

    This process is slow as it is using for-loops.
    """

    Nx, Ny, Nz, dummy = M.shape

    cleanM_large = convert_matrix_shape_to_clean(cleanM, M, wipe, Nx, Ny, Nz)

    # copy input values in here
    cleanM_large[wipe:Nx+wipe, wipe:Ny+wipe, wipe:Nz+wipe] = cleanM[:, :, :]

    offset = wipe

    for i in range(Nx):
        for j in range(Ny):
            for k in range(Nz):
                if sum(M[i, j, k]**2) < eps**2:
                    # wipe out matrix entries with indicies +- wipe around...
                    # ...[i,j,k]
                    cleanM_large[i-wipe+offset:i+wipe+1+offset,
                                 j-wipe+offset:j+wipe+1+offset,
                                 k-wipe+offset:k+wipe+1+offset] = zerovalue

    cleanM = cleanM_large[wipe:Nx+wipe, wipe:Ny+wipe, wipe:Nz+wipe]

    return cleanM


def central_differences(M, ovf_run):
    """reads the stepsizes of each component x,y,z from the ovf file being
    read, and uses this as well as the vectorfield data to calculate
    the central differences e.g. dMx/dx"""

    # print "a, b, c" as a, b, c
    dx = float(ovf_run["xstepsize:"])
    dy = float(ovf_run["ystepsize:"])
    dz = float(ovf_run["zstepsize:"])

    # total magnitude of curl is irrelevant, re-scale dx, dy, dz to...
    # ...avoid overflow:
    scale = min(dx, dy, dz)
    dx /= scale
    dy /= scale
    dz /= scale

    # compute (central differences):
    dMdx = Numeric.array(M[2:, :, :, :]-M[:-2, :, :, :])
    dMxdx, dMydx, dMzdx = [dMdx[:, :, :, i]/dx for i in range(3)]

    dMdy = Numeric.array(M[:, 2:, :, :]-M[:, :-2, :, :])
    dMxdy, dMydy, dMzdy = [dMdy[:, :, :, i]/dx for i in range(3)]

    dMdz = Numeric.array(M[:, :, 2:, :]-M[:, :, :-2, :])
    dMxdz, dMydz, dMzdz = [dMdz[:, :, :, i]/dx for i in range(3)]

    values = dMxdx, dMydx, dMzdx, dMxdy, dMydy, dMzdy, dMxdz, dMydz, dMzdz
    return values


def divergence_and_curl(vf, surfaceEffects, ovf_run):
    """A new attempt to compute the divergence and the curlfaster using
vector/matrix operations in Numeric rather than for-loops in
Python. (fangohr 31/03/2004 00:25)

Input data is:
    vf             : the VectorField (as created by omfread)
    surfaceEffects : a boolean
    ovf_run        : dictionary with keyword-value pairs from ovf file header.
    """
    dimensions = (int(ovf_run["xnodes:"]),
                  int(ovf_run["ynodes:"]),
                  int(ovf_run["znodes:"]))

    Nx, Ny, Nz = dimensions[0], dimensions[1], dimensions[2]

    # get data into array of shape (Nx,Ny,Nz,3) (This is C-style)
    M = convert_flat_fortran_to_3dmatrix(vf, Nx, Ny, Nz)
    M = convert_between_fortran_and_C(M)

    # retrieve central differences
    dMxdx, dMydx, dMzdx, dMxdy, dMydy, dMzdy, dMxdz, dMydz, dMzdz =\
        central_differences(M, ovf_run)

    # set divergence values
    div = Numeric.zeros((Nx, Ny, Nz), 'd')

    div[1:-1, :, :] += dMxdx
    div[:, 1:-1, :] += dMydy
    div[:, :, 1:-1] += dMzdz

    if not surfaceEffects:
        div = clean_surfaces(div, M, wipe=1)

    Fdiv = convert_between_fortran_and_C(div)
    divflat = convert_fortran_3dmatrix_to_flat(Fdiv)

    # set curl values
    curl = Numeric.zeros((Nx, Ny, Nz, 3), 'd')

    # taking the cross product (this excludes the outermost layers as
    # we can't take the central difference for these)
    curl[1:-1, 1:-1, 1:-1, 0] = dMzdy[1:-1, :, 1:-1]-dMydz[1:-1, 1:-1, :]
    curl[1:-1, 1:-1, 1:-1, 1] = dMxdz[1:-1, 1:-1, :]-dMzdx[:, 1:-1, 1:-1]
    curl[1:-1, 1:-1, 1:-1, 2] = dMydx[:, 1:-1, 1:-1]-dMxdy[1:-1, :, 1:-1]

    # special 2d-case (only one layer in z)
    if Nz == 1:
        print "-->Nz==1, special 2d case, will only compute \
z-component of curl"
        curl[1:-1, 1:-1, 0, 2] = dMydx[:, 1:-1, 0]-dMxdy[1:-1, :, 0]

    if not surfaceEffects:
        curl = clean_surfaces(curl, M, wipe=1)

    Fcurl = convert_between_fortran_and_C(curl)
    curlflat = convert_fortran_3dmatrix_to_flat_vector(Fcurl)

    curlmag = magnitude(curlflat)

    return (divflat, curlflat, curlflat[:, 0], curlflat[:, 1],
            curlflat[:, 2], curlmag)
