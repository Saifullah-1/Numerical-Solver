import numpy as np
from scipy import linalg
from math import sqrt, floor, log10


class Cholesky:
    def __init__(self, A, b, sf):
        self.b = b
        self.A = A
        # self.x = x
        self.sf = sf
        self.result = ""

    def sig_figs(self,x: float):
        if x == 0:
            return x
        x = float(x)
        precision = int(self.sf)
        return round(x, -int(floor(log10(abs(x)))) + (precision - 1))
    
    def checkDefPos(self, A):
        eigenvalues = np.linalg.eigvals(A)
        if all(eig > 0 for eig in eigenvalues):
            return True
        return False
    
    def execute(self):
        if not self.checkDefPos(self.A):
            return "cannot apply cholesky (Not Definite Positive)"
        n = len(self.A)
        x = np.zeros(n)
        L , U = self.DecompCholesky(self.A, n)
        self.result = "=>STEP 1 : DECOMPOSITION\n"
        self.result += "L =\n" + str(L) +"\n\n" + "Lt =\n" +str(U) +"\n\n"
        self.substitution(L, U, n, self.b, x)
        return self.result
    
    def DecompCholesky(self,A,n):
        n = len(A)
        L = np.zeros((n, n))
        Lt = np.zeros((n, n))
        for k in range(n):
            sum1 = 0
            for j in range(k):
                sum1 += self.sig_figs(L[k, j] ** 2)
            L[k, k] = self.sig_figs(sqrt(self.sig_figs(A[k, k] - sum1)))

            for i in range(k + 1, n):
                sum2 = 0
                for j in range(k):
                    sum2 += self.sig_figs(L[i, j] * L[k, j])
                L[i, k] = self.sig_figs((A[i, k] - sum2) / L[k, k])

        Lt = np.transpose(L)
        return L , Lt
    
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

        x[n-1] = self.sig_figs(y[n-1] / U[n-1, n-1])
        self.result += f"\nx{n} = {y[n-1]} / {U[n-1 , n-1]} = {x[n-1]}\n"

        for i in range(n-2, -1, -1):
            sum = 0
            for j in range(i+1, n):
                sum += self.sig_figs(U[i, j] * x[j])
            x[i] = self.sig_figs((y[i] - sum) / U[i, i])
            self.result += f"x{1+i} = {y[i+1]} - {sum} / {U[i+1,i+1]} = {x[i+1]}\n"


A = np.array([[5,2,-1],[2,8,1],[1,-1,4]], dtype= float)
b = np.array([1,2,3])
# x = np.array(['x','y','z'])
sf = 5
solver = Cholesky(A, b, sf)
result = solver.execute()


print(result)

