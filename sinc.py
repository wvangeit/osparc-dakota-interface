"""
Simple sinc multidimensional function.
"""
import math
import numpy as np

# ==============================================================================

def sinc(x = 0., a = math.pi):
    """
    For for scalar or 1d array like x, the sinc continuous function on R^n returns: 
        1                   if x == 0,
        sin(a|x|)/(a|x|)    otherwise.
    """
    x = np.atleast_1d(x)
    anx = a * np.linalg.norm(x)
    if anx == 0.:
        return 1.
    return math.sin(anx) / anx 

# ==============================================================================
# main

def main():
    # print(sinc(x=np.linspace(0, 1, 10)))
    print(sinc(x=0))
    print(sinc(x=1))
    print(sinc(x=1, a=0.))
    print(sinc(x=1, a=1.))

if __name__ == '__main__':
    main()
