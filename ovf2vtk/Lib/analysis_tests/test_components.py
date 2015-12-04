import numpy as np

from ovf2vtk import analysis

"""functions to test the components function within the analysis file for
ovf2vtk. By Harry Wilson. Last Updated 02/12/2015."""


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
