import numpy as np

from ovf2vtk import analysis


def test_cs(obs, M, wipe = 0, eps = 1e-3, zerovalue = 0.0):
    """Testing the clean_surfaces function within analysis.py for the ovf2vtk
    software. By Harry Wilson. Last updated 18/11/15"""
    cs = analysis.clean_surfaces((obs, M, wipe, eps, zerovalue))
    
    assert len(M.shape) == 4 # ensures right shape to assign values to Nx, Ny, Nz, dummy
    assert obs.shape == cs.shape # check output is expected shape
    
    # check zero values (if any) are assigned correctly
    Mcols = int(M.shape[-1]) 
    Mrows = int(M.shape[-2])
    obscols = int(obs.shape[-1])
    Mabs = abs(M)
    flatM = Mabs.ravel()
    for i in range(Mrows):
        rowsum = flatM[i:i + Mcols]
        if rowsum <= eps:
            for j in range(obscols):
                obs.itemset(j, 0.0)
    
    print 'pass'
            
        
    