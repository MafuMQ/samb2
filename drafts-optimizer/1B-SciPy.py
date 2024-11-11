# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 21:39:41 2024

@author: Mafu
"""

import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

# Coefficients for the objective function (profit)
c = np.array([-1.80, -1.60])  # Negative because milp minimizes

# Constraints matrix (for flour and sugar limits and minimum cakes)
A = np.array([[600, 400],    # Flour constraint
              [150, 300],    # Sugar constraint
              [-1, -1]])     # Minimum cake constraint (in negative form for milp)

# Right-hand side of the constraints
b = np.array([12000, 3600, -12])  # Flour, sugar, and at least 12 cakes (negative)

# Bounds for the decision variables (x1, x2)
lb = [0, 0]  # Lower bound: both decision variables should be >= 0
ub = [np.inf, np.inf]  # Upper bound: no specific upper limit

# Define bounds object
bounds = Bounds(lb, ub)

# Define the constraint object
linear_constraint = LinearConstraint(A, [-np.inf, -np.inf, -np.inf], b)

# Integrality constraints (both variables are integers)
integrality = np.array([1, 1])  # 1 means integer variable

# Solve the mixed-integer linear program
res = milp(c=c, integrality=integrality, constraints=[linear_constraint], bounds=bounds)

# Extract the solution
optimal_x1 = res.x[0]
optimal_x2 = res.x[1]
max_profit = -res.fun  # Convert back to a maximization result by negating the objective

# Print results
print(f'Optimal number of coffee walnut cakes: {optimal_x1}')
print(f'Optimal number of chocolate chip cakes: {optimal_x2}')
print(f'Maximum profit: £{max_profit:.2f}')







