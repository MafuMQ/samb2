# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 21:39:41 2024

@author: Mafu
"""

from pulp import LpProblem, LpVariable, LpMaximize, lpSum, PULP_CBC_CMD

class IntegerVariable:
    def __init__(self, name: str, lowerBound: int, upperBound: int, profit: float, integer: bool = True, multiplier: int = 1):
        self.name = name
        self.lowerBound = lowerBound
        self.upperBound = upperBound
        self.profit = profit  # Profit per cake (or per batch if multiplier > 1)
        self.integer = integer
        self.multiplier = multiplier

    def __repr__(self):
        return (f"IntegerVariable(name={self.name}, lowerBound={self.lowerBound}, "
                f"upperBound={self.upperBound}, profit={self.profit}, integer={self.integer}, "
                f"multiplier={self.multiplier})")
    
    # Method to set new bounds
    def set_bounds(self, lower: int, upper: int):
        self.lowerBound = lower
        self.upperBound = upper
    
    # Method to adjust the multiplier
    def set_multiplier(self, multiplier: int):
        self.multiplier = multiplier
    
    # Example method for a possible computation or use case
    def scaled_value(self, value: int):
        if not (self.lowerBound <= value <= self.upperBound):
            raise ValueError(f"Value {value} is out of bounds for {self.name}.")
        return value * self.multiplier

# List to store the IntegerVariable instances
variables_list = []

# Function to create an IntegerVariable instance and add it to the list
def create_integer_variable(name: str, lowerBound: int, upperBound: int, profit: float, integer: bool = True, multiplier: int = 1):
    var = IntegerVariable(name=name, lowerBound=lowerBound, upperBound=upperBound, profit=profit, integer=integer, multiplier=multiplier)
    variables_list.append(var)
    print(f"Added variable: {var}")


def optimize(variables: list[IntegerVariable]):
    model = LpProblem("Cake_Production", LpMaximize)
    lp_vars = {}
    
    for var in variables:
        lp_vars[var.name] = LpVariable(var.name, lowBound=var.lowerBound, upBound=var.upperBound, cat='Integer' if var.integer else 'Continuous')
    
    # Constraints of available pounds sterlings (GBP) with multiplier applied
    budget_constraint = lpSum([var.multiplier * lp_vars[var.name] for var in variables])
    model += (budget_constraint <= 13, "Budget_Constraint")  # £13 limit
    
    # Define the objective (maximize profit)
    total_profit = lpSum([var.profit * var.multiplier * lp_vars[var.name] for var in variables])
    model += total_profit, "Total_Profit"
    
    # Solve the optimization problem
    solver = PULP_CBC_CMD(msg=False)
    model.solve(solver)
    
    # Print results for each variable
    max_profit = 0
    print("\n")
    for var in variables:
        optimal_value = int(lp_vars[var.name].varValue)
        scaled_value = optimal_value * var.multiplier
        print(f'Optimal number of {var.name}: {scaled_value}')
        max_profit += var.profit * scaled_value
    
    # Print total maximum profit
    print(f'Maximum profit: £{max_profit:.2f}')
    
    return

# Create IntegerVariable instances and add them to the list
create_integer_variable(name="coffee cake", lowerBound=0, upperBound=None, profit=1.80, multiplier=8)  # Coffee walnut cakes
create_integer_variable(name="chocolate cake", lowerBound=0, upperBound=None, profit=1.60, multiplier=1)  # Chocolate chip cakes


# Call optimize with the list of IntegerVariable instances
optimize(variables_list)    


