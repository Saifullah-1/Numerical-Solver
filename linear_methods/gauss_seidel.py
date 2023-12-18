from Service.operations import Operations
import numpy as np


class GaussSeidel:
    def __init__(self, augmentedMatrix, vect, iterations, tolerance, precision):
        self.augmentedMatrix = augmentedMatrix
        self.vect = vect
        self.iterations = iterations
        self.tolerance = tolerance
        self.precision = precision

    def execute(self):
        for k in range(len(self.augmentedMatrix)):
            for y in range(len(self.augmentedMatrix)):
                if k == y and self.augmentedMatrix[k][y] == 0:
                    return "NO SOLUTION"

        for i in range(len(self.augmentedMatrix)):
            for j in range(len(self.augmentedMatrix[0])):
                if self.augmentedMatrix[i][j] != 0:
                    self.augmentedMatrix[i][j] = Operations.sig_figs(self.augmentedMatrix[i][j], self.precision)

        printlist = ""
        itr = -1
        old = np.zeros(len(self.vect))
        while True and self.iterations > 0:
            itr += 1
            self.iterations -= 1
            for i in range(len(self.augmentedMatrix)):
                total = 0
                for j in range(len(self.augmentedMatrix)):
                    total += self.augmentedMatrix[i][j] * self.vect[j]
                x = self.augmentedMatrix[i][i]
                old[i] = self.vect[i]
                self.vect[i] = (self.augmentedMatrix[i][-1] - total + self.augmentedMatrix[i][i] * self.vect[i]) / x
                if self.vect[i] != 0:
                    self.vect[i] = Operations.sig_figs(self.vect[i], self.precision)

            var1 = f"Iteration {itr + 1}: {self.vect}"
            printlist = printlist + var1
            printlist = printlist + "\n"
            if Operations.check_continue(self.vect, old, self.tolerance):
                break
        return printlist
