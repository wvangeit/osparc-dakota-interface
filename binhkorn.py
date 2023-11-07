"""
Simple multidimensional function.
"""

# ==============================================================================


def binhkorn(x):
    """
    See https://en.wikipedia.org/wiki/Test_functions_for_optimization

    """
    x1 = x[0]
    x2 = x[1]

    if not 0.0 <= x1 <= 5.0:
        raise ValueError(f"X1 out of bounds: {x1}")
    if not 0.0 <= x2 <= 3.0:
        raise ValueError(f"X2 out of bounds: {x2}")

    y1 = 4 * x1**2 + 4 * x1**2
    y2 = (x1 - 5)**2 + (x2 - 5)**2

    return y1, y2

# ==============================================================================
# main


def main():
    x = 1
    y = 2
    print(f"x={x}; y={y}; binhkorn(x,y)={binhkorn(x,y)}")


if __name__ == '__main__':
    main()
