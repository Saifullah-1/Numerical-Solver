import numpy as np
from math import floor, log10


class Crout:

    def __init__(self, A, b, x, sf):
        self.x = x
        self.A = A
        self.b = b
        self.sf = sf
        self.result = ""

    def sig_figs(self,x: float):
        if x == 0:
            return x
        x = float(x)
        precision = int(self.sf)
        return round(x, -int(floor(log10(abs(x)))) + (precision - 1))
    
    def execute(self):
        n = len(self.A)
        x = np.zeros(n)
        L , U = self.DecompCrout(self.A,n)
        self.result = "=>STEP 1 : DECOMPOSITION\n"
        self.result += "L =\n" + str(L) +"\n\n" + "U =\n" +str(U) +"\n\n"
        self.substitution(L , U , n ,self.b ,x)
        return self.result

    def DecompCrout(self,A,n):
        
        L = np.zeros((n, n))
        U = np.zeros((n, n))
    
        for i in range(n):
            L[i, 0] = A[i, 0]
            U[i,i] = 1

        for j in range(1, n):
            U[0, j] = self.sig_figs(A[0, j] / L[0, 0])

        for j in range(1, n-1):
            for i in range(j, n):
                sum1 = sum(self.sig_figs(L[i, k] * U[k, j]) for k in range(j))
                L[i, j] = self.sig_figs(A[i, j] - sum1)

            for kk in range(j+1, n):
                sum2 = sum(self.sig_figs(L[j, ii] * U[ii, kk]) for ii in range(j))
                U[j, kk] = self.sig_figs((A[j, kk] - sum2) / L[j, j])  

        sum3 = sum(self.sig_figs(L[n-1, x] * U[x, n-1]) for x in range(n-1))
        L[n-1, n-1] = self.sig_figs( A[n-1, n-1] - sum3)

        return L, U

    def substitution(self, L, U, n, b, x):
        self.result += "\n=>STEP 2 : FORWARD SUBSTITUTION\n"
        self.result += "\nLy = b \n\n"
        y = np.zeros(n)
        y[0] = self.sig_figs(b[0] / L[0,0])
        self.result += f"y{1} = {b[0]} / {L[0,0]}= {y[0]}\n"

        for i in range(1, n):
            sum = 0
            for j in range(i):
                sum += self.sig_figs(L[i, j] * y[j])
            y[i] = self.sig_figs((b[i] - sum) / L[i, i])
            self.result += f"y{1+i} = ( {b[i]} - {sum} ) / {L[i,i]} = {y[i]}\n"

        self.result += "\ny =\n" + str(y) + "\n"

        self.result += "\n=>STEP 3 : BACKWARD SUBSTITUTION\n"
        self.result += "\nUx = y\n"

        x[n-1] = y[n-1]
        self.result += f"\nx{n} = {y[n-1]} \n"

        for i in range(n-2, -1, -1):
            sum = 0
            for j in range(i+1, n):
                sum +=self.sig_figs(U[i, j] * x[j])
            x[i] = self.sig_figs((y[i] - sum) / U[i, i])
            self.result += f"x{1+i} = ( {y[i]} - {sum} ) / {U[i,i]} = {x[i]}\n"


