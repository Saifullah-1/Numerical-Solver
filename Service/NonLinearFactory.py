import sympy

from non_linear_methods.FixedPoint import FixedPoint
from non_linear_methods.bisection import Bisection
from non_linear_methods.regula_falsi import RegulaFalsi
from non_linear_methods.secant_method import SecantMethod
from non_linear_methods.newton_modified_1 import Newton_modified_1


class NonLinearFactory:
    def __init__(self, method, functions, precision, initial_guess, max_iterations, epsilon):
        self.method = method.lower()
        self.functions = functions
        self.precision = int(precision)
        self.initial_guess = initial_guess
        self.max_it = int(max_iterations)
        self.epsilon = float(epsilon)

    def create(self):
        if self.method == "bisection":
            return Bisection(self.functions, float(self.initial_guess[1]), float(self.initial_guess[0]), self.epsilon, self.max_it, self.precision)
        elif self.method == "false position":
            return RegulaFalsi(self.functions, float(self.initial_guess[1]), float(self.initial_guess[0]), self.epsilon, self.max_it, self.precision)
        elif self.method == "secant method":
            return SecantMethod(self.functions, self.max_it, self.epsilon, self.precision)
        elif self.method == "newton raphson 1":
            return Newton_modified_1(self.functions, self.max_it, self.epsilon, self.precision)
        # elif self.method == "newton raphson 2":
        #     return GaussSeidel(self.augmentedMatrix.tolist(), self.initial_guess, self.iterations, self.error, self.precision)
        elif self.method == "fixed point":
            return FixedPoint(sympy.sympify(self.functions), float(self.initial_guess[0]), self.epsilon, self.max_it, self.precision)
        else:
            return None
