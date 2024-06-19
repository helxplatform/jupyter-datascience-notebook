ARG BASE_IMAGE=containers.renci.org/helxplatform/jupyter/minimal-poetry-notebook
ARG BASE_IMAGE_TAG=v0.0.3
FROM $BASE_IMAGE:$BASE_IMAGE_TAG

USER root

WORKDIR /

# This turns off oneDNN custom operations, so that we don't see slightly different 
# numerical results due to floating-point round-off errors from different computation orders
ENV TF_ENABLE_ONEDNN_OPTS=0 \
    TF_CPP_MIN_LOG_LEVEL='2' \
    HOME_DIR=/home/jovyan

RUN sudo apt upgrade git

RUN pip install git+https://github.com/helxplatform/eduhelx-jupyterlab-student-ext.git@442952445b5aaea018c09ab638026f6e400a7749
RUN jupyter server extension enable eduhelx_jupyterlab_student

RUN pip install --upgrade git+https://github.com/helxplatform/eduhelx-utils.git@437bde76aa4ebf53b0ad6f67fe17a69cb3c2c4b1

RUN fix-permissions "/home" && \
    chmod 664 /etc/group

USER $NB_USER