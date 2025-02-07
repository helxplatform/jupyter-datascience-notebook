FROM containers.renci.org/helxplatform/jupyter/docker-stacks/minimal-notebook:cuda-202309182143

USER root

# Update available packages in the package index
RUN apt update -y

# Add ppa for git install later
RUN sudo apt-get install software-properties-common -y && \
    sudo add-apt-repository ppa:git-core/ppa

# These packages are necessary for some Poetry packages to correctly install later (like xmlsec) and LDAP
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y pkg-config libxml2-dev libxmlsec1-dev \
    libxmlsec1-openssl curl git libc-bin locales libcurl3-gnutls libnss-ldap

ENV POETRY_CONFIG_DIR=/opt/poetry/.config \
    POETRY_HOME=/opt/poetry \
    POETRY_CACHE_DIR=/opt/poetry/.cache \
    POETRY_VERSION=1.8.3

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

COPY root /

USER $NB_USER

CMD ["/init.sh"]