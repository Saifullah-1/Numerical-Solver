from linear_methods.gauss_elimination import *
from linear_methods.gauss_jordan import *
from linear_methods.doolittle import *
from linear_methods.crout import *
from linear_methods.cholesky import *
from linear_methods.jacobi_iteration import *
from operations import Service


class LinearFactory:
    def __init__(self, method, equations, precision, initial_guess=None, stopping_cond=None):
        self.method = method.lower()
        self.equations = Service.handle_equations(equations)
        self.precision = int(precision)
        self.initial_guess = initial_guess
        self.stopping_cond = stopping_cond

    def create(self):
        if self.method == "gauss elimination":
            return GaussElimination(self.precision)
        elif self.method == "gauss jordan":
            return GaussJordan()
        elif self.method == "doolittle":
            return Doolittle()
        elif self.method == "crout":
            return Crout()
        elif self.method == "cholesky":
            return Cholesky()
        elif self.method == "gauss seidel":
            return GaussSeidel()
        elif self.method == "jacobi iteration":
            return Jacobi()
        else:
            return None
