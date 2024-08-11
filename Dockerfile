# base image with Miniconda pre-installed?
FROM continuumio/miniconda3
MAINTAINER ersilia

WORKDIR /app

RUN pip install pandas
RUN pip instal rdkit
RUN pip install pytorch-lightning
RUN pip install torch-geometric

#  qupKake repository clone
RUN git clone https://github.com/Shualdon/QupKake.git

# change to the QupKake directory
WORKDIR /app/QupKake

# create the conda environment from the environment.yml file
RUN conda env create -f environment.yml

# activate the environment and install QupKake
RUN /bin/bash -c "source activate qupkake && pip install ."

# set conda environment path as the default PATH for all subsequent commands
ENV PATH /opt/conda/envs/qupkake/bin:$PATH

WORKDIR /repo
COPY . /repo
