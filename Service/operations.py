from math import floor, log10
from sympy import false, true


class Operations:
    def __init__(self):
        pass

    @staticmethod
    def sig_figs(x: float, precision: int):
        x = float(x)
        precision = int(precision)
        return round(x, -int(floor(log10(abs(x)))) + (precision - 1))

    @staticmethod
    def check_continue(new, vect, tolerance):  # check the stopping condition
        for i in range(len(vect)):
            if new[i] == 0:
                return true
            if abs((new[i] - vect[i]) / new[i]) * 100 >= tolerance:
                return false
        return true


