import os
<<<<<<< HEAD

=======
>>>>>>> f88224be0f7551ada7d06eda673835f43be5858e
import sys
sys.path.append('..')

import numpy as np

import analysis_new as nana

import omfread_new as nomf

import analysis_original

"""all the tests developed for the analysis.py script for ovf2vtk stored in
one place. By Harry Wilson. Last updated 04/11/15"""

# ************************** Global Variables ************************** #

# vf (vector field) is a flat matrix of shape (Nx3), where the values...
# ...listed are possible values of N
vfshapes = 0, 1, 10, 100, 1000, 10000, 100000
# Selection of values possible for the cells Nx, Ny and Nz.
Nxs = 0, 1, 5, 15, 35
Nys = 0, 1, 6, 15, 30
Nzs = 0, 1, 7, 15, 25
vfexample1 = np.array([[2.53, 37546.233, 254e-10], [1e-6, -55.333, -29.645],
                       [1.45e-22, 22.4e-9, 1e-7], [1.45e-6, -22.4e-9, 1e-7],
                       [1e-9, 1e-9, 1e-9], [0., 0., 0.], [1e-6, -1e-6, 1e-6],
                       [5.7735e-6, -5.7735e-6, 5.7735e-6]])
vfexample2 = np.array([[-0.02570023, 0.71960652, -0.69390631],
                       [-0.02479932, 0.71918023, -0.69438088],
                       [-0.0239594, 0.71878195, -0.69482255],
                       [-0.02317449, 0.71840912, -0.69523466],
                       [0.54348832, 0.66789049, 0.50847095],
                       [0.53792924, 0.61900675, 0.57224363],
                       [0.57508606, 0.62426734, 0.52874029],
                       [0.57158923, 0.66120869, 0.48588967]])

M_example_shapes = (3, 3, 3, 3), (4, 4, 4, 4)
obs_example_shapes = ((3, 3), (3, 3, 3), (3, 4, 3), (3, 3, 3, 3),
                      (3, 3, 4, 5, 3))
M_shape_obs_shape_assertion = ['equal', 'notequal', 'equal', 'notequal',
                               'notequal', 'notequal', 'equal', 'notequal',
                               'equal', 'notequal']

# example inputs and outputs for obs and M

# shape (3, 3, 3)
obs_example_input1 = np.array([[[1, 2, 3], [4.5, 7.7, 123.4], [0, 33, -46]],
                              [[-10, -25, -1223], [0, 0, 0], [1, 1, 1]],
                              [[-2, 1, 4.5], [0, 1.2, 5], [7., 1.5, -7.6]]])

# shape (3, 3, 3, 3)
obs_example_input2 = np.array([[[[1, 2, 3], [4.5, 7.7, 123.4], [0, 33, -46]],
                                [[-10, -25, -1223], [0, 0, 0], [1, 1, 1]],
                                [[-2, 1, 4.5], [0, 1.2, 5], [7., 1.5, -7.6]]],
                               [[[1, 2, 3], [4.5, 7.7, 123.4], [0, 33, -46]],
                                [[-10, -25, -1223], [0, 0, 0], [1, 1, 1]],
                                [[-2, 1, 4.5], [0, 1.2, 5], [7., 1.5, -7.6]]],
                               [[[1, 2, 3], [4.5, 7.7, 123.4], [0, 33, -46]],
                                [[-10, -25, -1223], [0, 0, 0], [1, 1, 1]],
                                [[-2, 1, 4.5], [0, 1.2, 5], [7., 1.5, -7.6]]]])

# shape (3, 3, 3, 3)
M_example_input = np.array([[[[2.53, 3756.2, 254e-10], [1e-6, -55.33, -29.64],
                              [1.45e-22, 22.4e-9, 1e-7]],
                             [[1.45e-6, -22.4e-9, 1e-7], [1e-9, 1e-9, 1e-9],
                              [0., 0., 0.]],
                             [[1e-6, -1e-6, 1e-6], [-45.656, -50000, -6e-100],
                              [5.7735e-6, -5.7735e-6, 5.7735e-6]]],
                            [[[2.53, 3756.2, 254e-10], [1e-6, -55.33, -29.64],
                              [1.45e-22, 22.4e-9, 1e-7]],
                             [[1.45e-6, -22.4e-9, 1e-7], [1e-9, 1e-9, 1e-9],
                              [0., 0., 0.]],
                             [[1e-6, -1e-6, 1e-6], [-45.656, -50000, -6e-100],
                              [5.7735e-6, -5.7735e-6, 5.7735e-6]]],
                            [[[2.53, 3756.2, 254e-10], [1e-6, -55.33, -29.64],
                              [1.45e-22, 22.4e-9, 1e-7]],
                             [[1.45e-6, -22.4e-9, 1e-7], [1e-9, 1e-9, 1e-9],
                              [0., 0., 0.]],
                             [[1e-6, -1e-6, 1e-6], [-45.656, -50000, -6e-100],
                              [5.7735e-6, -5.7735e-6, 5.7735e-6]]]])

# example output for clean_surfaces() function using example obs and M above.
clean_surfaces_output1 = np. array([[[1., 2., 0.], [0., 0., 0.],
                                     [0., 33., 0.]],
                                    [[-10., -25., 0.], [0., 0., 0.],
                                     [0., 1., 0.]],
                                    [[-2., 1., 0.], [0., 0., 0.],
                                     [0., 1.5, 0.]]])

clean_surfaces_output2 = np.array([[[[1., 2., 3.], [4.5, 7.7, 123.4],
                                     [0., 0., 0.]],
                                    [[0., 0., 0.], [0., 0., 0.],
                                     [0., 0., 0.]],
                                    [[0., 0., 0.], [0., 1.2, 5.],
                                     [0., 0., 0.]]],
                                   [[[1., 2., 3.], [4.5, 7.7, 123.4],
                                     [0., 0., 0.]],
                                    [[0., 0., 0.], [0., 0., 0.],
                                     [0., 0., 0.]],
                                    [[0., 0., 0.], [0., 1.2, 5.],
                                     [0., 0., 0.]]],
                                   [[[1., 2., 3.], [4.5, 7.7, 123.4],
                                     [0., 0., 0.]],
                                    [[0., 0., 0.], [0., 0., 0.],
                                     [0., 0., 0.]],
                                    [[0., 0., 0.], [0., 1.2, 5.],
                                     [0., 0., 0.]]]])


# ******************************* Tests ******************************** #


def test_magnitude():
    """function expects an array of N 3D vectors"""

    # test bordercases and other arbitrary shapes
    for vf in vfshapes:
        array = np.random.random_sample((vf, 3))
        # to include negative + larger values
        newarray = (array - 0.5) * 1000
        # ensure array of required shape
        assert newarray.shape == (long(vf), long(3))
        # compute expected result
        newarraysq = newarray ** 2
        exp = newarraysq.sum(1) ** 0.5
        # compute actual result
        act = nana.magnitude(newarray)
        # ensure result is a numpy array
        assert isinstance(act, np.ndarray)
        # code works?
        assert exp.all() == act.all()


def test_convert_flat_fortran_to_3dmatrix():
    """vf is expected to be an array of N 3D vectors; Nx, Ny, and Nz are
    expected to be positive integers"""

    for vf in vfshapes:
        for i in range(5):
            # compute actual result
            act = nana.convert_flat_fortran_to_3dmatrix(np.ones((vf, 1)),
                                                        Nxs[i], Nys[i], Nzs[i])
            # check returned array of expected type and shape
            assert isinstance(act, np.ndarray)
            if i == 0 and vf != 0:
                # shape returned differs under these conditions
                assert act.shape == (long(0),)
            else:
                # expected shape returned
                assert act.shape == (long(Nzs[i]), long(Nys[i]), long(Nxs[i]),
                                     long(3))


def test_convert_fortran_3dmatrix_to_flat():
    """input, M, is a matrix of shape (Nz, Ny, Nx, 3) -> Fortran order;
    or shape (Nx, Ny, Nz, 3) -> C order"""

    for i in range(5):
        M = np.ndarray((Nzs[i], Nys[i], Nxs[i], 3))
        # compute actual result from tested function
        Mflat = nana.convert_fortran_3dmatrix_to_flat(M)
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
        flatv = nana.convert_fortran_3dmatrix_to_flat_vector(M)
        # check if returned value is a numpy array
        assert isinstance(flatv, np.ndarray)
        # assert returned array of required shape
        assert flatv.shape == (long(length)/3, long(3))


def test_convert_between_fortran_and_c():
    """input, a, is a matrix of shape (Nz, Ny, Nx, 3) -> Fortran order"""

    for i in range(5):
        a = np.random.random_sample((Nzs[i], Nys[i], Nxs[i], 3))
        # to include negative + larger values
        a1 = (a - 0.5) * 1000
        # compute expected shape result
        exp = np.ndarray((Nxs[i], Nys[i], Nzs[i], 3))
        # compute expected shape result
        act = nana.convert_between_fortran_and_C(a1)
        # check act and exp have same shape
        assert exp.shape == act.shape
        # check values transpose correctly
        for x in range(Nxs[i]):
            for y in range(Nys[i]):
                for z in range(Nzs[i]):
                    for w in range(3):
                        assert a1[z, y, x, w] == act[x, y, z, w]


def test_components():
    "input is an array of N 3d vectors"""

    for vf in vfshapes:
        d = np.random.random_sample((vf, 3))
        # to include negative + larger values
        d1 = (d - 0.5) * 1000
        # compute expected result
        vfi = vfj = vfk = np.ndarray((1, vf))
        if vf == 0:
            vfi = vfj = vfk = np.ndarray((0, 3))
        else:
            for i in range(vf):
                vfi[0, i], vfj[0, i], vfk[0, i], = d1[i, 0], d1[i, 1], d1[i, 2]
        exp = (vfi, vfj, vfk)
        # compute actual result
        act = nana.components(d1)
        # check returned value is tuple
        assert isinstance(act, tuple)
        # check results are identical
        for f in range(3):
            assert exp[f].all() == act[f].all()


def test_plane_angles():
    """input is an array of N 3d vectors"""

    # test random samples first
    for vf in vfshapes:
        array = np.random.random_sample((vf, 3))
        # to include negative + larger values
        newarray = (array - 0.5) * 1000
        # compute actual result
        act = nana.plane_angles(newarray)
        # check return type is tuple of length 3 and that each item in tuple...
        # ...is an array of expected length
        assert isinstance(act, tuple)
        assert len(act) == int(3)
        for i in range(len(act)):
            assert isinstance(act[i], np.ndarray)
            assert len(act[i]) == vf

    # test specific example to ensure values of array are as expected
    # compute actual result
    for vfexample in (vfexample1, vfexample2):
        act = nana.plane_angles(vfexample)
        expected = analysis_original.plane_angles(vfexample)
        for j in range(len(act)):
            assert act[j].all() == expected[j].all()


def test_clean_surfaces():
    """input, obs, is a 3d or 4d matrix whose two outermost shape
    dimensions must be equal to those of the other input, matrix M.
    i.e. obs.shape[0:2] == M.shape[0:2]"""
    equal_notequal = []
    pass_assertion_obs = []
    is_3d_or_4d = []
    not_3d_or_4d = []

    # test assertion that obs.shape[0:2] == M.shape[0:2] from...
    # ... clean_surfaces function when it calls convert_matrix_shape_to_clean
    for obsshape in obs_example_shapes:
        for Mshape in M_example_shapes:
            obs = np.random.random(obsshape)
            M = np.random.random(Mshape)
            try:
                assert obs.shape[0:2] == M.shape[0:2]
                equal_notequal.append('equal')
                pass_assertion_obs.append(obs)
            except AssertionError:
                equal_notequal.append('notequal')
    assert equal_notequal == M_shape_obs_shape_assertion

    # test that obs that pass assertion test have either 3d or 4d shapes.
    for pass_obs in pass_assertion_obs:
        try:
            # test devised such that obs' that pass assertion test will have...
            # ...initial shape dimensions (3, 3) and therefore only match...
            # ...with initial shape dims of M_example_shapes[0] (3, 3),...
            # ...not M_example_shapes[1] (4, 4)
            nana.clean_surfaces(pass_obs,
                                np.random.random(M_example_shapes[0]))
            is_3d_or_4d.append(pass_obs.shape)
        except NotImplementedError:
            not_3d_or_4d.append(pass_obs.shape)
    assert is_3d_or_4d == [obs_example_shapes[1], obs_example_shapes[3]]
    assert not_3d_or_4d == [obs_example_shapes[0], obs_example_shapes[-1]]

    # whenever analysis.clean_surfaces() is called, wipe=1. Therefore no...
    # ...to test different values of wipe.

    # test whether output matrix returns expected values
    assert (nana.clean_surfaces(obs_example_input1, M_example_input).all()
            == clean_surfaces_output1.all())
    assert (nana.clean_surfaces(obs_example_input2, M_example_input).all()
            == clean_surfaces_output2.all())


def test_divergence_and_curl():
    """function takes inputs vf (a Nx3 array), SurfaceEffects (a boolean), and
    ovf_run (a dictionary of keyword pairs)"""

    # takes the filename and connects to the product of the files' Nx, Ny, Nz
    node_products = {os.path.join('..', 'Examples', 'cantedvortex.omf'):
                     32768,
                     os.path.join('..', 'Examples', 'ellipsoidwrap.omf'):
                     768,
                     os.path.join('..', 'Examples', 'h2hleftedge.ohf'):
                     25600,
                     os.path.join('..', 'Examples', 'yoyoleftedge.ohf'):
                     6000}
    filenames = (os.path.join('..', 'Examples', 'cantedvortex.omf'),
                 os.path.join('..', 'Examples', 'ellipsoidwrap.omf'),
                 os.path.join('..', 'Examples', 'h2hleftedge.ohf'),
                 os.path.join('..', 'Examples', 'yoyoleftedge.ohf'))

    # test that final shapes of returned objects are correct.
    # 'divflat' shape should be Nx x Ny x Nz whereas...
    # ...rotflat should be Nx x Ny x Nz x 3
    for filename in filenames:
        # 'vf' and 'ovf_run' are returned in functions within omfread.py
        divflat = nana.divergence_and_curl(
            nomf.read_structured_omf_file(filename), False,
            nomf.analyze(filename))[0]
        rotflat = nana.divergence_and_curl(
            nomf.read_structured_omf_file(filename), False,
            nomf.analyze(filename))[1]
        rotmag = nana.magnitude(rotflat)

        assert divflat.shape == (long(node_products[filename]),)
        assert rotflat.shape == (long(node_products[filename]), long(3))
        assert rotmag.shape == (long(node_products[filename]),)
        for i in range(3):
            assert rotflat[:, i].shape == (long(node_products[filename]),)

        # test the return types are numpy arrays.
        objects = [divflat, rotflat, rotflat[:, 0], rotflat[:, 1],
                   rotflat[:, 2], rotmag]
        for obj in objects:
            assert isinstance(obj, np.ndarray)

    # test returned objects contain correct data values for both...
    # ...surfaceeffects=true and surfaceeffects=false for each example file.

    surfaceEffects = [True, False]
    for filename in filenames:
        for boolean in surfaceEffects:
            # actual result
            act = nana.divergence_and_curl(
                nomf.read_structured_omf_file(filename), boolean,
                nomf.analyze(filename))
            # expected result. The original version of the function...
            # ... i.e. not refactored
            exp = analysis_original.divergence_and_curl(
                nomf.read_structured_omf_file(filename), boolean,
                nomf.analyze(filename))
            for j in range(len(act)):
                assert act[j].all() == exp[j].all()

    # test special 2d case; Nz = 1
    dic = {"xnodes:": 3, "ynodes:": 3, "znodes:": 1, "xstepsize:": 0.01,
           "ystepsize:": 0.01, "zstepsize:": 0.01}
    for boolean in surfaceEffects:
        # actual result
        act = nana.divergence_and_curl(vfexample2, boolean, dic)
        # expected result. The original version of the function...
        # ... i.e. not refactored
        exp = analysis_original.divergence_and_curl(vfexample2, boolean, dic)
        for j in range(len(act)):
            assert act[j].all() == exp[j].all()
<<<<<<< HEAD
=======
          
>>>>>>> f88224be0f7551ada7d06eda673835f43be5858e
