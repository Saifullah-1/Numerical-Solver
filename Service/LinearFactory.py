# from linear_methods.doolittle import *
# from linear_methods.crout import *
# from linear_methods.cholesky import *
import numpy as np

from linear_methods.Doolittle import Doolittle
from linear_methods.Error import Error
from linear_methods.Gauss import Gauss
from linear_methods.HandleEquations import PrepareEquations
from linear_methods.cholesky import Cholesky
from linear_methods.crout import Crout
from linear_methods.gauss_seidel import *
from linear_methods.jacobi_iteration import *
from linear_methods.GaussGordan import *


class LinearFactory:
    def __init__(self, method, equations, precision, initial_guess=0, iterations=0, error=0):
        self.method = method.lower()
        self.augmentedMatrix, self.coeff, self.unknowns, self.results, self.message = PrepareEquations(equations)
        self.precision = int(precision)
        self.initial_guess = initial_guess
        self.iterations = int(iterations)
        self.error = float(error)

    def create(self):
        if self.message != "continue":
            return Error(self.message)

        if self.method == "gauss elimination":
            return Gauss(self.augmentedMatrix, self.coeff, self.unknowns, self.results, self.precision)
        elif self.method == "gauss jordan":
            return GaussJordan(self.augmentedMatrix, self.coeff, self.unknowns, self.results, self.precision)
        elif self.method == "doolittle":
            return Doolittle(np.array(self.coeff),np.array(self.unknowns) ,np.array(self.results.flatten()), self.precision)
        elif self.method == "crout":
            return Crout(np.array(self.coeff),np.array(self.unknowns) ,np.array(self.results.flatten()), self.precision)
        elif self.method == "cholesky":
            return Cholesky(np.array(self.coeff),np.array(self.unknowns) ,np.array(self.results.flatten()), self.precision)
        elif self.method == "gauss seidel":
            return GaussSeidel(self.augmentedMatrix.tolist(), self.initial_guess, self.iterations, self.error, self.precision)
        elif self.method == "jacobi iteration":
            return Jacobi(self.augmentedMatrix.tolist(), self.initial_guess, self.iterations, self.error, self.precision)
        else:
            return None
