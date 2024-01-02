from matplotlib import pyplot as plt
import numpy as np


class Plotter:
    def __init__(self, equation):
        self.equation = equation

    def func(self, x):
        return eval(self.equation)

    def plot_fun(self):
        x = np.linspace(-10, 10, 1000)
        y = self.func(x)
        plt.plot(x, y, label=self.equation)
        plt.axhline(0, color='black', linestyle='--', linewidth=0.8)
        plt.axvline(0, color='black', linestyle='--', linewidth=0.8)

        plt.title('Plot of the Function')
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.legend()

        plt.show()
