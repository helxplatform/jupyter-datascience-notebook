#!/bin/bash

start.sh jupyter lab --LabApp.token= --ip="*" --NotebookApp.base_url=${NB_PREFIX} --NotebookApp.allow_origin="*"
