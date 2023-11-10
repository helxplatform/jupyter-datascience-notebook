ARG BASE_IMAGE=containers.renci.org/helxplatform/jupyter/docker-stacks/scipy-notebook
ARG BASE_IMAGE_TAG=cuda-202309182143
FROM $BASE_IMAGE:$BASE_IMAGE_TAG

USER root
COPY root /

# Theses are install in scipy-notebook: pandas scikit-learn scipy seaborn sqlalchemy statsmodels
RUN apt-get update && apt-get -y install pkg-config && \
    mamba install --yes \
        matplotlib \
        psycopg \
        pyodbc \
        numpy \
        tableone \
        xgboost
# Install MLBox, which would not install properly with mamba or pip.
# https://mlbox.readthedocs.io/en/latest/installation.html
# Installing via setup.py also fails.
# WORKDIR /tmp
# RUN apt-get -y install libhdf5-dev && \
#     wget https://github.com/AxeldeRomblay/MLBox/archive/refs/tags/v0.8.1.tar.gz && \
#     tar xf v0.8.1.tar.gz && \
#     cd MLBox-0.8.1 && \
#     python setup.py install
# RUN pip install --no-cache-dir mlbox && \
RUN fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home"
    # pip install --no-cache-dir mlbox && \

USER $NB_USER
CMD ["/init.sh"]
