from math import floor, log10
import sympy as sp


class Newton_modified_2:
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
    def sf(x: float, precision: int):
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

    def function_result(self, value):
        x = sp.symbols('x')
        values = {x: value}
        return self.sf(self.simplified_equation.subs(values).evalf(), self.figures)

    def derivative_result(self,value):
        x =sp.symbols('x')
        values={x: value}
        derivative=sp.diff(self.simplified_equation,x)
        return self.sf(derivative.subs(values).evalf(),self.figures)
    
    def second_derivative(self,value):
        x = sp.symbols('x')
        values ={x:value}
        first = sp.diff(self.simplified_equation,x)
        second = sp.diff(first,x)
        return  self.sf(second.subs(values).evalf(),self.figures)
    
    def solve(self,guess):
        newguess=self.sf(guess,self.figures)
        numerator = self.sf(self.function_result(newguess)*self.derivative_result(newguess),self.figures)
        second_derivative = self.sf(self.second_derivative(newguess),self.figures)
        denominator = self.sf(self.sf(self.derivative_result(newguess)**2,self.figures) - self.sf(self.function_result(newguess)*second_derivative,self.figures),self.figures)
        return  self.sf(newguess-self.sf(numerator/denominator,self.figures),self.figures)

    def execute(self,guess):
        solution = guess
        prev = 0
        check = 0
        printlist ="_____________________________________________________________\n"
        printlist += "i\tXi\t\tRelative Error(%)\n"
        printlist +="_____________________________________________________________\n"
        printlist += str(0) + "\t" + str(solution) + "\t\t" + "" + "\n"
        for itr in range(self.iterations):
            prev = solution
            newguess = self.sf(guess, self.figures)
            second_derivative = self.sf(self.second_derivative(newguess),self.figures)
            denominator = self.sf(self.sf(self.derivative_result(newguess)**2,self.figures) - self.sf(self.function_result(newguess)*second_derivative,self.figures),self.figures)
            if(denominator==0):
                break
            solution = self.solve(guess)
            error =self.sf(abs(self.sf(self.sf(solution-prev,self.figures)/solution,self.figures))*100,self.figures)
            step = str(itr+1) + "\t" + str(solution) + "\t\t" + str(error) + "\n"
            printlist = printlist + step
            print( self.sf(self.function_result(solution),self.figures) )
            if self.test_tolerance(prev, solution) or self.sf(self.function_result(solution),self.figures) == 0:
                check = 1
                printlist +="_____________________________________________________________\n"
                printlist = printlist + "Solution has been reached upon the given tolerance \n"
                printlist = printlist + "The root is : " + str(solution)
                break
            guess = solution
        if check == 0:
            printlist +="_____________________________________________________________\n"
            printlist = printlist + "Solution is not found upon the given tolerance"
        return printlist