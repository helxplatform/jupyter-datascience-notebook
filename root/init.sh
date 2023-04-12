#!/bin/bash

# If USER variable is set then container is being tested locally, else the
# NB_USER variable should be available when running with Tcyho.
if [ -z "${USER+x}" ]; then
  echo "USER is not set, setting it to $NB_USER"
  USER=$NB_USER
else
  echo "setting NB_USER=$USER"
  export NB_USER=$USER
fi

USER=${USER-"jovyan"}
DELETE_DEFAULT_USER_HOME_IF_UNUSED=${DELETE_DEFAULT_USER_HOME_IF_UNUSED-"yes"}
DEFAULT_USER="jovyan"
declare -i DEFAULT_UID=1000
declare -i DEFAULT_GID=100
declare -i CURRENT_UID=`id -u`
declare -i CURRENT_GID=`id -g`

echo "running as UID=$CURRENT_UID GID=$CURRENT_GID"

if [ $CURRENT_UID -ne 0 ]; then
  echo "not running as root"
  if [[ $CURRENT_UID -ne $DEFAULT_UID || "$USER" != "$DEFAULT_USER" ]]; then
    echo "not running as uid=$DEFAULT_UID or USER!=\"$DEFAULT_USER\""
    # Modify user entry in /etc/passwd.
    cp /etc/passwd /tmp/passwd
    sed -i -e "s/^$DEFAULT_USER\:x\:$DEFAULT_UID\:$DEFAULT_GID\:\:\/home\/$DEFAULT_USER/$USER\:x\:$CURRENT_UID\:$CURRENT_GID\:\:\/home\/$USER/" /tmp/passwd
    cp /tmp/passwd /etc/passwd
    rm /tmp/passwd

    if [[ -d /home/$DEFAULT_USER ]]; then
      if [[ "$USER" != "$DEFAULT_USER" && "$DELETE_DEFAULT_USER_HOME_IF_UNUSED" == "yes" ]]; then
        echo "deleting /home/$DEFAULT_USER"
        rm -rf /home/$DEFAULT_USER
      fi
    fi

  else
    echo "running as uid that is $DEFAULT_UID and USER is not \"$DEFAULT_USER\""
  fi
fi

HOME=/home/$USER
mkdir -p $HOME
# Copy default environment setup files if they don't already exist.
if [ ! -f $HOME/.bashrc ]; then
    cp /etc/skel/.bashrc $HOME/.bashrc
fi
if [ ! -f $HOME/.bash_logout ]; then
    cp /etc/skel/.bash_logout $HOME/.bash_logout
fi
if [ ! -f $HOME/.profile ]; then
    cp /etc/skel/.profile $HOME/.profile
fi

# Change CWD to /home/$USER so it is the starting point for shells in jupyter.
cd $HOME

# The default for XDG_CACHE_HOME to use /home/jovyan/.cache and jupyter will
# create the directory if it doesn't exist.
export XDG_CACHE_HOME=$HOME/.cache

# Run "jupyter -h" to see some options (notebook, server, lab, etc.).  To get more
# options run "jupyter server --help-all".
jupyter lab --IdentityProvider.token= --ServerApp.ip='*' \
    --ServerApp.base_url=${NB_PREFIX} --ServerApp.allow_origin="*" \
    --ServerApp.root_dir="/home/$USER" --no-browser \
    --ServerApp.default_url=${NB_PREFIX}/lab
