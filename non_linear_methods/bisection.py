import math

from Service.operations import Operations
import sympy as sp


class Bisection:
    def __init__(self, equation, xu, xl, eps, max_it, significant):
        self.equation = equation
        self.xu = xu
        self.xl = xl
        self.eps = eps
        self.max_it = max_it
        self.sf = significant
        self.operations = Operations
        self.symbolic_expr = sp.sympify(equation)
        self.lambda_func = sp.lambdify('x', self.symbolic_expr, 'numpy')

    def func(self, x):
        return self.lambda_func(x)

    def execute(self):
        xr = 0
        error = 0
        sol = ""

        # check interval
        try:
            if self.func(self.xu) < 0 < self.func(self.xl):
                temp = self.xl
                self.xl = self.xu
                self.xu = temp

            if self.func(self.xu) * self.func(self.xl) > 0:
                sol = "Error! No root in this interval or there exists an even no. of roots in this Interval"
                return sol
            if self.func(self.xu) == 0:
                return f"Root = {self.xu}"
            elif self.func(self.xl) == 0:
                return f"Root = {self.xl}"

            for i in range(self.max_it):
                temp = xr
                xr = self.operations.sig_figs((self.xl + self.xu) / 2, self.sf)
                f_xl = self.operations.sig_figs(self.func(self.xl), self.sf)
                f_xu = self.operations.sig_figs(self.func(self.xu), self.sf)
                f_xr = self.operations.sig_figs(self.func(xr), self.sf)
                sol = sol + f"\ni = {i + 1} >> xl = {self.xl} | xu = {self.xu} | xr = {xr} | f(xl) = {f_xl} | f(xu) = {f_xu} | f(xr) = {f_xr}"

                if temp != 0:
                    if xr == 0:
                        sol = sol + f" | Ea = {error}"
                    else:
                        error = self.operations.sig_figs(math.fabs((xr - temp) / xr), self.sf) * 100
                        sol = sol + f" | Ea = {error}%\n"
                    if error <= self.eps:
                        break
                else:
                    sol = sol + "\n"

                if f_xr == 0:
                    return sol + f"\nRoot = {xr}"

                elif f_xu * f_xr < 0:
                    self.xl = xr
                else:
                    self.xu = xr

            return sol + f"\nRoot = {xr}"

        except ZeroDivisionError:
            return "No Solution, Function is not continuous"
        except ValueError:
            return "No Solution"
