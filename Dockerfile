ARG BASE_IMAGE=containers.renci.org/helxplatform/jupyter/docker-stacks/datascience-notebook
ARG BASE_IMAGE_TAG=latest
FROM $BASE_IMAGE:$BASE_IMAGE_TAG

USER root
COPY root /
RUN fix-permissions /home

USER $NB_USER
CMD ["/init.sh"]
