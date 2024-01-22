"""!@file fraction_tools.py
@brief Module containing tools for fractions.

@details This module contains .

@author J. Fergusson
@date 08/11/2023
"""


def add(a,b):
    """!@brief Add two fractions.
    
    @details This function adds two fractions which are input as tuples. The code returns the sum of the two fractions as a tuple.

    @param a The first fraction.
    @param b The second fraction.
    @return c The sum of the two fractions.
    """

    c = (a[0]*b[1] + b[0]*a[1],a[1]*b[1])
    return c