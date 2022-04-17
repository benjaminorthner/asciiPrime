# ----------------------------------------------------------------------------------------------------
# This file handles the calling of the c function primify() via the python wrapper function primify()
# ----------------------------------------------------------------------------------------------------

import ctypes, os

# load shared library by giving path to shared library (compiled c program)
_primify = ctypes.CDLL('./primify.so')

# tell ctypes what the data types are that the c function primify() will need for the function
# char **primify(char *asciiImageString, int width, int height, int borderWidth, char *luminosityGroupsString, int numberOfPrimeChecks) 
_primify.primify.argtypes = (ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int)
_primify.primify.restype = ctypes.c_char_p

# python wrapper function of c function primify()
def primify(asciiImage, cols, rows, borderWidth, luminosityGroups, numberOfPrimeChecks):
    # make global to help interpreter find the c function
    global _primify

    # convert variables into ctypes
    cols_c = ctypes.c_int(cols)
    rows_c = ctypes.c_int(rows)
    borderWidth_c = ctypes.c_int(borderWidth)
    numberOfGroups_c = ctypes.c_int(len(luminosityGroups))
    numberOfPrimeChecks_c = ctypes.c_int(numberOfPrimeChecks)

    # I can not get passing an array of strings to work with ctype, so I will convert asciiImage to a single continuous string
    asciiImage_c = ctypes.c_char_p(''.join(asciiImage).encode('utf-8'))

    # also convert lumniosity groups to a single continuous string but add a "-" between each group
    luminosityGroups_c = ctypes.c_char_p('-'.join(luminosityGroups).encode('utf-8'))
    
    # call the c function and save results as primeAsciiImage
    primeAsciiImageString = _primify.primify(asciiImage_c, cols_c, rows_c, borderWidth_c, luminosityGroups_c, numberOfGroups_c, numberOfPrimeChecks_c)
    
    # convert asciiImageString back to 2d array, and standard encoding
    primeAsciiImage = [primeAsciiImageString[i:i+cols].decode('utf-8') for i in range(0, len(primeAsciiImageString), cols)]
    return primeAsciiImage