ARG BASE_IMAGE=containers.renci.org/helxplatform/jupyter/minimal-poetry-notebook
ARG BASE_IMAGE_TAG=v0.0.3
FROM $BASE_IMAGE:$BASE_IMAGE_TAG

USER root

WORKDIR /
COPY root .
COPY scripts ./scripts

# This turns off oneDNN custom operations, so that we don't see slightly different 
# numerical results due to floating-point round-off errors from different computation orders
ENV TF_ENABLE_ONEDNN_OPTS=0 \
    TF_CPP_MIN_LOG_LEVEL='2' \
    HOME_DIR=/home/jovyan

# This is necessary because by default Poetry creates a virtual environment, which we don't want in production
RUN $POETRY_HOME/bin/poetry config virtualenvs.create false
# Copy poetry files to container
COPY pyproject.toml poetry.lock $POETRY_HOME/
# Run `poetry install`
RUN cd $POETRY_HOME && $POETRY_HOME/bin/poetry install --no-interaction --no-ansi --no-root
# Remove Poetry files from container, as they're no longer needed
RUN rm $POETRY_HOME/pyproject.toml $POETRY_HOME/poetry.lock

RUN pip install git+https://github.com/helxplatform/eduhelx-jupyterlab-prof-ext.git@b52e0933514d809d50b5e37a867757b7e99abca1
RUN jupyter server extension enable eduhelx_jupyterlab_prof

RUN pip install --upgrade git+https://github.com/helxplatform/eduhelx-utils.git@437bde76aa4ebf53b0ad6f67fe17a69cb3c2c4b1

RUN fix-permissions "/home" && \
    chmod 664 /etc/group

USER $NB_USER