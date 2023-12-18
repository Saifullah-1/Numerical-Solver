import numpy as np
from math import floor, log10


class Doolittle:
    def __init__(self, A, un, b, sf):
        self.b = b
        self.A = A
        self.un = un
        self.sf = sf
        self.result = ""

    def sig_figs(self,x: float):
        print(1)
        if x == 0:
            return x
        x = float(x)
        precision = int(self.sf)
        return round(x, -int(floor(log10(abs(x)))) + (precision - 1))
    
    def execute(self):
        n = len(self.A)
        s = np.zeros(n)  # scaling factors
        o = np.zeros(n, dtype=int)  # indices for pivot rows
        x = np.zeros(n)
        L, U = self.decomposeDol(self.A, n, o, s)
        
        self.result = "=>STEP 1 : DECOMPOSITION\n"
        self.result += "L =\n" + str(L) +"\n\n" + "U =\n" +str(U) +"\n\n"
        self.substitutionDol(L, U, o , n , self.b ,x)
        return self.result
    
    def decomposeDol(self, A, n, o, s):
        L = np.zeros((n, n))
        for i in range(n):
            L[i, i] = 1

        for i in range(n):
            o[i] = i
            s[i] = abs(A[i, 0])
            for j in range(1, n):
                if abs(A[i, j]) > s[i]:
                    s[i] = abs(A[i, j])
        for k in range(n - 1):
            #pivot(A, o, s, n, k)
            for i in range(k + 1, n):
                factor = self.sig_figs(A[o[i], k] / A[o[k], k])
                L[o[i], k] = factor
                for j in range(k , n):
                    A[o[i], j] = self.sig_figs(A[o[i], j] - self.sig_figs(factor * A[o[k], j]))
        return L, A


    def substitutionDol(self, L, U, o, n, b, x):
        print(6)
        self.result += "\n=>STEP 2 : FORWARD SUBSTITUTION\n"
        self.result += "\nLy = b \n\n"
        y = np.zeros(n)
        y[0] = b[0]
        self.result += f"y{1} = {b[1]} = {y[1]}\n"
        for i in range(1, n):
            sum = 0
            for j in range(i):
                sum = self.sig_figs(sum + self.sig_figs(L[i, j] * y[j]))
            y[i] = self.sig_figs(b[i] - sum)
            self.result += f"y{1+i} = {b[i]} - {sum} = {y[i]}\n" 

        self.result += "\ny =\n"+str(y) +"\n"

        self.result += "\n=>STEP 3 : BACKWARD SUBSTITUTION\n"
        self.result += "\nUx = y\n"

        x[n-1] = self.sig_figs(y[n-1] / U[n-1, n-1])
        self.result += f"\n{str(self.un[n-1])} = {y[n-1]} / {U[n-1 , n-1]} ={x[n-1]}\n"

        for i in range(n-2, -1, -1):
            sum = 0
            for j in range(i+1, n):
                sum = self.sig_figs(sum + self.sig_figs(U[i, j] * x[j]))
            x[i] = self.sig_figs((y[i] - sum) / U[i, i])
            self.result += f"{str(self.un[i])} = {y[i]} - {sum} / {U[i,i]} = {x[i]}\n"
