# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 21:39:41 2024

@author: Mafu
"""

from gekko import GEKKO

# Create GEKKO model
m = GEKKO(remote=False)

# Define the integer variables
b1 = m.Var(lb=0, integer=True)  # Number of batches of coffee walnut cakes (each batch is 4 cakes)
q2 = m.Var(lb=0, integer=True)  # Number of chocolate chip cakes

# Constraints of available pounds sterlings (GBP)
m.Equation(4 * b1 + 1 * q2 <= 100)  # £100 limit: 4 per batch of coffee walnut cakes, 1 per chocolate chip cake

# Profit per cake
q1pr = 1.80 * 4  # Profit per batch of 4 coffee walnut cakes
q2pr = 1.60      # Profit per chocolate chip cake

# Define the objective (maximize profit)
profit = q1pr * b1 + q2pr * q2
m.Maximize(profit)

# Solve the optimization problem
m.solve(disp=False)

# Calculate the actual number of cakes based on the values of b1 and q2
optimal_batches = int(b1.value[0])  # Number of batches of 4 coffee walnut cakes
optimal_q2 = int(q2.value[0])        # Number of chocolate chip cakes

# Calculate the maximum profit using the optimized cake values
max_profit = q1pr * optimal_batches + q2pr * optimal_q2

# Print results
print(f'Optimal number of coffee walnut cakes: {optimal_batches * 4}')  # Total coffee walnut cakes
print(f'Optimal number of chocolate chip cakes: {optimal_q2}')
print(f'Maximum profit: £{max_profit:.2f}')



