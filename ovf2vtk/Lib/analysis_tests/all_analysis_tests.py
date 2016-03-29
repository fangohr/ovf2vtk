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
