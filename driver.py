#!/usr/bin/env python3

""" 
Driver that wraps and executes an arbitrary function from dakota input
(parameter) file format and returns the result as a dakota (results) output
file.

The fom of the call must be: 
    driver module.func inputfile [outputfile]

where:

    driver is a bash executable generated by the drivergen.py script,

    module.func is the python path to the simulation function,

    inputfile is a dakota input parameter file, 

    outputfile is the dakota output results file generated by the simulation function. 
"""

import sys
import ast
import functools
import fio

# ==============================================================================
# proc

def split_on_last(string, delimiter):
    """
    Return the last element from string, after the delimiter.
    If string ends in the delimiter or the delimiter is absent,
    returns the original string without the delimiter.
    """
    prefix, delim, last = string.rpartition(delimiter)
    return prefix, last if (delim and last) else prefix

def get_variables(slines):
    """
    Returns variable values from dakota input format as a list of lists. 
    """
    ln = len(slines) 
    vals = []
    for i in range(0, ln):
        words = slines[i]
        if words[1] == "variables":
            n = int(words[0])
            for j in range(i+1, i+n+1):
                l = slines[j]
                v = float(l[0])
                vals.append(v)
            break
    return vals

def read_dakota_params(infile):
    slines = fio.read_wsv(infile)
    return get_variables(slines)

def write_dakota_results(data, outfile):
    fio.write_wsv(data, outfile)


# ==============================================================================
# run

def runsim(f, infile, outfile=None):
    x = read_dakota_params(infile)
    y = f(x)
    outdata = [[y, 'f']]
    write_dakota_results(outdata, outfile)

def main():
    args = sys.argv
    if len(args) < 3:
        raise RuntimeError('not enough arguments')
    if len(args) < 4:
        args.append(None)

    # read conf json file and extract either python func name or osparc service data
    parfile = sys.argv[1]
    par = fio.to_jsonobj(fio.read_file(parfile))
    pypath = par['service']['pypath']
    mod, fun = split_on_last(pypath, '.')

    # simulation function
    f = getattr(__import__(mod), fun)

    params = {}
    for p in par['parameters']:
        params[p['name']] = ast.literal_eval(p['value'])

    # partial simulation
    g = functools.partial(f, **params)

    # run partial simulation on arg files
    runsim(g, sys.argv[2], sys.argv[3])

if __name__ == '__main__':
    main()
