import numpy as np
import re
from math import floor, log10

# equ1 = '0.05462498 x1  -  1.89623    x2 - 79856 x3 = - 0.7845623'
# equ2 = '4.849629 x1  -  1.8452603    x2 - 0.874652 x3 =  0.21618'
# equ3 = '0x1  +00.08941981653    x2 -0.954625x3= 3.531284964'
# equs = [equ1,equ2,equ3]
# Prec = 5


def PrepareEquations(equs):
    def getEquations(equation):
        equation = equation.replace(" ",'').replace("-"," -").replace('+',' +')
        equation = equation.strip()
        result = re.split('= |=| ', equation)
        return result
    
    def Unknowns(equations):
        operands = []
        for equation in equations:
            for term in equation[:-1]:
                ind =  -1
                unknown = term[ind]
                while unknown[0].isnumeric():
                    ind -= 1
                    unknown = term[ind]+unknown
                if not unknown in operands:
                    operands.append(unknown)
        return operands
    
    def coefficientMatrix(unknowns,equations):
        coeff = []
        for equation in equations:
            temp = unknowns
            row = ['0'] * len(equations)
            for term in equation[:-1]:
                for unknown in temp:
                    if (unknown in term):
                        operand = term[:-len(unknown)]
                        row[unknowns.index(unknown)] = operand
                        break
            coeff.append(row)
        return coeff
    
    def resultsMatrix(equations):
        res = []
        for equation in equations:
            res.append(equation[-1])
        return res
    
    def convertNumbers(coeff,res):
        for i in range (len(coeff)):
            for j in range (len(coeff[0])):
                if coeff[i][j] == '-' : coeff[i][j] = -1.0
                elif coeff[i][j] == '+' : coeff[i][j] = 1.0
                else : coeff[i][j]=float(coeff[i][j])
        for i in range (len(res)) :
            res[i] = float(res[i])
        return coeff,res
        
    def getAugMatrix(a,b):
        aug = a
        for i in range(len(aug)):
            aug[i].append(b[i])
        return aug
    
    n=len(equs) #Num of Equations
    for i in range(len(equs)) : equs[i] = getEquations(equs[i])
    unknowns=  Unknowns(equs)
    coeffs = coefficientMatrix(unknowns,equs)
    results = resultsMatrix(equs)
    coeffs , results = convertNumbers(coeffs,results)
    coeffs = np.array(coeffs).reshape(n,n)
    results = np.array(results).reshape(n,1)
    unknowns = np.array(unknowns).reshape(n,1)
    augMatrix = np.matrix(coeffs)
    augMatrix = np.append (augMatrix,results,axis=1)
    
    return augMatrix,coeffs,unknowns,results


