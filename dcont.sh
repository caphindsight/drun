#! /usr/bin/env bash

# Run a CLI tool inside docker container

useradd -ms /bin/bash $DRUN_USER
cd /workspace
sudo -u $DRUN_USER $DRUN_TOOL $@

