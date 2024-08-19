FROM bentoml/model-server:0.11.0-py39
MAINTAINER ersilia

WORKDIR /app

RUN pip install pandas
RUN pip install rdkit
RUN pip install pytorch-lightning
RUN pip install torch-geometric

RUN pip install git+https://github.com/Shualdon/QupKake.git

WORKDIR /repo
COPY . /repo