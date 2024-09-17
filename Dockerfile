FROM bentoml/model-server:0.11.0-py310
MAINTAINER ersilia


RUN pip install pandas==2.2.2
RUN pip install rdkit==2024.3.5
RUN pip install pytorch-lightning==2.4.0
RUN pip install torch-geometric==2.6.0

WORKDIR /repo
COPY . /repo
