ARG BASE_IMAGE_TAG=latest
FROM containers.renci.org/helxplatform/jupyter/docker-stacks/datascience-notebook:$BASE_IMAGE_TAG

USER root
COPY root /
RUN fix-permissions /home

USER $NB_USER
CMD ["/init.sh"]
