import numpy as np
from linear_methods import gauss


def solve_doolittle(precision, matrix):
    u = gauss.solve_gauss(precision, matrix)
    return u

def solve_crout(precision, matrix):
    return matrix


def solve_cholesky(precision, matrix):
    return matrix