!/bin/csh

# C-shell script

limit stacksize unlimited

_VCRTLIBRARIESINFO_

setenv OMP_NUM_THREADS 1
setenv MKL_NUM_THREADS 1
setenv I_MPI_PIN_DOMAIN omp
setenv KMP_STACKSIZE 16m

# Set VM2 executable to use
set VC_FORTRAN_EXE=_VCEXELOCATION_/VC_CompChemPackage_mpi.exe

# Set VM2 input and output file names
set VC_IN_FILE=_VCFILEINP_
set VC_OUT_FILE=_VCFILEOUT_

# Will run 8 MPI processes
nohup mpirun -n 8 $VC_FORTRAN_EXE $VC_IN_FILE $VC_OUT_FILE
