"""
Textbook problem 18.24

@author: Jacob Needham
"""

import numpy as np

#two data sets from problmes 18.5 and 18.6
problem5 = 18.5
x_185 = np.matrix([1.6,2,2.5,3.6,4,4.5], dtype = "float")
y_185 = np.matrix([2,8,14,15,8,2], dtype = "float")

problem6 = 18.6
x_186 = np.matrix([1,2,3,5,7,8], dtype = "float")
y_186 = np.matrix([3,6,19,99,291,444], dtype = "float")

'''
Main function defines data series of points and what X is to be found and calls
the cubic spline interpolation to find corresponding Y value.
'''
def Main(x,y,find_x,problem):    
    #put data here:
    n = x.size 
    CubicSplineInt(x,y,n,find_x,problem)

'''
Function takes data series x,y and the length of the data set, n, and finds a
coresponding Y value (y_eval) for an input X value (x_eval).
'''
def CubicSplineInt(x,y,n,x_eval,problem):
    #initilzing matrix A, solution vector b, and 2nd derivates vector Fpp
    A = np.matrix([[0 for x in range(n)] for y in range(n)], dtype = 'float')
    A[0,0] = 1
    A[n-1,n-1] = 1
    
    Fpp = np.matrix([None]*n, dtype = 'float')
    
    b = np.matrix([None]*n, dtype = 'float')
    b[0,0] = 0
    b[0,n-1] = 0
    
    #Populating the A matrix with left hand side of equation 18.37 from book
    #and b matrix with right hand side of same equation.
    for i in range(1,n-1):
        A[i,i-1] = x[0,i] - x[0,i-1]
        A[i,i] = 2*(x[0,i+1] - x[0,i-1])
        A[i,i+1] = x[0,i+1] - x[0,i]
        b[0,i] = (6*(y[0,i+1]-y[0,i]))/(x[0,i+1]-x[0,i]) \
                 + (6*(y[0,i-1]-y[0,i]))/(x[0,i]-x[0,i-1])
    
    #linear algebra to solve for Fpp vector using Fpp = A^-1*b
    Fpp = np.dot(np.linalg.inv(A),np.transpose(b))
    
    #calculating the interpolated point for the chosen x value x_eval
    for i in range(n-1):
        if (x[0,i-1] <= x_eval and x[0,i] >= x_eval):
            y_eval = (Fpp[i-1,0]*(x[0,i]-x_eval)**3)/(6*(x[0,i]-x[0,i-1])) \
                    + (Fpp[i,0]*(x_eval - x[0,i-1])**3)/(6*(x[0,i]-x[0,i-1])) \
                    + ((y[0,i-1]/(x[0,i]-x[0,i-1]))-(Fpp[i-1,0]*(x[0,i]-x[0,i-1]))/6)*\
                    (x[0,i]-x_eval)
                    + ((y[0,i]/(x[0,i]-x[0,i-1]))-(Fpp[i,0]*(x[0,i]-x[0,i-1]))/6)*\
                    (x_eval-x[0,i-1])
    
    print('For the data set from problem ',problem,', and x value=',x_eval,\
          ', the interpolated y value is: ',round(y_eval,4), sep = '')

#calling the function for the two data sets from 18.5 and 18.6
Main(x_185,y_185,2.25,problem5)
Main(x_186,y_186,2.25,problem6)