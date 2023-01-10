FROM jupyter/datascience-notebook:x86_64-notebook-6.5.1

ARG NB_USER="jovyan"
ARG NB_UID="30000"
ARG NB_GID="1136"

# Configure environment
ENV CONDA_DIR=/opt/conda \
    SHELL=/bin/bash \
    NB_USER="${NB_USER}" \
    NB_UID=${NB_UID} \
    NB_GID=${NB_GID} \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8 \
    JULIA_PKGDIR=/opt/julia
ENV PATH="${CONDA_DIR}/bin:${PATH}" \
    HOME="/home/${NB_USER}"

USER root

RUN fix-permissions /etc/jupyter/ "${HOME}" "${CONDA_DIR}" "${JULIA_PKGDIR}"

