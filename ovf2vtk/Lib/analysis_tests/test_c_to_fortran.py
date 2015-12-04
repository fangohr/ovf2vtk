import numpy as np

from ovf2vtk import analysis

"""functions to test the convert_C_to_Fortran function within the analysis file
for ovf2vtk. By Harry Wilson. Last Updated 02/12/2015."""


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