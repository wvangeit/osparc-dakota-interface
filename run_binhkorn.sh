#!/bin/bash

module load litis/dakota

pyenv local 3.8.10

python user_binhkorn.py -i opt_binhkorn.in

