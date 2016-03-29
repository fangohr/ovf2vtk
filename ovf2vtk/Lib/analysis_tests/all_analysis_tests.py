import math

import numpy as np

from ovf2vtk import analysis

"""all the tests developed for the analysis.py script for ovf2vtk stored in
one place. By Harry Wilson. Last updated 04/11/15"""

# ************************** Global Variables ************************** #

# vf is a flat matrix of shape (1xN), where the values listed are possible...
# ...values of N
vfs = 0, 1, 10, 100, 1000, 10000, 100000
# Selection of values possible for the cells Nx, Ny and Nz.
Nxs = 0, 1, 5, 15, 35
Nys = 0, 1, 6, 15, 30
Nzs = 0, 1, 7, 15, 25

# ******************************* Tests ******************************** #


def test_magnitude():
    """function expects an array of N 3D vectors"""

    # test bordercases and other arbitrary shapes
    shapes = (0, 1, 6, 60, 600, 6000)
    for shapeval in shapes:
        array = np.random.random_sample((shapeval, long(3)))
    # to include negative + larger values
    newarray = (array - 0.5) * 1000
    # ensure array of required shape
    assert newarray.shape == (long(shapeval), long(3))
    # compute expected result
    newarraysq = newarray ** 2
    exp = newarraysq.sum(1) ** 0.5
    # compute actual result
    act = analysis.magnitude(newarray)
    # ensure result is a numpy array
    assert isinstance(act, np.ndarray)
    # code works?
    assert exp.all() == act.all()


def test_convert_flat_fortran_to_3dmatrix():
    """vf is expected to be a flat matrix; Nx, Ny, and Nz are expected to be
    positive integers"""

    for vf in vfs:
        for i in range(5):
            # compute actual result
            act = analysis.convert_flat_fortran_to_3dmatrix(np.ones((vf, 1)), Nxs[i], Nys[i], Nzs[i])
            # check returned array of expected type and shape
            assert isinstance(act, np.ndarray)
            if i == 0 and vf != 0:
                # shape returned differs under these conditions
                assert act.shape == (long(0),)
            else:
                # expected shape returned
                assert act.shape == (long(Nzs[i]), long(Nys[i]), long(Nxs[i]), long(3))


def test_convert_fortran_3dmatrix_to_flat():
    """input, M, is a matrix of shape (Nz, Ny, Nx, 3) -> Fortran order;
    or shape (Nx, Ny, Nz, 3) -> C order"""

    for i in range(5):
        M = np.ndarray((Nzs[i], Nys[i], Nxs[i], 3))
        # compute actual result from tested function
        Mflat = analysis.convert_fortran_3dmatrix_to_flat(M)
        # test computed result is a numpy array
        assert isinstance(Mflat, np.ndarray)
        # compute length of flattened array by finding product of array shape
        length = 1
        for j in M.shape:
            length = length * j
        # test actual result is 1D with same length as expected
        assert (long(length),) == Mflat.shape


def test_convert_fortran_3dmatrix_to_flat_vector():
    """input, M, is a matrix of shape (Nz, Ny, Nx, 3) -> Fortran order;
    or shape (Nx, Ny, Nz, 3) -> C order"""

    for i in range(5):
        M = np.ndarray((Nzs[i], Nys[i], Nxs[i], 3))
        # compute expected length of flattened array
        length = 1
        for i in M.shape:
            length = length * i
        # compute actual length of flattened array
        Mlength = M.ravel()
        # compare expected vs actual
        assert int(length) == len(Mlength)
        # compute actual returned function
        flatv = analysis.convert_fortran_3dmatrix_to_flat_vector(M)
        # check if returned value is a numpy array
        assert isinstance(flatv, np.ndarray)
        # assert returned array of required shape
        assert flatv.shape == (long(length)/3, long(3))


def test_convert_fortran_to_c():
    """input, a, is a matrix of shape (Nz, Ny, Nx, 3) -> Fortran order;
    or shape (Nx, Ny, Nz, 3) -> C order"""

    for i in range(5):
        a = np.random.random_sample((Nzs[i], Nys[i], Nxs[i], 3))
        # to include negative + larger values
        a1 = (a - 0.5) * 1000
        # compute expected shape result
        exp = np.ndarray((Nxs[i], Nys[i], Nzs[i], 3))
        # compute expected shape result
        act = analysis.convert_fortran_to_C(a1)
        # check act and exp have same shape
        assert exp.shape == act.shape
        # check values transpose correctly
        for x in range(Nxs[i]):
            for y in range(Nys[i]):
                for z in range(Nzs[i]):
                    for w in range(3):
                        assert a1[z, y, x, w] == act[x, y, z, w]


def test_convert_c_to_fortran():
    """input, a, is a matrix of shape (Nz, Ny, Nx, 3) -> Fortran order;
    or shape (Nx, Ny, Nz, 3) -> C order"""

    for i in range(5):
        a = np.random.random_sample((Nzs[i], Nys[i], Nxs[i], 3))
        # to include negative + larger values
        a1 = (a - 0.5) * 1000
        # compute expected shape result
        exp = np.ndarray((Nxs[i], Nys[i], Nzs[i], 3))
        # compute expected shape result
        act = analysis.convert_C_to_fortran(a1)
        # check act and exp have same shape
        assert exp.shape == act.shape
        # check values transpose correctly
        for x in range(Nxs[i]):
            for y in range(Nys[i]):
                for z in range(Nzs[i]):
                    for w in range(3):
                        assert a1[z, y, x, w] == act[x, y, z, w]


def test_components():

    shapes = [(2, 3), (2, 3, 4), (2, 3, 4, 5), (2, 3, 4, 5, 6)]

    for shape in shapes:
        d = np.random.random_integers(1, 10, shape)
        # check input is an array
        assert isinstance(d, np.ndarray)
        # check array of required shape
        assert d.shape[-1] >= long(3)
        # compute expected result
        dexp = (d[:, 0],  d[:, 1],  d[:, 2])
        # compute actual result
        dact = analysis.components(d)
        # check returned value is array
        assert isinstance(dact, tuple)
        # check results are identical
        for i in range(len(dexp)):
            assert dexp[i].any() == dact[i].any()
