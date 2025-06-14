"""
LP_Interface.py

Interface for setting up and solving a linear programming (LP) problem using helper functions from LP_PULP.

- Defines variables for an optimization problem (e.g., cake production).
- Provides functions to add variables to the model and to call the optimizer.

@author: Mafu
@date: 2025-06-14
"""

from LP_PULP import dictList2Var, optimizeCall

Budget = 13  # Budget constraint for the optimization problem

ListofVar = []  # List to store variable definitions as dictionaries

# Define variables for the optimization problem
coffee_cake = {"name":"coffee cake", "lowerBound":0, "upperBound":None, "profit":1.80, "multiplier":8}
ListofVar.append(coffee_cake)

chocolate_cake = {"name":"chocolate cake", "lowerBound":0, "upperBound":None, "profit":1.60, "multiplier":1}
ListofVar.append(chocolate_cake)


def addVariablesToModel(Lv = ListofVar):
    """
    Add a list of variable dictionaries to the optimization model.

    Args:
        Lv (list): List of variable dictionaries to add (default: ListofVar).
    """
    dictList2Var(Lv)


def LP_optimizeCall(Budget, Show = False):
    """
    Call the optimizer with the given budget and display option.

    Args:
        Budget (float): The budget constraint for the optimization.
        Show (bool): Whether to display detailed output (default: False).
    Returns:
        Result of optimizeCall from LP_PULP.
    """
    return optimizeCall(Budget, Show)
