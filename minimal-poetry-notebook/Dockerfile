FROM containers.renci.org/helxplatform/jupyter/docker-stacks/minimal-notebook:cuda-202309182143

USER root

# These packages are necessary for some Poetry packages to correctly install later (like xmlsec)
RUN apt-get update && \
    apt-get install -y pkg-config libxml2-dev libxmlsec1-dev libxmlsec1-openssl curl
RUN apt-get upgrade -y libc-bin locales libcurl3-gnutls

ENV POETRY_CONFIG_DIR=/opt/poetry/.config \
    POETRY_HOME=/opt/poetry \
    POETRY_CACHE_DIR=/opt/poetry/.cache \
    POETRY_VERSION=1.8.3

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

COPY root /

USER $NB_USER

CMD ["/init.sh"]