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


def test_magnitude_bordercase():
    # n = 1

    x = np.array([[1.34]])
    # requirement for magnitude:
    assert x.shape == (1, 1)

    # compute result we expect
    y1 = math.sqrt(1.34 ** 2)

    # compute actual result from analysis.magnitude
    y2 = analysis.magnitude(x)
    assert y1 == float(y2)

    # n = 0

    x = np.array([[]])
    # requirement for magnitude:
    assert x.shape == (1, 0)

    # compute result we expect
    y1 = 0

    # compute actual result from analysis.magnitude
    y2 = analysis.magnitude(x)
    assert y1 == float(y2)


def test_magnitude_return_type():
    x = np.array([[1]])
    y = analysis.magnitude(x)

    # make sure return value is numpy array
    assert isinstance(y, np.ndarray)

    # assert shape is as expected
    assert y.shape == (1,)

    for N in range(0, 10):
        x = np.array([[1] * N])
        y = analysis.magnitude(x)

        # make sure return value is numpy array
        assert isinstance(y, np.ndarray)

        # assert shape is as expected
        assert y.shape == (1,)
