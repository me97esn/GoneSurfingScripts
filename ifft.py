import numpy as np
import math
import datetime


def ifft2(x, y, fourierCoefficients, lenX, lenY, numberOfFrequenciesToInclude=30, numberOfRowsToIncludeBottom=2, numberOfRowsToIncludeTop=10):
    """Note: lenX and lenY should be the total number of samples BEFORE subtracting the ignored frequencies"""
    result = 0.0j
    number_to_skip = lenY - numberOfFrequenciesToInclude * 2
    numberOfRowsToSkip = lenX - numberOfRowsToIncludeBottom * 2

    for m in range(len(fourierCoefficients)):
        _m = None
        if m < numberOfRowsToIncludeBottom:# or m >= len(fourierCoefficients)-numberOfRowsToIncludeTop:
            # print("including row: ", m)
            _m = m
        elif m >= len(fourierCoefficients)-numberOfRowsToIncludeTop:
            _m = m + numberOfRowsToSkip
            # print("second including row: ", m)
        else:
            continue
            # _m = m
            # else:
            #     _m = m + numberOfRowsToSkip
            #
        for n in range(len(fourierCoefficients[0])):
            fourierCoefficient = fourierCoefficients[m][n]
            # Low frequencies are at the beginning of the list
            if  n < numberOfFrequenciesToInclude:
                result = result + fourierCoefficient*np.exp(2*np.pi*1j*(_m*x/lenX + n*y/lenY))/(lenX*lenY)
            else:
                # Middle frequencies are not included in the list
                _n = n + number_to_skip
    
                # High frequencies are at the end of the list
                result = result + fourierCoefficient*np.exp(2*np.pi*1j*(_m*x/lenX + _n*y/lenY))/(lenX*lenY)
    return result.real


def ifft2_with_interpolation(x, y, fourierCoefficients, lenX, lenY, step_size=1):
    x0y0 = math.floor(x/step_size)*step_size, math.floor(y/step_size)*step_size, ifft2_include_all(math.floor(x/step_size)*step_size, math.floor(y/step_size)*step_size, fourierCoefficients, lenX, lenY)
    x0y1 = math.floor(x/step_size)*step_size, math.ceil(y/step_size)*step_size, ifft2_include_all(math.floor(x/step_size)*step_size, math.ceil(y/step_size)*step_size, fourierCoefficients, lenX, lenY)
    x1y0 = math.ceil(x/step_size)*step_size, math.floor(y/step_size)*step_size, ifft2_include_all(math.ceil(x/step_size)*step_size, math.floor(y/step_size)*step_size, fourierCoefficients, lenX, lenY)
    x1y1 = math.ceil(x/step_size)*step_size, math.ceil(y/step_size)*step_size, ifft2_include_all(math.ceil(x/step_size)*step_size, math.ceil(y/step_size)*step_size, fourierCoefficients, lenX, lenY)

    points = [x0y0, x0y1, x1y0, x1y1]

    return bilinear_interpolation(x, y, points)

def ifft2_include_all(x, y, fourierCoefficients, lenX, lenY):
    result = 0.0j
    for m in range(len(fourierCoefficients)):
        for n in range(len(fourierCoefficients[0])):
            fourierCoefficient = fourierCoefficients[m][n]
            result = result + fourierCoefficient*np.exp(2*np.pi*1j*(m*x/lenX + n*y/lenY))/(lenX*lenY)

    return result.real

def bilinear_interpolation(x, y, points):
    '''Interpolate (x,y) from values associated with four points.

    The four points are a list of four triplets:  (x, y, value).
    The four points can be in any order.  They should form a rectangle.

        >>> bilinear_interpolation(12, 5.5,
        ...                        [(10, 4, 100),
        ...                         (20, 4, 200),
        ...                         (10, 6, 150),
        ...                         (20, 6, 300)])
        165.0

    '''
    # See formula at:  http://en.wikipedia.org/wiki/Bilinear_interpolation

    points = sorted(points)               # order points by x, then by y
    (x1, y1, q11), (_x1, y2, q12), (x2, _y1, q21), (_x2, _y2, q22) = points

    if x1 != _x1 or x2 != _x2 or y1 != _y1 or y2 != _y2:
        raise ValueError('points do not form a rectangle')
    if not x1 <= x <= x2 or not y1 <= y <= y2:
        raise ValueError('(x, y) not within the rectangle')

    # To avoid division by zero
    if (x == x1 and y == y1):
        return q11
    elif (x == x1 and y == y2):
        return q12
    elif (x == x2 and y == y1):
        return q21
    elif (x == x2 and y == y2):
        return q22
    elif( ((x2 - x1) * (y2 - y1) + 0.0) == 0):
        # Safeguard, should not happen
        return q11

    return (q11 * (x2 - x) * (y2 - y) +
            q21 * (x - x1) * (y2 - y) +
            q12 * (x2 - x) * (y - y1) +
            q22 * (x - x1) * (y - y1)
           ) / ((x2 - x1) * (y2 - y1) + 0.0)

def ifft(t, fourierCoefficients):
    ""
    n = len(fourierCoefficients)
    result = 0.0j
    for m in range(n):
        result = result + fourierCoefficients[m]*np.exp(2*np.pi*1j*m*t/n)/n
    return result.real

# NOTE: This function does not work as expected
def ifft3(a, b, c, fourierCoefficients, lenA, lenB, lenC):
    # print("a: ", a, "b: ", b, "c: ", c)
    result = 0.0j
    print(".", end="")
    # return fourierCoefficients[a][b][c]
    for l in range(lenA):
        for m in range(lenB):
            for n in range(lenC):
                fourierCoefficient = fourierCoefficients[l][m][n]
                result = result + fourierCoefficient*np.exp(2*np.pi*1j*(l*a/lenA + m*b/lenB + n*c/lenC))/(lenA*lenB*lenC)
    return result.real


