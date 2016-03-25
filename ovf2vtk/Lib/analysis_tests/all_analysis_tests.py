import math

import numpy as np

from ovf2vtk import analysis

"""all the tests developed for the analysis.py script for ovf2vtk stored in
one place. By Harry Wilson. Last updated 04/11/15"""


"""magnitude"""


def test_magnitude():
    """function expects an array of 1xN 3D vectors"""

    # test bordercases and other arbitrary shapes
    shapes = (0, 1, 6, 60, 600, 6000)
    for shapeval in shapes:
        array = np.random.random_sample((1, shapeval))
    # to include negative + larger values
    newarray = (array - 0.5) * 1000
    # ensure array of required shape
    assert newarray.shape == (long(1), long(shapeval))
    # compute expected result
    newarraysq = newarray ** 2
    exp = newarraysq.sum(1) ** 0.5
    # compute actual result
    act = analysis.magnitude(newarray)
    # ensure result is a numpy array
    assert isinstance(act, np.ndarray)
    # code works?
    assert exp == act


def test_convert_flat_fortran_to_3Dmatrix():
    """vf is expected to be a flat matri; Nx, Ny, and Nz are expected to be
    positive integers"""

    # shape = (1, 3)

    vf = np.array([1, 2, 3])
    # select arbitrary node values
    Nx, Ny, Nz = 10, 10, 10
    # compute actual result from tested function
    A = analysis.convert_flat_fortran_to_3dmatrix(vf, Nx, Ny, Nz)
    # ensure returned value A is numpy array
    assert isinstance(A, np.ndarray)
    # compare expected shape to one computed
    assert A.shape == (long(Nz), long(Ny), long(Nx), 3)

    # shape = (5, 1)

    vf = np.array([[1], [2], [3], [4], [5]])
    # select arbitrary node values
    Nx, Ny, Nz = 5, 5, 5
    # compute actual result from tested function
    A = analysis.convert_flat_fortran_to_3dmatrix(vf, Nx, Ny, Nz)
    # ensure returned value A is numpy array
    assert isinstance(A, np.ndarray)
    # compare expected shape to one computed
    assert A.shape == (long(Nz), long(Ny), long(Nx), 3)

    # shape = (3, 7, 2)

    vf = np.random.random_sample((3, 7, 2))
    # select arbitrary node values
    Nx, Ny, Nz = 15, 15, 15
    # compute actual result from tested function
    A = analysis.convert_flat_fortran_to_3dmatrix(vf, Nx, Ny, Nz)
    # ensure returned value A is numpy array
    assert isinstance(A, np.ndarray)
    # compare expected shape to one computed
    assert A.shape == (long(Nz), long(Ny), long(Nx), 3)

    # shape = (3, 7, 4, 2), different node values

    vf = np.random.random_sample((3, 7, 4, 2))
    # select arbitrary node values
    Nx, Ny, Nz = 5, 10, 15
    # compute actual result from tested function
    A = analysis.convert_flat_fortran_to_3dmatrix(vf, Nx, Ny, Nz)
    # ensure returned value A is numpy array
    assert isinstance(A, np.ndarray)
    # compare expected shape to one computed
    assert A.shape == (long(Nz), long(Ny), long(Nx), 3)


def test_ff23Dm_bordercase():

    # shape = (1, 1)

    vf = np.array([1])
    # select arbitrary node values
    Nx, Ny, Nz = 5, 10, 15
    # compute actual result from tested function
    A = analysis.convert_flat_fortran_to_3dmatrix(vf, Nx, Ny, Nz)
    # ensure returned value A is numpy array
    assert isinstance(A, np.ndarray)
    # compare expected shape to one computed
    assert A.shape == (long(Nz), long(Ny), long(Nx), 3)

    # shape = (0)

    vf = np.array([])
    # select arbitrary node values
    Nx, Ny, Nz = 5, 10, 15
    # compute actual result from tested function
    A = analysis.convert_flat_fortran_to_3dmatrix(vf, Nx, Ny, Nz)
    # ensure returned value A is numpy array
    assert isinstance(A, np.ndarray)
    # compare expected shape to one computed
    assert A.shape == (long(Nz), long(Ny), long(Nx), 3)


"""fortran_3Dmatrix_to_flat"""


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


"""fortran_3Dmatrix_to_flat_vector"""


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


"""fortran_to_c"""


def test_f2c():

    # check values return as expected

    # shape = (3, 1, 3)

    a = np.array([[[1, 2, 3]], [[4, 5, 6]], [[7, 8, 9]]])
    # input required to be a 3D matrix at minimum
    assert a.shape[0] >= long(3)
    # check matrix contains 3D vectors only
    assert a.shape[-1] == long(3)
    # compute actual result
    Cact = analysis.convert_fortran_to_C(a)
    # check array shape is correct
    assert Cact.shape == (a.shape[2], a.shape[1], a.shape[0])
    # expected result
    Cexp = np.array([[[1, 4, 7]], [[2, 5, 8]], [[3, 6, 9]]])
    # assert expected and actual result are identical
    assert Cexp.all() == Cact.all()

    # shape = (4, 1, 9, 3). Try with floated values and negatives

    a = np.array([[[[-2.5, -2.0, -1.5], [-1.0, -0.5, 0], [0.5, 1.0, 1.5],
                    [-2.5, -2.0, -1.5], [-1.0, -0.5, 0], [0.5, 1.0, 1.5],
                    [-2.5, -2.0, -1.5], [-1.0, -0.5, 0], [0.5, 1.0, 1.5]]],
                  [[[-2.5, -2.0, -1.5], [-1.0, -0.5, 0], [0.5, 1.0, 1.5],
                    [-2.5, -2.0, -1.5], [-1.0, -0.5, 0], [0.5, 1.0, 1.5],
                    [-2.5, -2.0, -1.5], [-1.0, -0.5, 0], [0.5, 1.0, 1.5]]],
                  [[[-2.5, -2.0, -1.5], [-1.0, -0.5, 0], [0.5, 1.0, 1.5],
                    [-2.5, -2.0, -1.5], [-1.0, -0.5, 0], [0.5, 1.0, 1.5],
                    [-2.5, -2.0, -1.5], [-1.0, -0.5, 0], [0.5, 1.0, 1.5]]],
                  [[[-2.5, -2.0, -1.5], [-1.0, -0.5, 0], [0.5, 1.0, 1.5],
                    [-2.5, -2.0, -1.5], [-1.0, -0.5, 0], [0.5, 1.0, 1.5],
                    [-2.5, -2.0, -1.5], [-1.0, -0.5, 0], [0.5, 1.0, 1.5]]]])
    # input required to be a 3D matrix at minimum
    assert a.shape[0] >= long(3)
    # check matrix contains 3D vectors only
    assert a.shape[-1] == long(3)
    # compute actual result
    Cact = analysis.convert_fortran_to_C(a)
    # check array shape is correct
    assert Cact.shape == (a.shape[2], a.shape[1], a.shape[0], a.shape[3])
    # expected result
    Cexp = np.array([[[[-2.5, -2., -1.5],
                       [-2.5, -2., -1.5],
                       [-2.5, -2., -1.5],
                       [-2.5, -2., -1.5]]],
                     [[[-1., -0.5, 0.],
                       [-1., -0.5, 0.],
                       [-1., -0.5, 0.],
                       [-1., -0.5, 0.]]],
                     [[[0.5, 1., 1.5],
                       [0.5, 1., 1.5],
                       [0.5, 1., 1.5],
                       [0.5, 1., 1.5]]],
                     [[[-2.5, -2., -1.5],
                       [-2.5, -2., -1.5],
                       [-2.5, -2., -1.5],
                       [-2.5, -2., -1.5]]],
                     [[[-1., -0.5, 0.],
                       [-1., -0.5, 0.],
                       [-1., -0.5, 0.],
                       [-1., -0.5, 0.]]],
                     [[[0.5, 1., 1.5],
                       [0.5, 1., 1.5],
                       [0.5, 1., 1.5],
                       [0.5, 1., 1.5]]],
                     [[[-2.5, -2., -1.5],
                       [-2.5, -2., -1.5],
                       [-2.5, -2., -1.5],
                       [-2.5, -2., -1.5]]],
                     [[[-1., -0.5, 0.],
                       [-1., -0.5, 0.],
                       [-1., -0.5, 0.],
                       [-1., -0.5, 0.]]],
                     [[[0.5, 1., 1.5],
                       [0.5, 1., 1.5],
                       [0.5, 1., 1.5],
                       [0.5, 1., 1.5]]]])
    # assert expected and actual result are identical
    assert Cexp.all() == Cact.all()

    # check shape returned is as expected

    # shape = (4, 5, 6, 7)

    a = np.ones((4, 5, 6, 7))
    # compute actual result
    Cact = analysis.convert_fortran_to_C(a)
    # check shape of result is as expected
    assert Cact.shape == (long(6), long(5), long(4), long(7))

    # shape = (5, 1, 9, 8, 5)

    a = np.ones((5, 1, 9, 8, 5))
    # compute actual result
    Cact = analysis.convert_fortran_to_C(a)
    # check shape of result is as expected
    assert Cact.shape == (long(9), long(1), long(5), long(8), long(5))


"""c_to_fortran"""


def test_c2f():

    # check values return as expected

    # shape (3, 1, 3)

    a = np.array([[[1, 2, 3]], [[4, 5, 6]], [[7, 8, 9]]])
    # compute actual result
    Xact = analysis.convert_C_to_fortran(a)
    # compute expected result
    Xexp = analysis.convert_fortran_to_C(a)
    # ensure actual and expected are identical
    assert Xact.all() == Xexp.all()

    # check shape returns as expected

    # shape (3, 4, 5)

    a = np.ones((3, 4, 5))
    # compute actual result
    Xact = analysis.convert_C_to_fortran(a)
    # check its shape
    assert Xact.shape == (long(5), long(4), long(3))
    # compute expected result
    Xexp = analysis.convert_fortran_to_C(a)
    # ensure actual and expected are identical
    assert Xact.all() == Xexp.all()

    # shape (3, 4, 5)

    a = np.ones((1, 6, 4, 5))
    # compute actual result
    Xact = analysis.convert_C_to_fortran(a)
    # check its shape
    assert Xact.shape == (long(4), long(6), long(1), long(5))
    # compute expected result
    Xexp = analysis.convert_fortran_to_C(a)
    # ensure actual and expected are identical
    assert Xact.all() == Xexp.all()


"""fortanindex"""


def test_fortranindex():

    # Nx, Ny, Nz identical
    # i, j, k are arrays

    Nx, Ny, Nz = 7.5, 7.5, 7.5
    i = 10 * np.random.random_sample(size=(1, 3))
    j = 10 * np.random.random_sample(size=(1, 3))
    k = 10 * np.random.random_sample(size=(1, 3))
    # compute expected result
    exp = i + j * Nx + k * Nx * Ny
    # check output is array
    assert isinstance(exp, np.ndarray)
    # check computed result identical to returned value
    act = analysis.fortranindex(i, j, k, Nx, Ny, Nz)
    assert exp.all() == act.all()

    # Nx, Ny, Nz different
    # i, j, k varying shapes

    Nx, Ny, Nz = 27.3, 8.8, 15.3
    i = 10 * np.random.random_sample(size=(2, 3))
    j = 10 * np.random.random_sample(size=(5, 2, 3))
    k = 10 * np.random.random_sample(size=(3, 5, 2, 3))
    # compute expected result
    exp = i + j * Nx + k * Nx * Ny
    # check output is array
    assert isinstance(exp, np.ndarray)
    # check computed result identical to returned value
    act = analysis.fortranindex(i, j, k, Nx, Ny, Nz)
    assert exp.all() == act.all()

    # Nx, Ny, Nz different
    # i, j, k floated values

    Nx, Ny, Nz = float(5), float(26.7), float(2.3)
    i, j, k = float(31.3), float(1.5), float(16)
    # compute expected result
    exp = i + j * Nx + k * Nx * Ny
    # check output is array
    assert isinstance(exp, float)
    # check computed result identical to returned value
    act = analysis.fortranindex(i, j, k, Nx, Ny, Nz)
    assert exp == act


def test_fortanindex_bordercase():

        # Nx, Ny, Nz = 1
        # i, j, k = arrays of shape((1))

        Nx, Ny, Nz = 1, 1, 1
        i = 10 * np.random.random_sample(size=(1))
        j = 10 * np.random.random_sample(size=(1))
        k = 10 * np.random.random_sample(size=(1))
        # compute expected result
        exp = i + j * Nx + k * Nx * Ny
        # check output is array
        assert isinstance(exp, np.ndarray)
        # check computed result identical to returned value
        act = analysis.fortranindex(i, j, k, Nx, Ny, Nz)
        assert exp.all() == act.all()

        # Nx, Ny, Nz = 0
        # i, j , k = empty arrays

        Nx, Ny, Nz = 0, 0, 0
        i = 10 * np.random.random_sample(size=(0))
        j = 10 * np.random.random_sample(size=(0))
        k = 10 * np.random.random_sample(size=(0))
        # compute expected result
        exp = i + j * Nx + k * Nx * Ny
        # check output is array
        assert isinstance(exp, np.ndarray)
        # check computed result identical to returned value
        act = analysis.fortranindex(i, j, k, Nx, Ny, Nz)
        assert exp.all() == act.all()

        # Nx, Ny, Nz = 0
        # i, j, k = 0

        Nx, Ny, Nz = float(0), float(0), float(0)
        i, j, k = float(0), float(0), float(0)
        # compute expected result
        exp = i + j * Nx + k * Nx * Ny
        # check output is array
        assert isinstance(exp, float)
        # check computed result identical to returned value
        act = analysis.fortranindex(i, j, k, Nx, Ny, Nz)
        assert exp == act


"""Cindex"""


def test_Cindex():

    # Nx, Ny, Nz identical
    # i, j, k are arrays

    Nx, Ny, Nz = 7.5, 7.5, 7.5
    i = 10 * np.random.random_sample(size=(1, 3))
    j = 10 * np.random.random_sample(size=(1, 3))
    k = 10 * np.random.random_sample(size=(1, 3))
    # compute expected result
    exp = i * Nz * Ny + j * Nz + k
    # check output is array
    assert isinstance(exp, np.ndarray)
    # check computed result identical to returned value
    act = analysis.Cindex(i, j, k, Nx, Ny, Nz)
    assert exp.all() == act.all()

    # Nx, Ny, Nz different
    # i, j, k varying shapes

    Nx, Ny, Nz = 27.3, 8.8, 15.3
    i = 10 * np.random.random_sample(size=(2, 3))
    j = 10 * np.random.random_sample(size=(5, 2, 3))
    k = 10 * np.random.random_sample(size=(3, 5, 2, 3))
    # compute expected result
    exp = i * Nz * Ny + j * Nz + k
    # check output is array
    assert isinstance(exp, np.ndarray)
    # check computed result identical to returned value
    act = analysis.Cindex(i, j, k, Nx, Ny, Nz)
    assert exp.all() == act.all()

    # Nx, Ny, Nz different
    # i, j, k floated values

    Nx, Ny, Nz = float(5), float(26.7), float(2.3)
    i, j, k = float(31.3), float(1.5), float(16)
    # compute expected result
    exp = i * Nz * Ny + j * Nz + k
    # check output is array
    assert isinstance(exp, float)
    # check computed result identical to returned value
    act = analysis.Cindex(i, j, k, Nx, Ny, Nz)
    assert exp == act


def test_Cindex_bordercase():

        # Nx, Ny, Nz = 1
        # i, j, k = arrays of shape((1))

        Nx, Ny, Nz = 1, 1, 1
        i = 10 * np.random.random_sample(size=(1))
        j = 10 * np.random.random_sample(size=(1))
        k = 10 * np.random.random_sample(size=(1))
        # compute expected result
        exp = i * Nz * Ny + j * Nz + k
        # check output is array
        assert isinstance(exp, np.ndarray)
        # check computed result identical to returned value
        act = analysis.Cindex(i, j, k, Nx, Ny, Nz)
        assert exp.all() == act.all()

        # Nx, Ny, Nz = 0
        # i, j , k = empty arrays

        Nx, Ny, Nz = 0, 0, 0
        i = 10 * np.random.random_sample(size=(0))
        j = 10 * np.random.random_sample(size=(0))
        k = 10 * np.random.random_sample(size=(0))
        # compute expected result
        exp = i * Nz * Ny + j * Nz + k
        # check output is array
        assert isinstance(exp, np.ndarray)
        # check computed result identical to returned value
        act = analysis.Cindex(i, j, k, Nx, Ny, Nz)
        assert exp.all() == act.all()

        # Nx, Ny, Nz = 0
        # i, j, k = 0

        Nx, Ny, Nz = float(0), float(0), float(0)
        i, j, k = float(0), float(0), float(0)
        # compute expected result
        exp = i * Nz * Ny + j * Nz + k
        # check output is array
        assert isinstance(exp, float)
        # check computed result identical to returned value
        act = analysis.Cindex(i, j, k, Nx, Ny, Nz)
        assert exp == act


"""components"""


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
