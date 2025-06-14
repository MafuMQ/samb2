# -*- coding: utf-8 -*-
"""
1B-PuLP-A.py

This script demonstrates a simple integer linear programming optimization using PuLP.
It defines a class for integer variables (e.g., cakes to produce), sets up an optimization
problem to maximize profit under a budget constraint, and solves for the optimal production
quantities.

Classes:
    IntegerVariable: Represents a variable in the optimization problem with bounds, profit, and multiplier.

Functions:
    create_integer_variable: Helper to create and store IntegerVariable instances.
    optimize: Sets up and solves the optimization problem using PuLP.

Example:
    The script creates two cake variables and optimizes their production for maximum profit
    under a £13 budget constraint.

@author: Mafu
@date: 2024-10-11
"""

from pulp import LpProblem, LpVariable, LpMaximize, lpSum, PULP_CBC_CMD

class IntegerVariable:
    """
    Represents an integer (or continuous) variable for optimization.

    Attributes:
        name (str): Name of the variable.
        lowerBound (int): Minimum value.
        upperBound (int or None): Maximum value (None for unbounded above).
        profit (float): Profit per unit (or per batch if multiplier > 1).
        integer (bool): Whether the variable is integer (default True).
        multiplier (int): Multiplier for scaling (e.g., batch size).
    """
    def __init__(self, name: str, lowerBound: int, upperBound: int | None, profit: float, integer: bool = True, multiplier: int = 1):
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
    
    def set_bounds(self, lower: int, upper: int):
        """Set new lower and upper bounds for the variable."""
        self.lowerBound = lower
        self.upperBound = upper
    
    def set_multiplier(self, multiplier: int):
        """Set a new multiplier for the variable."""
        self.multiplier = multiplier
    
    def scaled_value(self, value: int):
        """
        Return the scaled value (value * multiplier) if within bounds.
        Raises ValueError if value is out of bounds.
        """
        if value < self.lowerBound or (self.upperBound is not None and value > self.upperBound):
            raise ValueError(f"Value {value} is out of bounds for {self.name}.")
        return value * self.multiplier

# List to store the IntegerVariable instances
variables_list = []


def create_integer_variable(name: str, lowerBound: int, upperBound: int | None, profit: float, integer: bool = True, multiplier: int = 1):
    """
    Create an IntegerVariable and add it to the global variables_list.

    Args:
        name (str): Name of the variable.
        lowerBound (int): Minimum value.
        upperBound (int or None): Maximum value.
        profit (float): Profit per unit.
        integer (bool): Whether variable is integer.
        multiplier (int): Multiplier for scaling.
    """
    var = IntegerVariable(name=name, lowerBound=lowerBound, upperBound=upperBound, profit=profit, integer=integer, multiplier=multiplier)
    variables_list.append(var)
    print(f"Added variable: {var}")


def optimize(variables: list[IntegerVariable]):
    """
    Set up and solve the integer programming problem to maximize profit.

    Args:
        variables (list[IntegerVariable]): List of variables to optimize.
    """
    model = LpProblem("Cake_Production", LpMaximize)
    lp_vars = {}
    
    # Create PuLP variables for each IntegerVariable
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


