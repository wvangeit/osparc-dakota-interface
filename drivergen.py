"""
Generate a driver executable using the driver.py script.

The fom of the call must be: 
    python drivergen drivername parfile
where: drivername is the name of the generated executable

Example:
    python drivergen sinc pars.json
"""
import sys
import os

def gen(execfile, parfile):
    command = ['python3', 'driver.py', parfile, '$@']
    with open(execfile, 'w') as f:
        f.write(' '.join(command))
    os.chmod(execfile, 0o777)

def main():
    args = sys.argv
    if len(args) < 3:
        raise RuntimeError('not enough arguments')
    gen(args[1], args[2])

if __name__ == '__main__':
    main()
