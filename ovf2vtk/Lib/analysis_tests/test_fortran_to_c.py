import numpy as np

from ovf2vtk import analysis

"""functions to test the convert_fortran_to_C function within the analysis file
for ovf2vtk. By Harry Wilson. Last Updated 02/12/2015."""


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