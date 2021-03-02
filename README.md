This repository includes the python file and two data files needed to reproduce an Intel MKL
Pardiso error that occurs to us, when partially solving a linear
equation with Pardiso:


- run_pardiso.py: python code that invokes Intel MKL Pardiso

- rhs_ernie.npz and stiffmat_ernie.npz: data file used


The steps below trigger the error:

- Pull the docker image:  docker pull continuumio/anaconda3

- Change directory to the one of this repository: cd repo_dir

- Run the docker image while mounting the directory of the repository:
  docker run --mount type=bind,source=${PWD},target=/mnt/local -it continuumio/anaconda3 /bin/bash

- Run the python file from within the Docker image:
  python /mnt/local/run_pardiso.py

