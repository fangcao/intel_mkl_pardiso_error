An error in using Intel MKL Pardiso
=====

This repository includes the python file and two data files needed to reproduce an Intel MKL
Pardiso error that occurs to us, when partially solving a linear
equation with Pardiso:


- run_pardiso.py: python code that invokes Intel MKL Pardiso

- rhs_ernie.npz and stiffmat_ernie.npz: data file used


The steps below trigger the error:

1. Install docker: https://docs.docker.com/get-docker/

2. Pull the docker image:  docker pull continuumio/anaconda3

3. Change directory to the one of this repository: cd <your_repo_dir>

4. Run the docker image while mounting the directory of the repository:
  docker run --mount type=bind,source=${PWD},target=/mnt/local -it continuumio/anaconda3 /bin/bash

5. Run the python file within the Docker image:
  python /mnt/local/run_pardiso.py

