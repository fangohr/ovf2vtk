import numpy as np

from ovf2vtk import analysis

"""functions to test the convert_fortran_3Dmatrix_to_flat_vector function
within the analysis file for ovf2vtk. By Harry Wilson. Last Updated 02/12/2015.
"""


def test_f3Dm2fv():

    # shape = (2, 3)

    M = np.ones((2, 3))
    # compute expected length of flattened array
    x = 1
    for i in M.shape:
        x = x * i
    # compute actual length of flattened array
    Mrav = M.ravel()
    # compare expected vs actual
    assert int(x) == len(Mrav)
    # compute actual returned function
    flatv = analysis.convert_fortran_3dmatrix_to_flat_vector(M)
    # check if returned value is a numpy array
    assert isinstance(flatv, np.ndarray)
    # assert returned array of required shape
    assert flatv.shape == (long(x)/3, long(3))

    # shape = (4, 7)

    M = np.ones((4, 7))
    # compute expected length of flattened array
    x = 1
    for i in M.shape:
        x = x * i
    # compute actual length of flattened array
    Mrav = M.ravel()
    # compare expected vs actual
    assert int(x) == len(Mrav)
    # compute actual returned function
    flatv = analysis.convert_fortran_3dmatrix_to_flat_vector(M)
    # check if returned value is a numpy array
    assert isinstance(flatv, np.ndarray)
    # assert returned array of required shape
    assert flatv.shape == (long(x)/3, long(3))

    # shape = (20, 35) with negative entries

    M = np.ones((20, 35))
    # compute expected length of flattened array
    x = 1
    for i in M.shape:
        x = x * i
    # compute actual length of flattened array
    Mrav = M.ravel()
    # compare expected vs actual
    assert int(x) == len(Mrav)

    # compute actual returned function
    flatv = analysis.convert_fortran_3dmatrix_to_flat_vector(M)
    # check if returned value is a numpy array
    assert isinstance(flatv, np.ndarray)
    # assert returned array of required shape
    assert flatv.shape == (long(x)/3, long(3))


def test_f3Dm2fv_bordercase():

    # shape = (1, 1)

    M = np.ones((1, 1))
    # compute expected length of flattened array
    x = 1
    for i in M.shape:
        x = x * i
    # compute actual length of flattened array
    Mrav = M.ravel()
    # compare expected vs actual
    assert int(x) == len(Mrav)

    # compute actual returned function
    flatv = analysis.convert_fortran_3dmatrix_to_flat_vector(M)
    # check if returned value is a numpy array
    assert isinstance(flatv, np.ndarray)
    # assert returned array of required shape
    assert int(x) < 3
    assert flatv.shape == (long(x)/3,)

    # shape = (0)

    M = np.ones((0))
    # compute expected length of flattened array
    x = 1
    for i in M.shape:
        x = x * i
    # compute actual length of flattened array
    Mrav = M.ravel()
    # compare expected vs actual
    assert int(x) == len(Mrav)

    # compute actual returned function
    flatv = analysis.convert_fortran_3dmatrix_to_flat_vector(M)
    # check if returned value is a numpy array
    assert isinstance(flatv, np.ndarray)
    # assert returned array of required shape
    assert int(x) < 3
    assert flatv.shape == (long(x)/3, long(3))

    # shape = (1, 2):

    M = np.ones((1, 2))
    # compute expected length of flattened array
    x = 1
    for i in M.shape:
        x = x * i
    # compute actual length of flattened array
    Mrav = M.ravel()
    # compare expected vs actual
    assert int(x) == len(Mrav)

    # compute actual returned function
    flatv = analysis.convert_fortran_3dmatrix_to_flat_vector(M)
    # check if returned value is a numpy array
    assert isinstance(flatv, np.ndarray)
    # assert returned array of required shape
    assert int(x) < 3
    assert flatv.shape == (long(x)/3,)
    