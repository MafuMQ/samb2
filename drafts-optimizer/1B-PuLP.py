# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 21:39:41 2024

@author: Mafu
"""

from pulp import LpProblem, LpVariable, LpMaximize, lpSum, LpStatus, value, PULP_CBC_CMD

def optimize():
    # Create a PuLP model
    model = LpProblem("Cake_Production", LpMaximize)
    
    # Define the integer variables
    b1 = LpVariable("b1", lowBound=0, cat='Integer')  # Number of batches of coffee walnut cakes (each batch is 8 cakes)
    q2 = LpVariable("q2", lowBound=0, cat='Integer')  # Number of chocolate chip cakes
    
    # Constraints of available pounds sterlings (GBP)
    model += (8 * b1 + 1 * q2 <= 13, "Budget_Constraint")  # £13 limit
    
    # Profit per cake
    q1pr = 1.80 * 8  # Profit per batch of 8 coffee walnut cakes
    q2pr = 1.60      # Profit per chocolate chip cake
    
    # Define the objective (maximize profit)
    model += lpSum([q1pr * b1, q2pr * q2]), "Total_Profit"
    
    # Solve the optimization problem
    solver = PULP_CBC_CMD(msg=False)
    #solver = None
    model.solve(solver)
    
    # Calculate the actual number of cakes based on the values of b1 and q2
    optimal_batches = int(b1.varValue)  # Number of batches of 8 coffee walnut cakes
    optimal_q2 = int(q2.varValue)        # Number of chocolate chip cakes
    
    # Calculate the maximum profit using the optimized cake values
    max_profit = q1pr * optimal_batches + q2pr * optimal_q2
    
    # Print results
    print(f'Optimal number of coffee walnut cakes: {optimal_batches * 8}')  # Total coffee walnut cakes
    print(f'Optimal number of chocolate chip cakes: {optimal_q2}')
    print(f'Maximum profit: £{max_profit:.2f}')
    
    return

optimize()

