import numpy as np

from ovf2vtk import analysis

"""functions to test the convert_fortran_3Dmatrix_to_flat function within the
analysis file for ovf2vtk. By Harry Wilson. Last Updated 02/12/2015."""


def test_f3D2f():

    # shape = (1, 2)

    M = np.ones((1, 2))
    # compute actual result from tested function
    Mrav = analysis.convert_fortran_3dmatrix_to_flat(M)
    # test computed result is a numpy array
    assert isinstance(Mrav, np.ndarray)
    # compute length of flattened array
    x = 1
    for i in M.shape:
        x = x * i
    # test actual result is 1D with same length as expected
    assert (long(x),) == Mrav.shape

    # shape = (1, 2, 3)

    M = np.ones((1, 2, 3))
    # compute actual result from tested function
    Mrav = analysis.convert_fortran_3dmatrix_to_flat(M)
    # test computed result is a numpy array
    assert isinstance(Mrav, np.ndarray)
    # compute length of flattened array
    x = 1
    for i in M.shape:
        x = x * i
    # test actual result is 1D with same length as expected
    assert (long(x),) == Mrav.shape

    # test shapes between 4D and 10D

    for S in range(4, 11, 1):
        M = np.ones(tuple(range(1, S+1, 1)))
        # compute actual result from tested function
        Mrav = analysis.convert_fortran_3dmatrix_to_flat(M)
        # test computed result is a numpy array
        assert isinstance(Mrav, np.ndarray)
        # compute length of flattened array
        x = 1
        for i in M.shape:
            x = x * i
        # test actual result is 1D with same length as expected
        assert (long(x),) == Mrav.shape


def test_f3D2f_bordercase():

    # shape = (1, 1)

    M = np.ones((1, 1))
    # compute actual result from tested function
    Mrav = analysis.convert_fortran_3dmatrix_to_flat(M)
    # test computed result is a numpy array
    assert isinstance(Mrav, np.ndarray)
    # compute length of flattened array
    x = 1
    for i in M.shape:
        x = x * i
    # test actual result is 1D with same length as expected
    assert (long(x),) == Mrav.shape

    # shape = (0)

    M = np.ones((0))
    # compute actual result from tested function
    Mrav = analysis.convert_fortran_3dmatrix_to_flat(M)
    # test computed result is a numpy array
    assert isinstance(Mrav, np.ndarray)
    # compute length of flattened array
    x = 1
    for i in M.shape:
        x = x * i
    # test actual result is 1D with same length as expected
    assert (long(x),) == Mrav.shape
        