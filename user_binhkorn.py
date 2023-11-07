"""
Main script to be run by the user.
"""

import argparse
import subprocess
import file_io
import drivergen
import logging

logging.basicConfig(level=logging.DEBUG)
# ==============================================================================

# save parameters configuration


def make_parfile(parfile):
    pars = {
        'service': {
            'pypath': 'binhkorn.binhkorn',
            'shpath': 'binhkorn'
        },
        'variables': [
            {'name': 'x',
             'type': 'list[float]'},
        ],
        'parameters': [],
        'functions': [
            {'name': 'f',
             'type': 'float'},
        ],
    }
    file_io.write_file(parfile, file_io.to_jsonstr(pars))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--infile', required=True,
        help='dakota input configuration file')
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
    pars = file_io.to_jsonobj(file_io.read_file(parfile))

    # genreate executable file
    execfile = pars['service']['shpath']
    drivergen.gen(execfile, parfile)

    # print execfile content
    print(file_io.read_file(execfile))

    # execute dakota and save results to resfile
    command = 'dakota -i ' + confile + ' -o ' + resfile
    subprocess.run(command, shell=True)


if __name__ == '__main__':
    main()

# ==============================================================================
