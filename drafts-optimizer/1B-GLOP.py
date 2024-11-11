# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 21:39:41 2024

@author: Mafu
"""

from ortools.linear_solver import pywraplp

# Create a GLOP solver
solver = pywraplp.Solver.CreateSolver('GLOP')

# Define the integer variables
b1 = solver.IntVar(0, solver.infinity(), 'b1')  # Number of batches of coffee walnut cakes (each batch is 4 cakes)
q2 = solver.IntVar(0, solver.infinity(), 'q2')   # Number of chocolate chip cakes

# Constraints of available pounds sterlings (GBP)
solver.Add(4 * b1 + 1 * q2 <= 99)  # £100 limit: 4 per batch of coffee walnut cakes, 1 per chocolate chip cake

# Profit per cake
q1pr = 1.80 * 4  # Profit per batch of 4 coffee walnut cakes
q2pr = 1.60      # Profit per chocolate chip cake

# Define the objective (maximize profit)
solver.Maximize(q1pr * b1 + q2pr * q2)

# Solve the optimization problem
status = solver.Solve()

# Check if an optimal solution was found
if status == pywraplp.Solver.OPTIMAL:
    # Calculate the actual number of cakes based on the values of b1 and q2
    optimal_batches = int(b1.solution_value())  # Number of batches of 4 coffee walnut cakes
    optimal_q2 = int(q2.solution_value())        # Number of chocolate chip cakes

    # Calculate the maximum profit using the optimized cake values
    max_profit = q1pr * optimal_batches + q2pr * optimal_q2

    # Print results
    print(f'Optimal number of coffee walnut cakes: {optimal_batches * 4}')  # Total coffee walnut cakes
    print(f'Optimal number of chocolate chip cakes: {optimal_q2}')
    print(f'Maximum profit: £{max_profit:.2f}')
else:
    print("The problem does not have an optimal solution.")





