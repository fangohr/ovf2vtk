import numpy as np

from ovf2vtk import analysis


def test_mag(x):
    """Testing the magnitude function within analysis.py for the ovf2vtk
    software. By Harry Wilson. Last updated 05/11/15"""
    mag = analysis.magnitude

# check input and output of function is a numpy array
    assert type(x) == type(mag(x)) == np.ndarray

# check input is correct array shape i.e. (1 X N)
# check output is correct array shape i.e. (1L)
    n = x.size
    assert x.shape == (long(1), long(n))
    assert mag(x).shape == (long(1),)

# check output as expected for initial inputted array
    xa = x**2.
    xb = xa.sum()
    xc = np.sqrt(xb)
    assert xc == mag(x)[0]

# check output as expected for a selection of alternative inputs
    y1 = np.array([[5., 39., 104.]])
    y2 = np.array([[-3., -10., -51.]])
    y3 = np.array([[0., 0., 0.]])
    y4 = np.array([[29., 0., 54.]])
    y5 = np.array([[16., -27., 0.]])
    yn = (y1, y2, y3, y4, y5)
    for y in yn:
        yabs = abs(y)
        ya = yabs**2.
        yb = ya.sum()
        yc = np.sqrt(yb)
        assert yc == mag(y)[0]

    print 'pass'
