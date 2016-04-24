import os

from ovf2vtk import omfread_new as nomf


def test_dicts():
    a = nomf.analyze(os.path.join('..', 'Examples', 'cantedvortex.omf'))
    assert a == {}
