ARG BASE_IMAGE_TAG=latest
FROM containers.renci.org/helxplatform/jupyter/docker-stacks/datascience-notebook:$BASE_IMAGE_TAG

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

COPY root /
RUN fix-permissions /home

USER $NB_USER
CMD ["/init.sh"]
