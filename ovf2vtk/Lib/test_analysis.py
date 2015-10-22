import math

import numpy as np

import analysis


def test_magnitude_n():

    # n = 3

    x = np.array([[1, 2, 3.]])
    # requirement for magnitude:
    assert x.shape == (1, 3)

    # compute result we expect
    y1 = math.sqrt(1 ** 2 + 2 ** 2 + 3 ** 2)

    # compute actual result from analysis.magnitude
    y2 = analysis.magnitude(x)
    assert y1 == float(y2)

    # n = 5
    x = np.array([[1, 2, 3., 0.1, 0]])
    # requirement for magnitude:
    assert x.shape == (1, 5)

    # compute result we expect
    y1 = math.sqrt(1 ** 2 + 2 ** 2 + 3 ** 2 + 0.1 ** 2 + 0 ** 2)

    # compute actual result from analysis.magnitude
    y2 = analysis.magnitude(x)
    assert y1 == float(y2)

    # n = 3, with negative entries

    x = np.array([[-1, -2, 3.]])
    # requirement for magnitude:
    assert x.shape == (1, 3)

    # compute result we expect
    y1 = math.sqrt((-1) ** 2 + (-2) ** 2 + 3. ** 2)

    # compute actual result from analysis.magnitude
    y2 = analysis.magnitude(x)
    assert y1 == float(y2)
