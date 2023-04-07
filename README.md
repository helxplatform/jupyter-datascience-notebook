## Introduction

This project creates a [Jupyter datascience-notebook](https://github.com/jupyter/docker-stacks) docker image that is meant to run within our HeLx platofrm.  It uses the datascience-notebook image as it's base image.

## Configuring

Some configuration variables can be set in the "config.env" file.  There are others to set the image tag and registry.  Also some to use when running the container locally.  "run.env" can be used to set variables within the container when running.

## Building

To build the image you can use the basic docker command or use the included Makefile.
```
  make build
```
  To build the image without using the docker cache you can use the 'build-nc' argument.

## Running Locally

```
  make run
```
  Then connect to localhost:8888 in your web browser.

## Publishing Image to Registry
  To push the image to the configured registry (in config.env) use the 'publish' argument.
```
  make publish
```
  To build the image without the docker cache and publish you can use the 'release' argument.

## Container Environment Variables
  USER | NB_USER : Used to change the username of the process running within the container.
  
  NB_PREFIX : Used to set the URL path prefix to access the Jupyter datascience-notebook. 
