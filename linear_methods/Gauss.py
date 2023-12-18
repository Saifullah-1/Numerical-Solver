import numpy as np
import re
from math import floor, log10

from Service.operations import Operations


class Gauss:
    def __init__(self, augMatrix, coeffs, unknowns, results, precision):
        self.augMatrix = augMatrix
        self.coeffs = coeffs
        self.unknowns = unknowns
        self.results = results
        self.precision = precision

    def GaussSolver(self):
        str = ""
        str = str + (f"\nLet A the Coefficient Matrix :\n{self.coeffs}\n\nX the Unknowns Vector :\n{self.unknowns}\n\nAnd B the Results Vector :\n{self.results}\n")
        str = str + (f"\nA * X = B\n\nTo Solve, We Must Get the Augmented Matrix :\n{self.augMatrix}\n")
        
        def partialPivoting(aug,row,col):
            print(1)
            pivot = aug[row,col]
            newR = row
            for i in range(row+1,aug.shape[0]) :
                if abs(aug[i,col])>abs(pivot):
                    pivot = aug [i,col]
                    newR = i
            temp = np.array(aug[newR])
            aug[newR] = aug[row]
            aug[row] = temp
            for i in range (aug.shape[0]):
                    for j in range (aug.shape[1]):
                        if aug[i,j]!=0:
                            aug[i,j] == Operations.sig_figs(aug[i,j],self.precision)
            return aug
        
        def ForElimNumbers(aug,str):
            print(2)
            str = str + (f"\n-- Applying Gauss Elimination Method --\n")  
            str = str + (f"\nFirst : [Forward Elimination]\n")
            for i in range (aug.shape[0]):
                    for j in range (aug.shape[1]):
                        if aug[i,j]!=0:
                            aug[i,j] = Operations.sig_figs(aug[i,j],self.precision)
            numOfRows = aug.shape[0]
            numOfCols = aug.shape[1]
            for current in range(numOfRows-1):      #Current Row = Current Col (Pivot)
                aug = partialPivoting (aug,current,current)
                pivot = aug[current,current]
                str = str + (f"\nApplying Partial Pivoting For the Pivot in Row and Column {current+1} : \n{aug}\n")
                str = str + (f"\nNew Pivot = {pivot} \n")
                for i in range (current+1,numOfRows):
                    if aug[i,current] == 0 : 
                        str = str + (f"\nThe Element to be Eliminated in Row {i+1} is Already 0, We Move to The Next Step\n")
                        continue
                    factor = (aug[i,current]/pivot)
                    if factor != 0 : factor = Operations.sig_figs(factor,self.precision)
                    str = str + (f"\nRow {i+1} = Row {i+1} - ({factor} * Row {current+1}) : \n")
                    for j in range (current,numOfCols):
                        if j == current : aug[i,j] = 0
                        else : aug[i,j] -= factor*aug[current,j]
                    for i in range (aug.shape[0]):
                        for j in range (aug.shape[1]):
                            if aug[i,j]!=0:
                                aug[i,j] = Operations.sig_figs(aug[i,j],self.precision)
                    str = str + (f'\n{aug}\n')
            return aug,str
        
        def CheckSolvability (aug,str):
            print(3)
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
            return str,state
        
        def BackSubNumbers(aug,str):
            print(4)
            str = str + (f"\nSecond : [Backword Substitution]\n")
            numOfRows = aug.shape[0]
            result = [0]*numOfRows
            for row in range(numOfRows-1,-1,-1):      #Current Row = Current Col (Pivot)
                sum=0
                str = str + (f"\nFrom Row {row+1}, We Get {self.unknowns[row,0]} : \n")
                for j in range (row+1,numOfRows):
                    sum += result[j]*aug[row,j]
                if sum != 0 : sum = Operations.sig_figs(sum,self.precision)
                str = str + (f"\n({aug[row,row]})*{self.unknowns[row,0]} = {aug[row,numOfRows]} - {sum}\n")
                sum = aug[row,numOfRows]-sum
                if sum != 0 : sum = Operations.sig_figs(sum,self.precision)
                result[row]= sum/aug[row,row]
                for i in range (len(result)):
                    if result[i]!=0:
                        result[i] = Operations.sig_figs(result[i],self.precision)
                str = str + (f"\n{self.unknowns[row,0]} = {result[row]}\n")
            str = str + (f"\nThe Answers = {result}\n")
            return result,str
        
    # =========================================================================================
    # def ForElimLetters(aug,str):          
    #     str = str + (f"\n-- Applying Gauss Elimination Method --\n")  
    #     str = str + (f"\nFirst : [Forward Elimination]\n")
    #     numOfRows = aug.shape[0]
    #     numOfCols = aug.shape[1]
    #     for current in range(numOfRows-1):      #Current Row = Current Col (Pivot)
    #         pivot = aug[current,current]
    #         str = str + (f"\nPivot is {pivot}\n")
    #         for i in range (current+1,numOfRows):
    #             if aug[i,current] == '0' : 
    #                 str = str + (f"\nThe Element to be Eliminated in Row {i+1} is Already 0, We Move to The Next One\n")
    #                 continue
    #             factor = aug[i,current]+'/'+pivot+''
    #             str = str + (f"\nRow {i+1} = Row {i+1} - ( ({factor}) * Row {current+1} ) : \n")
    #             for j in range (current,numOfCols):
    #                 elem = aug[i,j] + '-[(' + factor + ')*(' + aug[current,j] + ')]'
    #                 aug[i,j]= '0' if j==current else elem 
    #             str = str + (f"\n{aug}\n")
    #     return aug,str
    
    # def BackSubLetters(aug,str):      
    #     numOfRows = aug.shape[0]
    #     result = [0]*numOfRows
    #     for row in range(numOfRows-1,-1,-1):      #Current Row = Current Col (Pivot)
    #         sum=0
    #         for j in range (row+1,numOfRows):
    #             sum += result[j]*aug[row,j]
    #         sum = aug[row,numOfRows]-sum
    #         result[row]= sum/aug[row,row]
    #     return result,str
    # ============================================================================================
        np.set_printoptions(suppress = True)
        # if (type=='numbers'):
        self.augMatrix, str = ForElimNumbers(self.augMatrix, str)
        str, state = CheckSolvability(self.augMatrix, str)
        if (state=='continue'):
            str = str + (f"\nThere is a Unique Solution for the System\n")
            final,str = BackSubNumbers(self.augMatrix,str)

        # else:
        #     for i in range(augMatrix.shape[0]):
        #         for j in range(augMatrix.shape[1]):
        #             if augMatrix[i,j][0]=='+': augMatrix[i,j]=augMatrix[i,j][1:]
        #     # augMatrix,str = ForElimLetters(augMatrix,str)
        #     # final = BackSubLetters(augMatrix)
        
        return str




