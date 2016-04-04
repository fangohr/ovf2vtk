import math

import numpy as np

from ovf2vtk import analysis

"""all the tests developed for the analysis.py script for ovf2vtk stored in
one place. By Harry Wilson. Last updated 04/11/15"""

# ************************** Global Variables ************************** #

# vf (vector field) is a flat matrix of shape (Nx3), where the values...
# ...listed are possible values of N
vfshapes = 0, 1, 10, 100, 1000, 10000, 100000
# Selection of values possible for the cells Nx, Ny and Nz.
Nxs = 0, 1, 5, 15, 35
Nys = 0, 1, 6, 15, 30
Nzs = 0, 1, 7, 15, 25
vfexample1 = np.array([[2.53, 37546.233, 254e-10], [1e-6, -55.333, -29.645],
                       [1.45e-22, 22.4e-9, 1e-7], [1.45e-6, -22.4e-9, 1e-7],
                       [1e-9, 1e-9, 1e-9], [0., 0., 0.], [1e-6, -1e-6, 1e-6],
                       [5.7735e-6, -5.7735e-6, 5.7735e-6]])
obs_example_shapes = (3, 3), (3, 3, 3), (3, 3, 3, 3), (3, 3, 3, 3, 3)
# ******************************* Tests ******************************** #


def test_magnitude():
    """function expects an array of N 3D vectors"""

    # test bordercases and other arbitrary shapes
    for vf in vfshapes:
        array = np.random.random_sample((vf, 3))
        # to include negative + larger values
        newarray = (array - 0.5) * 1000
        # ensure array of required shape
        assert newarray.shape == (long(vf), long(3))
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
    """vf is expected to be an array of N 3D vectors; Nx, Ny, and Nz are
    expected to be positive integers"""

    for vf in vfshapes:
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
    "input is an array of N 3d vectors"""

    for vf in vfshapes:
        d = np.random.random_sample((vf, 3))
        # to include negative + larger values
        d1 = (d - 0.5) * 1000
        # compute expected result
        vfi = vfj = vfk = np.ndarray((1, vf))
        if vf == 0:
            vfi = vfj = vfk = np.ndarray((0, 3))
        else:
            for i in range(vf):
                vfi[0, i], vfj[0, i], vfk[0, i], = d1[i, 0], d1[i, 1], d1[i, 2]
        exp = (vfi, vfj, vfk)
        # compute actual result
        act = analysis.components(d1)
        # check returned value is tuple
        assert isinstance(act, tuple)
        # check results are identical
        for f in range(3):
            assert exp[f].all() == act[f].all()


def test_plane_angles():
    """input is an array of N 3d vectors"""

    # test random samples first
    for vf in vfshapes:
        array = np.random.random_sample((vf, 3))
        # to include negative + larger values
        newarray = (array - 0.5) * 1000
        # compute actual result
        act = analysis.plane_angles(newarray)
        # check return type is tuple of length 3 and that each item in tuple...
        # ...is an array of expected length
        assert isinstance(act, tuple)
        assert len(act) == int(3)
        for i in range(len(act)):
            assert isinstance(act[i], np.ndarray)
            assert len(act[i]) == vf

    # test specific example to ensure values of array are as expected
    # compute actual result
    act = analysis.plane_angles(vfexample1)
    expected = (np.array([1.57072894, -1.57079631, 0., -0.01544705, 0., 0.,
                          -0.78539816, -0.78539816]),
                np.array([6.76499291e-13, -2.64975088e+00, 0.00000000e+00,
                          1.79115875e+00, 0.00000000e+00, 0.00000000e+00,
                          2.35619449e+00, 2.35619449e+00]),
                np.array([1.00395257e-08, -1.57079629e+00, 0.00000000e+00,
                          6.88564893e-02, 0.00000000e+00, 0.00000000e+00,
                          7.85398163e-01, 7.85398163e-01]))
    for j in range(len(act)):
        assert act[j].all() == expected[j].all()
        

def test_clean_surfaces():
    