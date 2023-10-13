""" 
Main script to be run by the user.
"""

import sys
import argparse
import json
import subprocess
import fio
import driver
import drivergen

# ==============================================================================

# save parameters configuration  
def make_parfile(parfile):
    pars = {
        'service' : {
            'pypath':'sinc.sinc',
            'shpath':'sinc' 
        },
        'variables' : [ 
            { 'name':'x',
              'type':'list[float]'},
        ],
        'parameters' : [ 
            { 'name':'a',
              'type':'float',
              'value':'3.14159265358979323846'},
        ],
        'functions' : [ 
            { 'name':'f',
              'type':'float'},
        ],
    }
    fio.write_file(parfile, fio.to_jsonstr(pars))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', required=True, help='dakota input configuration file')
    parser.add_argument('-o', '--outfile', help='dakota output results file')
    parser.add_argument('-p', '--parfile', help='json parameters file')
    args = parser.parse_args()

    confile = args.infile
    resfile = 'res.out'
    if args.outfile:
        resfile = args.outfile
    parfile = 'par.json'
    if args.parfile:
        parfile = args.parfile

    # save parameters configuration  
    make_parfile(parfile)

    # read parfile
    pars = fio.to_jsonobj(fio.read_file(parfile))

    # genreate executable file
    execfile = pars['service']['shpath'] 
    drivergen.gen(execfile, parfile)

    # print execfile content
    print(fio.read_file(execfile))

    # execute dakota and save results to resfile
    command = 'dakota -i ' + confile + ' -o ' + resfile
    subprocess.run(command, shell=True)



if __name__ == '__main__':
    main()

# ==============================================================================
