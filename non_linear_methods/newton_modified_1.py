from math import floor, log10
import sympy as sp


class Newton_modified_1:
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
            return False
        return (abs((solution - prev))/abs(solution))*100 <= self.tolerance

    def function_result(self, value):
        x = sp.symbols('x')
        values = {x: value}
        return self.sig_figs(self.simplified_equation.subs(values).evalf(), self.figures)

    def derivative_result(self,value):
        x =sp.symbols('x')
        values={x: value}
        derivative=sp.diff(self.simplified_equation,x)
        return self.sig_figs(derivative.subs(values).evalf(),self.figures)

    def solve(self,guess,multiplicity):
        newguess=self.sig_figs(guess,self.figures)
        return  self.sig_figs(newguess-multiplicity*self.sig_figs(self.function_result(newguess)/self.derivative_result(newguess),self.figures),self.figures)

    def plot(self):
        sp.plot(self.simplified_equation,show=True)

    def execute(self, guess, multiplicity):
        solution = 1e10
        prev = 0
        check = 0
        printlist = ""
        for itr in range(self.iterations):
            prev = solution
            newguess = self.sig_figs(guess, self.figures)
            if(self.derivative_result(newguess)==0):
                break
            solution = self.solve(guess,multiplicity)
            step = "iteration " + str(itr + 1) + ": " + str(solution) + "\n"
            printlist = printlist + step
            if self.test_tolerance(prev, solution):
                check = 1
                printlist = printlist + "Solution has been reached upon the given tolerance \n"
                printlist = printlist + "The root is : " + str(solution)
                break
            guess = solution
        if check == 0:
            printlist = printlist + "Solution is not found upon the given tolerance"
        return printlist
