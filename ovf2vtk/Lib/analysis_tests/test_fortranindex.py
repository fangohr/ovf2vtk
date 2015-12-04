import numpy as np

from ovf2vtk import analysis

"""functions to test the fortranindex function within the analysis file
for ovf2vtk. By Harry Wilson. Last Updated 03/12/2015."""


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