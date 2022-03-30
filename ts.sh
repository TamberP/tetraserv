#!/bin/bash
export PYTHONPATH=./src:${PYTHONPATH}
python -m tetraserv $@
