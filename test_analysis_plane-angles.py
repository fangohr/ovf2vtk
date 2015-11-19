import numpy as np

from ovf2vtk import analysis


def test_plane_angles(d):
    """Testing the plane_angles function within analysis.py for the ovf2vtk
    software. By Harry Wilson. Last updated 09/11/15"""

# check array type and shape is correct for a 3d vector [1L X (N+3)L]
    assert type(d) == np.ndarray
    assert d.shape[0] == long(1)
    assert d.shape[1] >= long(3)

# check output as expected for initial inputted array
    x = d.item(0)
    y = d.item(1)
    z = d.item(2)
    comps = [x, y, z]

    for i in comps:             # if component of vector less than cutoff...
        if abs(i) < 1e-6:       # ...size of 1e-6 then assume value of 0.
            i = np.array([0.0])
        else:
            i = np.array([i])

    xy = np.arctan2(y, x)
    yz = np.arctan2(z, y)
    xz = np.arctan2(z, x)

    angles = (xy, yz, xz)
    plangs = analysis.plane_angles(d)
    assert angles == plangs

# check output as expected for a selection of alternative inputs
    y1 = np.array([[5., 39., 104.]])
    y2 = np.array([[-3., -10., -51.]])
    y3 = np.array([[0., 0., 0.]])
    y4 = np.array([[29., 0., 54.]])
    y5 = np.array([[16., -27., 0.]])
    yn = (y1, y2, y3, y4, y5)
    for i in yn:
        assert type(i) == np.ndarray
        assert i.shape[0] == long(1)
        assert i.shape[1] >= long(3)

        xn = i.item(0)
        yn = i.item(1)
        zn = i.item(2)
        compsn = [xn, yn, zn]

        for j in compsn:
            if abs(j) < 1e-6:
                j = np.array([0.0])
            else:
                j = np.array([j])

        xyn = np.arctan2(yn, xn)
        yzn = np.arctan2(zn, yn)
        xzn = np.arctan2(zn, xn)

        anglesn = (xyn, yzn, xzn)
        assert anglesn == analysis.plane_angles(i)

    print 'pass'