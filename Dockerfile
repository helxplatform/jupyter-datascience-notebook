ARG BASE_IMAGE=containers.renci.org/helxplatform/jupyter/docker-stacks/scipy-notebook
ARG BASE_IMAGE_TAG=cuda-2023051923
FROM $BASE_IMAGE:$BASE_IMAGE_TAG

USER root
COPY root /
RUN fix-permissions /home

USER $NB_USER
CMD ["/init.sh"]
