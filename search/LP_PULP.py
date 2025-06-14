# -*- coding: utf-8 -*-
"""
LP_PULP.py

Core logic for defining and solving integer linear programming (ILP) problems using PuLP.

- Defines the IntegerVariable class for optimization variables.
- Provides functions to create variables, build and solve the optimization model, and interface with variable lists.
- Used as a backend for higher-level interfaces (see LP_Interface.py).

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
        upperBound (int): Maximum value.
        profit (float): Profit per unit (or per batch if multiplier > 1).
        integer (bool): Whether the variable is integer (default True).
        multiplier (int): Multiplier for scaling (e.g., batch size).
    """
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
        if not (self.lowerBound <= value <= self.upperBound):
            raise ValueError(f"Value {value} is out of bounds for {self.name}.")
        return value * self.multiplier

# List to store the IntegerVariable instances
variables_list = []

# Function to create an IntegerVariable instance and add it to the list
def create_integer_variable(name: str, lowerBound: int, upperBound: int, profit: float, integer: bool = True, multiplier: int = 1):
    """
    Create an IntegerVariable and add it to the global variables_list.

    Args:
        name (str): Name of the variable.
        lowerBound (int): Minimum value.
        upperBound (int): Maximum value.
        profit (float): Profit per unit.
        integer (bool): Whether variable is integer.
        multiplier (int): Multiplier for scaling.
    """
    var = IntegerVariable(name=name, lowerBound=lowerBound, upperBound=upperBound, profit=profit, integer=integer, multiplier=multiplier)
    variables_list.append(var)
    #print(f"Added variable: {var}")


def optimize(variables: list[IntegerVariable], Budget, msgShow = False, EachVariableShow = True):
    """
    Set up and solve the integer programming problem to maximize profit.

    Args:
        variables (list[IntegerVariable]): List of variables to optimize.
        Budget (float): The budget constraint for the optimization.
        msgShow (bool): Whether to show solver messages (default: False).
        EachVariableShow (bool): Whether to print each variable's result (default: True).
    Returns:
        float: The maximum profit achieved (rounded to 2 decimal places).
    """
    model = LpProblem("Cake_Production", LpMaximize)
    lp_vars = {}
    
    # Create PuLP variables for each IntegerVariable
    for var in variables:
        lp_vars[var.name] = LpVariable(var.name, lowBound=var.lowerBound, upBound=var.upperBound, cat='Integer' if var.integer else 'Continuous')
    
    # Constraints of available pounds sterlings (GBP) with multiplier applied
    budget_constraint = lpSum([var.multiplier * lp_vars[var.name] for var in variables])
    model += (budget_constraint <= Budget, "Budget_Constraint")  # £13 limit
    
    # Define the objective (maximize profit)
    total_profit = lpSum([var.profit * var.multiplier * lp_vars[var.name] for var in variables])
    model += total_profit, "Total_Profit"
    
    # Solve the optimization problem
    solver = PULP_CBC_CMD(msg=msgShow)
    model.solve(solver)
    
    # Print results for each variable
    max_profit = 0
    if EachVariableShow:
        print("\n")

    for var in variables:
        optimal_value = int(lp_vars[var.name].varValue)
        scaled_value = optimal_value * var.multiplier
        if EachVariableShow:
            print(f'Optimal number of {var.name}: {scaled_value}')
        max_profit += var.profit * scaled_value
    
    # Print total maximum profit
    if EachVariableShow:
        print(f'Maximum profit: £{max_profit:.2f}')
    

    return float(f'{max_profit:.2f}')

def dictList2Var(dictList):
    """
    Convert a list of variable dictionaries to IntegerVariable instances and store them in variables_list.
    Clears the existing list before adding new variables.

    Args:
        dictList (list): List of dictionaries, each representing a variable.
    """
    global variables_list
    variables_list.clear()

    # Create IntegerVariable instances and add them to the list
    for i in dictList:
        create_integer_variable(name=i["name"], lowerBound=i["lowerBound"], upperBound=i["upperBound"], profit=i["profit"], multiplier=i["multiplier"])

def optimizeCall(Budget, Show):
    """
    Call optimize with the list of IntegerVariable instances.

    Args:
        Budget (float): The budget constraint for the optimization.
        Show (bool): Whether to print each variable's result.
    Returns:
        float: The maximum profit achieved.
    """
    return optimize(variables_list, Budget, EachVariableShow = Show)