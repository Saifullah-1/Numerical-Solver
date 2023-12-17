import numpy as np
import re

def getEquations(equation):
    equation = equation.replace(" ",'').replace("-"," -").replace('+',' +')
    equation = equation.strip()
    result = re.split('= |=| ', equation)
    return result
# Remove Spaces and Set the Equations Form

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
#Getting the Unknowns to Check is it's X,Y,Z or X1,X2,X3 For Example

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
# Returns the Coeff Matrix

def resultsMatrix(equations):
    res = []
    for equation in equations:
        res.append(equation[-1])
    return res
# Returns الحدود المطلقة

def convertNumbers(coeff,res):
    for i in range (len(coeff)):
        for j in range (len(coeff[0])):
            coeff[i][j]=float(coeff[i][j])
    for i in range (len(res)) :
        res[i] = float(res[i])
    return coeff,res
# Coefficients are Strings and Chars, They Must be Integers
# ======================
# Important
# ======================
# You Must't Apply this Fn if the coeffs are letters in Gauss (Bonus Point 2), This Fn will Decide the type of Coeff,
# Make a Condition ONLY in Gauss if the function returns 'numbers' use the above converter fn , if 'letters don't use it
def typeOfCoefficients (equation):
    for i in equation[0]:
        if i.isalpha():
            return 'letters'
    return 'numbers'



def getAugMatrix(a,b):
    aug = a
    for i in range(len(aug)):
        aug[i].append(b[i])
    return aug
# Augment Coeffs and الحدود المطلقة Matrices