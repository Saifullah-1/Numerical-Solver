from matplotlib import pyplot as plt
import numpy as np
import sympy as sp


class Plotter:
    def __init__(self, equation):
        self.equation = equation
        self.symbolic_expr = sp.sympify(equation)
        self.lambda_func = sp.lambdify('x', self.symbolic_expr, 'numpy')

    def func(self, x):
        return self.lambda_func(x)

    def plot_fun(self):
        x_vals = np.linspace(-10, 10, 1000)
        y_vals = self.func(x_vals)

        plt.plot(x_vals, y_vals, label=self.equation)
        plt.axhline(0, color='black', linestyle='--', linewidth=0.8)
        plt.axvline(0, color='black', linestyle='--', linewidth=0.8)

        plt.title('Plot of the Function')
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.legend()

        plt.show()
