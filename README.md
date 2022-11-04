The Dockerfile is used to build a Jupyter image based on jupyter/datascience-notebook that changes the UID/GID for the process running in the container.  The UID is specified but I don't think it is actually used.  The changes are made in order to work with a particular use case we have, but should also work in other environments.

