import numpy as np

from Service.operations import Operations


class Jacobi:  # version that takes iterations
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
        while True and self.iterations > 0:
            itr += 1
            self.iterations -= 1
            new = np.zeros(len(self.vect))  # initialize a vector to hold new guess
            vect2 = np.zeros(len(self.vect))  # Store the old vector
            for i in range(len(self.augmentedMatrix)):
                total = 0
                for j in range(len(self.augmentedMatrix)):
                    total += self.augmentedMatrix[i][j] * self.vect[j]
                x = self.augmentedMatrix[i][i]
                new[i] = (self.augmentedMatrix[i][-1] - total + self.augmentedMatrix[i][i] * self.vect[
                    i]) / x  # subtract every thing then add the value that will not be subtracted   #-1 to access last value in the row
                if new[i] != 0:
                    new[i] = Operations.sig_figs(new[i], self.precision)
            vect2 = self.vect
            self.vect = new
            var1 = f"Iteration {itr + 1}: {self.vect}"
            printlist = printlist + var1
            printlist = printlist + "\n"
            if Operations.check_continue(new, vect2, self.tolerance):
                break

        return printlist
