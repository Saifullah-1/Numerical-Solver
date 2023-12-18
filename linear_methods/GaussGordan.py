import numpy as np
import re
from math import floor, log10

from Service.operations import Operations


class GaussJordan:
    def __init__(self, augMatrix, coeffs, unknowns, results, precision):
        self.augMatrix = augMatrix
        self.coeffs = coeffs
        self.unknowns = unknowns
        self.results = results
        self.precision = precision

    def GaussGordanSolver(self):
        str = ""
        str = str + (f"\nLet A the Coefficient Matrix :\n{self.coeffs}\n\nX the Unknowns Vector :\n{self.unknowns}\n\nAnd B the Results Vector :\n{self.results}\n")
        str = str + (f"\nA * X = B\n\nTo Solve, We Must Get the Augmented Matrix :\n{self.augMatrix}\n")
        np.set_printoptions(suppress= True)
        
        def CheckSolvability(aug, str):
            str = str + (f"\nChecking the Solvability of the System")
            rows = aug.shape[0]
            zeroCoeffs = False
            zeroAug = False
            state = 'continue'
            for i in range (aug.shape[0]):
                zeroCoeffs = True
                zeroAug = True
                for j in range (aug.shape[0]):
                    if (aug[i,j]!=0) :
                        zeroCoeffs = False
                        break
                if aug [i,rows] != 0 : zeroAug=False
                if zeroCoeffs and not zeroAug : 
                    str = str + (f"\nThere is No Soultion for the System\n") 
                    state = 'terminate'
                elif zeroCoeffs and zeroAug :
                    str = str + (f"\nThere is an Infinite Number of Solutions\n")
                    state = 'terminate'
            return str, state
        
        def scaling(aug,row,col):
            for i in range(row,aug.shape[0]) :
                largest = abs(aug[i,col])
                for j in range(col,aug.shape[1]-1):
                    if abs(aug[i,j])>largest:
                        largest = abs(aug[i,j])
                for j in range(col,aug.shape[1]):
                    aug[i,j] /= largest        
            return aug
        
        def partialPivoting(aug,row,col,str):
            temp = np.copy(aug)
            temp = scaling(temp,row,col)
            str = str + (f"\nApplying Scaling to Determine if the Matrix needs Partial Pivoting\n{temp}\n")
            pivot = temp[row,col]
            newR = row
            for i in range(row+1,temp.shape[0]) :
                if abs(temp[i,col])>abs(pivot):
                    pivot = temp [i,col]
                    newR = i
            temp = np.array(aug[newR])
            aug[newR] = aug[row]
            aug[row] = temp
            for i in range (aug.shape[0]):
                    for j in range (aug.shape[1]):
                        if aug[i,j]!=0:
                            aug[i,j] = Operations.sig_figs(aug[i,j],self.precision)
            return aug,str
        
        def Elimination(aug,str):    
            str = str + (f"\n-- Applying Gauss Gordan Method --\n")    
            numOfRows = aug.shape[0]
            numOfCols = aug.shape[1]
            # 
            for i in range (aug.shape[0]):
                for j in range (aug.shape[1]):
                    if aug[i,j]!=0:
                        aug[i,j] = Operations.sig_figs(aug[i,j],self.precision)
            # 
            for current in range(numOfRows):      #Current Row = Current Col (Pivot)
                aug,str = partialPivoting (aug,current,current,str)
                pivot = aug[current,current]
                str = str + (f"\nApplying Partial Pivoting Based On Scaling For the Pivot in Row and Column {current+1} : \n{aug}\n")
                str = str + (f"\nNew Pivot = {pivot} \n")
                if pivot == 0 :
                    str,state = CheckSolvability(aug,str)
                    if state=='terminate' :
                        return aug,str
                for i in range (0,numOfRows):
                    if i==current : continue
                    elif aug[i,current] == 0 : 
                        str = str + (f"\nThe Element to be Eliminated in Row {i+1} is Already 0, We Move to The Next Step\n")
                        continue
                    factor = (aug[i,current]/pivot)
                    if factor != 0 : factor = Operations.sig_figs(factor, self.precision)
                    str = str + (f"\nRow {i+1} = Row {i+1} - ({factor} * Row {current+1}) : \n")
                    for j in range (current,numOfCols):
                        if j == current : aug[i,j] = 0
                        else : aug[i,j] -= factor*aug[current,j]
                    for i in range (aug.shape[0]):
                        for j in range (aug.shape[1]):
                            if aug[i,j]!=0:
                                aug[i,j] = Operations.sig_figs(aug[i,j],self.precision)
                    str = str + (f'\n{aug}\n')
            answers = np.array([0.0]*numOfRows)
            str,state = CheckSolvability(aug,str)
            if state == 'continue':
                str = str + (f"\nThere is a Unique Solution for the System\n")
                str = str +(f"\nNormalizing the Pivots : \n")
                for i in range(numOfRows):                #Normalizing
                    aug[i,numOfCols-1] /= aug[i,i]
                    aug[i,i] = 1
                    answers[i]=aug[i,numOfCols-1]
                for i in range (aug.shape[0]):
                    for j in range (aug.shape[1]):
                        if aug[i,j]!=0:
                            aug[i,j] = Operations.sig_figs(aug[i,j], self.precision)
                for i in range (len(answers)):
                    if answers[i] != 0:
                        answers [i] = Operations.sig_figs(answers[i], self.precision)
                str = str + (f"\n{self.augMatrix}\n")
                str = str + (f"\nThe Answers = {answers}\n")
            return str
        return Elimination(self.augMatrix, str)                       # returns
