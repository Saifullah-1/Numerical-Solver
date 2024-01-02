from math import floor, log10
import sympy as sp

class SecantMethod:
    def __init__(self, equation, iterations, tolerance, figures):
        self.simplified_equation = self.equations_parser(equation)
        self.iterations = iterations
        self.tolerance = tolerance
        self.figures = figures

    @staticmethod
    def equations_parser(equation):
        x = sp.symbols('x')
        simplified_equation = sp.simplify(equation)
        return simplified_equation

    @staticmethod
    def sig_figs(x: float, precision: int):
        if x == 0:
            return 0
        x = float(x)
        precision = int(precision)
        return round(x, -int(floor(log10(abs(x)))) + (precision - 1))

    @staticmethod
    def check_denominator(value):
        if value == 0:
            return True

    def test_tolerance(self, prev, solution):
        if self.check_denominator(solution):
            return True
        return (abs((solution - prev))/abs(solution))*100 <= self.tolerance

    def result(self, value):
        x = sp.symbols('x')
        values = {x: value}
        return self.sig_figs(self.simplified_equation.subs(values).evalf(), self.figures)

    def solve(self, x_prev, x_current):
        numerator = self.sig_figs(x_current, self.figures) - (
            self.sig_figs(self.result(x_current), self.figures) *
            self.sig_figs((x_prev - x_current), self.figures)
        ) / (
            self.sig_figs(self.result(x_prev), self.figures) -
            self.sig_figs(self.result(x_current), self.figures)
        )
        return self.sig_figs(numerator, self.figures)

    def plot(self):
        sp.plot(self.simplified_equation, show=True)

    def execute(self, x_prev1, x_prev2):
        solution = 1e10
        prev = 0
        check = 0
        printlist = ""
        for itr in range(self.iterations):
            prev = solution
            if((self.sig_figs(self.result(x_prev1), self.figures) -self.sig_figs(self.result(x_prev2), self.figures))==0):
                break
            solution = self.solve(x_prev1, x_prev2)
            step = "iteration " + str(itr + 1) + ": " + str(solution) + "\n"
            printlist = printlist + step
            if self.test_tolerance(prev, solution):
                check = 1
                printlist = printlist + "Solution has been reached upon the given tolerance \n"
                printlist = printlist+ "The root is : "+ str(solution)
                break
            x_prev1, x_prev2 = x_prev2, solution
        if check == 0:
            printlist = printlist + "Solution is not found upon the given tolerance"
        return printlist
