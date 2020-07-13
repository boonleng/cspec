#!/bin/bash

if [ "${HOSTNAME}" == "bumblebee.arrc.ou.edu" ]; then
	python -m notebook --no-browser --port=8080
else
	python -m notebook
fi
