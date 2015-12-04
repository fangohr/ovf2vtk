import numpy as np

from ovf2vtk import analysis

"""functions to test the convert_flat_fortran_to_3Dmatrix function within the
analysis file for ovf2vtk. By Harry Wilson. Last Updated 02/12/2015."""


def test_ff23Dm():

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
 