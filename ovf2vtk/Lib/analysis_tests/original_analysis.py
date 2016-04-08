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
    print "This program needs Numpy. Please download and install. (http://sourceforge.net/projects/numpy)."
    print "If you are using Numeric, you can use the older version 0.1.17 of ovf2vtk."
    raise ImportError,"Couldn't import Numpy -- cannot proceed."

__version__ = "$Revision: 1.3 $"


def magnitude(d):
    """expects d to be a 1xN array,
    returns the magnitude (standard 2-Norm)"""
    # square entries:                  d*d
    # sum over 3-components (axis 1):  add.reduce( d*d, 1)
    # take square root                 sqrt( add.reduce ( d*d, 1 ) )
    return Numeric.sqrt(Numeric.add.reduce(d * d, 1))


def convert_flat_fortran_to_3dmatrix( vf, Nx, Ny, Nz ):
    return Numeric.resize( vf, (Nz,Ny,Nx,3)) #this is in Fortran order

def convert_fortran_3dmatrix_to_flat( M ):
    return Numeric.array( M ).ravel()

def convert_fortran_3dmatrix_to_flat_vector( M ):
    N = len( Numeric.array(M).ravel() )
    return Numeric.resize( M, (N/3,3) )

def convert_fortran_to_C( a ):
    """assuming Fortran data is stored as M[Nz,Ny,Nx,:,...:] and
    C data as M[Nx,Ny,Nz,:,,...,:] then this function converts from
    one to the other. (fangohr 31/03/2004 23:06)"""
    return Numeric.swapaxes( a, 0, 2)

def convert_C_to_fortran( a ):
    return convert_fortran_to_C( a )

def fortranindex (i,j,k,Nx,Ny,Nz):
    """x changes fastest"""
    return i+j*Nx+k*Nx*Ny

def Cindex (i,j,k,Nx,Ny,Nz):
    """z changes fastest """
    return i*Nz*Ny+j*Nz+k

def components( d ):
    return ( d[:,0],  d[:,1],  d[:,2] )

def plane_angles( d ):
    """
    Input is matrix, containing N 3d vectors.

    returns angles in yx, yz and xz plane for all vectors. """
    x, y, z = components( d )

    #if any Ms is smaller that 1e-6, then set to zero to eliminate noise
    cutoff=1e-6

    Ms = magnitude( d )
    
    x2 = Numeric.choose( Numeric.less( Ms, cutoff ), ( x, 0.0 ) )
    y2 = Numeric.choose( Numeric.less( Ms, cutoff ), ( y, 0.0 ) )
    z2 = Numeric.choose( Numeric.less( Ms, cutoff ), ( z, 0.0 ) ) 
    
    xy = Numeric.arctan2( y2, x2 )
    yz = Numeric.arctan2( z2, y2 )
    xz = Numeric.arctan2( z2, x2 )
    return xy, yz, xz 

def clean_surfaces( obs, M, wipe=0, eps = 1e-3, zerovalue = 0.0):
    """sets all values in obs to zero value for which abs(M)<eps. If wipe > 0, then
    all positions up to 'wipe' indicies away from the M<eps entry are set to zerovalue
    as well.

    Example: hide divergence effects at surface:

       * clean_surfaces( div, M, wipe=1, eps=1e-5)

    This is only of relevance if there is 'vacuum' in the simulation cell (i.e. an aero with
    Ms=0). The computation of the divergence and the curl will produce large values across
    the interface from Ms!=0 to Ms=0. This distracts from the more interesting data
    inside the Ms!=0 volume. We therefore simply wipe out the outermost layer of div and
    curl data that is affected by this.

    This process is slow as it is using for-loops. 
    """

    assert obs.shape[0:2] == M.shape[0:2],"Internal error"

    Nx, Ny, Nz, dummy = M.shape

    if len(obs.shape) == 3:
        obs_is_scalar = True
        obs_is_vector = False
        obs_rank = 1
        
    elif len(obs.shape) == 4:
        obs_is_scalar = False
        obs_is_vector = True
        obs_rank = 3
    else:
        raise NotImplementedError,"Can only deal with scalar and vectors (in 3d positional matrix)"

    if obs_is_scalar:
        big_obs = Numeric.zeros( (Nx+2*wipe,Ny+2*wipe,Nz+2*wipe), 'd')
    if obs_is_vector:
        big_obs = Numeric.zeros( (Nx+2*wipe,Ny+2*wipe,Nz+2*wipe,3), 'd')

    offset = wipe
    
    #copy input values in here
    big_obs[wipe:Nx+wipe,wipe:Ny+wipe,wipe:Nz+wipe] = obs[:,:,:]

    for i in range(Nx):
        for j in range(Ny):
            for k in range(Nz):
                if sum(M[i,j,k]**2) < eps**2:
                    #wipe out matrix entries with indicies +- wipe around [i,j,k]
                    big_obs[i-wipe+offset:i+wipe+1+offset,
                            j-wipe+offset:j+wipe+1+offset,
                            k-wipe+offset:k+wipe+1+offset]=zerovalue
 
    obs = big_obs[wipe:Nx+wipe,wipe:Ny+wipe,wipe:Nz+wipe]

    return obs
    

def divergence_and_curl( vf, surfaceEffects, ovf_run ):
    """A new attempt to compute the divergence and the curlfaster using
vector/matrix operations in Numeric rather than for-loops in
Python. (fangohr 31/03/2004 00:25)

Input data is:
    vf              : the VectorField (as created by omfread)
    surfaceEffects  : a boolean
    ovf_run         : dictionarry with keyword-value pairs from ovf file header.
    """
    dimensions = ( int( ovf_run["xnodes:"] ), \
                   int( ovf_run["ynodes:"] ), \
                   int( ovf_run["znodes:"] ))

    Nx = dimensions[0]
    Ny = dimensions[1]
    Nz = dimensions[2]

    # get data into array of shape (Nx,Ny,Nz,3) (This is C-style)
    M = convert_flat_fortran_to_3dmatrix( vf, Nx, Ny, Nz )
    M = convert_fortran_to_C( M )

    #print "Nx, Ny, Nz=", Nx, Ny, Nz

    dx = float( ovf_run["xstepsize:"] )
    dy = float( ovf_run["ystepsize:"] )
    dz = float( ovf_run["zstepsize:"] )

    #total magnitude of curl is irrelevant, re-scale dx, dy, dz to avoid overflow:

    scale = min(dx, dy, dz)

    dx /= scale
    dy /= scale
    dz /= scale

    #compute dMx/dx (central differences):

    dMdx = Numeric.array( M[2:,:,:,:]-M[:-2,:,:,:])
    dMxdx, dMydx, dMzdx = dMdx[:,:,:,0]/dx,dMdx[:,:,:,1]/dx,dMdx[:,:,:,2]/dx
    dMdy = Numeric.array( M[:,2:,:,:]-M[:,:-2,:,:])
    dMxdy, dMydy, dMzdy = dMdy[:,:,:,0]/dy,dMdy[:,:,:,1]/dy,dMdy[:,:,:,2]/dy
    dMdz = Numeric.array( M[:,:,2:,:]-M[:,:,:-2,:])
    dMxdz, dMydz, dMzdz = dMdz[:,:,:,0]/dz,dMdz[:,:,:,1]/dz,dMdz[:,:,:,2]/dz

    div = Numeric.zeros( (Nx,Ny,Nz), 'd' )

    div[1:-1,:,:] += dMxdx
    div[:,1:-1,:] += dMydy
    div[:,:,1:-1] += dMzdz

    if not surfaceEffects:
        div = clean_surfaces( div, M, wipe=1 )

    Fdiv = convert_C_to_fortran( div )
    divflat = convert_fortran_3dmatrix_to_flat( Fdiv )

    rot = Numeric.zeros( (Nx,Ny,Nz,3), 'd' )

    #taking the cross product (this excludes the outermost layers as
    #we can't take the central difference for these)
    rot[1:-1,1:-1,1:-1,0] = dMzdy[1:-1,:,1:-1]-dMydz[1:-1,1:-1,:]
    rot[1:-1,1:-1,1:-1,1] = dMxdz[1:-1,1:-1,:]-dMzdx[:,1:-1,1:-1]
    rot[1:-1,1:-1,1:-1,2] = dMydx[:,1:-1,1:-1]-dMxdy[1:-1,:,1:-1]

    #special 2d-case (only one layer in z)
    if Nz == 1:
        print "-->Nz==1, special 2d case, will only compute z-component of curl"
        rot[ 1:-1, 1:-1, 0, 2] = dMydx[:,1:-1,0]-dMxdy[1:-1,:,0]

    if not surfaceEffects:
        rot = clean_surfaces( rot, M, wipe=1 )

    Frot = convert_C_to_fortran( rot )
    rotflat = convert_fortran_3dmatrix_to_flat_vector( Frot )

    rotmag = magnitude( rotflat )

    return (divflat, rotflat, rotflat[:,0], rotflat[:,1], rotflat[:,2], rotmag)
