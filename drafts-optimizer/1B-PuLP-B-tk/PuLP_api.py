from pulp import LpProblem, LpVariable, LpMaximize, lpSum, PULP_CBC_CMD

class IntegerVariable:
    def __init__(self, name: str, lowerBound: int, upperBound: int, profit: float, integer: bool = True, multiplier: int = 1):
        self.name = name
        self.lowerBound = lowerBound
        self.upperBound = upperBound
        self.profit = profit
        self.integer = integer
        self.multiplier = multiplier

    def __repr__(self):
        return (f"IntegerVariable(name={self.name}, lowerBound={self.lowerBound}, "
                f"upperBound={self.upperBound}, profit={self.profit}, integer={self.integer}, "
                f"multiplier={self.multiplier})")

# List to store IntegerVariable instances
variables_list = []

# Function to create an IntegerVariable instance and add it to the list
def create_integer_variable(name: str, lowerBound: int, upperBound: int, profit: float, integer: bool = True, multiplier: int = 1):
    var = IntegerVariable(name=name, lowerBound=lowerBound, upperBound=upperBound, profit=profit, integer=integer, multiplier=multiplier)
    variables_list.append(var)
    print(f"Added variable: {var}")

# Optimization function
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
    
    # Prepare results for each variable
    max_profit = 0
    resultTest = ''
    for var in variables:
        optimal_value = int(lp_vars[var.name].varValue)
        scaled_value = optimal_value * var.multiplier
        resultTest += f'Optimal number of {var.name}: {scaled_value}\n'
        max_profit += var.profit * scaled_value
    
    return f"Maximum profit: £{max_profit:.2f}\n{resultTest}"
