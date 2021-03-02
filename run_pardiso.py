# Example program to show the error when using of the partial solve option in Pardiso in a real and symmetric positive definte linear systems.
# Our goal is to speed up the computation on the solving phase 33, and in this case, we tried to use the parital solver to reduce computation cost for the last step, phase 33.

import sys
import ctypes
import time
import numpy as np
import scipy.sparse as sp

def get_libmkl():

    if sys.platform == 'darwin':
        return ctypes.CDLL('libmkl_rt.dylib')
    elif sys.platform == 'win32':
        return ctypes.CDLL('mkl_rt.dll')
    else:
        return ctypes.CDLL('libmkl_rt.so')

def call_pardiso(A, b):
    """
    Python interface to the Intel MKL PARDISO library for solving large sparse linear systems of equations Ax=b.

    Parameters
    ------------
    A: scipy.sparse csr or csc
        Sparse square left-hand side matrix with dimension of NxN
    b: right hand side vector with dimension of Nx1
    """

    pardiso = get_libmkl().pardiso

    # A is always a real and symmetric positive definite matrix
    mtype = 2

    # Number of right hand sides. b is always a vector.
    nrhs = 1

    # determine 32bit or 64bit architecture
    if ctypes.sizeof(ctypes.c_void_p) == 8:
        pt_type = (ctypes.c_int64, np.int64)
    else:
        pt_type = (ctypes.c_int32, np.int32)

    pt = np.zeros(64, dtype=pt_type[1])
    iparm = np.zeros(64, dtype=np.int32)
    iparm[0] = 1
    iparm[1] = 2
    iparm[30] = 1;

    # # added by Fang 20210210. Change it back in the future
    perm = np.zeros((A.shape[1],), dtype=np.int32)
    perm[0:306976] = 1

    # Maximum number of numerical factorizations.
    maxfct = 1;

    # Which factorization to use.
    mnum = 1;

    # Supress printing statistical information
    msglvl = False

    error = ctypes.c_int32(0)

    ia = A.indptr + 1
    ja = A.indices + 1

    ddum = np.zeros((1,), dtype=np.float)

    # Reordering and Symbolic Factorization.
    phase = 11

    print('Phase {} starts ...'.format(phase))
    pardiso(
        pt.ctypes.data_as(ctypes.POINTER(pt_type[0])), # pt
        ctypes.byref(ctypes.c_int32(maxfct)), # maxfct
        ctypes.byref(ctypes.c_int32(mnum)), # mnum
        ctypes.byref(ctypes.c_int32(mtype)), # mtype -> 11 for real-nonsymetric
        ctypes.byref(ctypes.c_int32(phase)), # phase
        ctypes.byref(ctypes.c_int32(A.shape[0])), #N -> number of equations/size of matrix
        A.data.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), # A -> non-zero entries in matrix
        ia.ctypes.data_as(ctypes.POINTER(ctypes.c_int32)), # ia -> csr-indptr
        ja.ctypes.data_as(ctypes.POINTER(ctypes.c_int32)), # ja -> csr-indices
        perm.ctypes.data_as(ctypes.POINTER(ctypes.c_int32)), # perm -> empty
        ctypes.byref(ctypes.c_int32(nrhs)), # nrhs
        iparm.ctypes.data_as(ctypes.POINTER(ctypes.c_int32)), # iparm-array
        ctypes.byref(ctypes.c_int32(msglvl)), # msg-level -> 1: statistical info is printed
        ddum.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), # b -> right-hand side vector/matrix
        ddum.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), # x -> output
        ctypes.byref(error) # pardiso error
    )

    print('Phase {} ends ...'.format(phase))

    if error.value != 0:
        print('The Pardiso solver failed with error code {} on solving phase {}.'.format(error.value, phase))

    phase = 22

    print('Phase {} starts ...'.format(phase))

    pardiso(
        pt.ctypes.data_as(ctypes.POINTER(pt_type[0])), # pt
        ctypes.byref(ctypes.c_int32(maxfct)), # maxfct
        ctypes.byref(ctypes.c_int32(mnum)), # mnum
        ctypes.byref(ctypes.c_int32(mtype)), # mtype -> 11 for real-nonsymetric
        ctypes.byref(ctypes.c_int32(phase)), # phase
        ctypes.byref(ctypes.c_int32(A.shape[0])), #N -> number of equations/size of matrix
        A.data.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), # A -> non-zero entries in matrix
        ia.ctypes.data_as(ctypes.POINTER(ctypes.c_int32)), # ia -> csr-indptr
        ja.ctypes.data_as(ctypes.POINTER(ctypes.c_int32)), # ja -> csr-indices
        perm.ctypes.data_as(ctypes.POINTER(ctypes.c_int32)), # perm -> empty
        ctypes.byref(ctypes.c_int32(nrhs)), # nrhs
        iparm.ctypes.data_as(ctypes.POINTER(ctypes.c_int32)), # iparm-array
        ctypes.byref(ctypes.c_int32(msglvl)), # msg-level -> 1: statistical info is printed
        ddum.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), # b -> right-hand side vector/matrix
        ddum.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), # x -> output
        ctypes.byref(error) # pardiso error
    )

    print('Phase {} ends ...'.format(phase))
    if error.value != 0:
        print ('The Pardiso solver failed with error code {} on solving phase {}.'.format(error.value, phase))

    phase = 33

    x = np.zeros_like(b)

    print('Phase {} starts ...'.format(phase))

    start = time.time()

    pardiso(
        pt.ctypes.data_as(ctypes.POINTER(pt_type[0])), # pt
        ctypes.byref(ctypes.c_int32(maxfct)), # maxfct
        ctypes.byref(ctypes.c_int32(mnum)), # mnum
        ctypes.byref(ctypes.c_int32(mtype)), # mtype -> 11 for real-nonsymetric
        ctypes.byref(ctypes.c_int32(phase)), # phase
        ctypes.byref(ctypes.c_int32(A.shape[0])), #N -> number of equations/size of matrix
        A.data.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), # A -> non-zero entries in matrix
        ia.ctypes.data_as(ctypes.POINTER(ctypes.c_int32)), # ia -> csr-indptr
        ja.ctypes.data_as(ctypes.POINTER(ctypes.c_int32)), # ja -> csr-indices
        perm.ctypes.data_as(ctypes.POINTER(ctypes.c_int32)), # perm -> empty
        ctypes.byref(ctypes.c_int32(nrhs)), # nrhs
        iparm.ctypes.data_as(ctypes.POINTER(ctypes.c_int32)), # iparm-array
        ctypes.byref(ctypes.c_int32(msglvl)), # msg-level -> 1: statistical info is printed
        b.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), # b -> right-hand side vector/matrix
        x.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), # x -> output
        ctypes.byref(error) # pardiso error
    )


    print(f'{time.time()-start:.2f} seconds to solve system')

    print('Phase {} ends ...'.format(phase))

    if error.value != 0:
        print ('The Pardiso solver failed with error code {} on solving phase {}.'.format(error.value, phase))

    phase = -1

    pardiso(
        pt.ctypes.data_as(ctypes.POINTER(pt_type[0])), # pt
        ctypes.byref(ctypes.c_int32(maxfct)), # maxfct
        ctypes.byref(ctypes.c_int32(mnum)), # mnum
        ctypes.byref(ctypes.c_int32(mtype)), # mtype -> 11 for real-nonsymetric
        ctypes.byref(ctypes.c_int32(phase)), # phase
        ctypes.byref(ctypes.c_int32(A.shape[0])), #N -> number of equations/size of matrix
        ddum.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), # A -> non-zero entries in matrix
        ia.ctypes.data_as(ctypes.POINTER(ctypes.c_int32)), # ia -> csr-indptr
        ja.ctypes.data_as(ctypes.POINTER(ctypes.c_int32)), # ja -> csr-indices
        perm.ctypes.data_as(ctypes.POINTER(ctypes.c_int32)), # perm -> empty
        ctypes.byref(ctypes.c_int32(nrhs)), # nrhs
        iparm.ctypes.data_as(ctypes.POINTER(ctypes.c_int32)), # iparm-array
        ctypes.byref(ctypes.c_int32(msglvl)), # msg-level -> 1: statistical info is printed
        ddum.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), # b -> right-hand side vector/matrix
        ddum.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), # x -> output
        ctypes.byref(error) # pardiso error
    )

    if error.value != 0:
        print ('The Pardiso solver failed with error code {} on solving phase {}.'.format(error.value, phase))

    return np.ascontiguousarray(x) # change memory-layout back from fortran to c order


if __name__ == "__main__":

    file_A = './stiffmat_ernie.npz'
    file_b = './rhs_ernie.npz'

    print ('Load matrix A ...')
    A = sp.load_npz(file_A)
    print('Matrix A loaded.')

    print ('Load rhs b ...')
    b = np.load(file_b)
    print ('Rhs b loaded.')

    print ('Call Intel MKL Pardiso ...')
    x = call_pardiso(A, b)
