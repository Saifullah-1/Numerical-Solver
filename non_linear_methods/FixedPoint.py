from sympy import diff, Symbol
from Service.operations import Operations


class FixedPoint:

    def __init__(self, g, initial, EPS, maxIterations, precision):
        self.g = g
        self.initial = initial
        self.EPS = EPS
        self.maxIterations = maxIterations
        self.precision = precision

        # print(g)
        # print(initial)
        # print(type(initial))
        # print(EPS)
        # print(type(EPS))
        # print(maxIterations)
        # print(type(maxIterations))
        # print(precision)
        # print(type(precision))

    def execute(self):
        def CheckConvergance(result):
            result+=("-"*25)
            result+= (f"\nFirst, Check the Convergence : \n\nFirst Derivative of g(x) = {diff(self.g)}\n")
            derivative = diff(self.g).subs(x,self.initial) 
            if derivative!=0 : derivative = Operations.sig_figs(derivative,self.precision)
            result+= (f"g'({self.initial}) = {derivative}")
            if derivative > -1 and derivative < 1: result+= (f"\nThe Convergence is Guaranted.\n")
            else: result+=(f"\nThe Function May not Converge.\n")
            return result
        
        def Iterate(result):
            result+=(f"\nStarting The Iterative Process : \n")
            result+=('-'*25)
            X = self.initial
            i,lastX,relError,lastError,nonDecreasingErrors = 0,0,'---',0,0
            result += (f"\nIteration     Xi     Relative Error(%)\n")
            while i < self.maxIterations:
                i += 1
                if i != 1:
                    absError = abs(X-lastX)
                    lastError = relError
                    if X!=0 : relError = abs((absError/X))*100
                    if relError != 0 and relError!='---' : relError = Operations.sig_figs(relError,self.precision)
                lastX = X
                X = self.g.subs(x,X)
                if X != 0 : 
                    try : 
                        X = Operations.sig_figs(X,self.precision) 
                    except (OverflowError,ValueError) : 
                        if OverflowError : 
                            result+=(f"\n\nThe Error Increases Drastically, The Method Diverges at Xo = {self.initial}.\n")
                            return result
                result += (f"\n  {i}           {lastX}          {relError}")
                if i!= 1 : 
                    if relError != '---':
                        if relError <= self.EPS : break
                if relError != '---' and lastError != '---' :
                    if (relError>=lastError) : nonDecreasingErrors += 1
                    else : nonDecreasingErrors = 0
                if nonDecreasingErrors >= 4 :
                    result += (f"\n\nThe Error isn't Decreasing, The Method Diverges at Xo = {self.initial}\n")
                    return result
            if i!=self.maxIterations : result+=(f"\n\nThe Root of the Equation = {lastX}\nObtained in {i} iterations\n")
            else : result += (f"\n\nThe Method Didn't Converge after {self.maxIterations} iteration\n")
            return result
        
        x = Symbol('x')
        result = CheckConvergance("")
        return Iterate(result) 
