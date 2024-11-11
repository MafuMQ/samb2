# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 18:02:18 2024

@author: Mafu
"""

from gekko import GEKKO

# Create GEKKO model
m = GEKKO(remote=False)

# Define the integer variables for the quotients of the cakes
q1 = m.Var(lb=0, integer=True)  # Quotient for coffee walnut cakes
q2 = m.Var(lb=0, integer=True)  # Quotient for chocolate chip cakes

# Multiplyers
Mult1 = 1
Mult2 = 1

# Define the actual number of cakes as multiples of 5
x1 = Mult1 * q1  # Coffee walnut cakes must be a multiple of 5
x2 = Mult2 * q2  # Chocolate chip cakes must be a multiple of 5

# Constraints for flour and sugar
m.Equation(600 * x1 + 400 * x2 <= 12000)  # Total flour in grams (converted from kg)
m.Equation(150 * x1 + 300 * x2 <= 3600)   # Total sugar in grams (converted from kg)
m.Equation(x1 + x2 >= 12)  # At least 12 cakes should be made

# Define the objective (maximize profit)
profit = 1.80 * x1 + 1.60 * x2
m.Maximize(profit)

# Solve the optimization problem
m.solve(disp=False)

# Calculate the actual number of cakes based on the values of q1 and q2
optimal_x1 = Mult1 * int(q1.value[0])
optimal_x2 = Mult2 * int(q2.value[0])

# Calculate the maximum profit using the optimized cake values
max_profit = 1.80 * optimal_x1 + 1.60 * optimal_x2

# Print results
print(f'Optimal number of coffee walnut cakes: {optimal_x1}')
print(f'Optimal number of chocolate chip cakes: {optimal_x2}')
print(f'Maximum profit: £{max_profit:.2f}')




