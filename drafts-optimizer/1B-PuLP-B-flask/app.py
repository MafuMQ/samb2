from flask import Flask, render_template, request, flash
from pulp import LpProblem, LpVariable, LpMaximize, lpSum, PULP_CBC_CMD

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for flashing messages

# List to store the IntegerVariable instances
variables_list = []

# IntegerVariable class as before
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

# Function to create an IntegerVariable instance and add it to the list
def create_integer_variable(name: str, lowerBound: int, upperBound: int, profit: float, integer: bool = True, multiplier: int = 1):
    var = IntegerVariable(name=name, lowerBound=lowerBound, upperBound=upperBound, profit=profit, integer=integer, multiplier=multiplier)
    variables_list.append(var)

# Optimize function to process variables in the list
def optimize(variables):
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
    
    # Gather results
    max_profit = 0
    result = {}
    for var in variables:
        optimal_value = int(lp_vars[var.name].varValue)
        scaled_value = optimal_value * var.multiplier
        result[var.name] = scaled_value
        max_profit += var.profit * scaled_value

    return max_profit, result

# Combined route for both input and results
@app.route("/", methods=["GET", "POST"])
def index():
    max_profit = None
    result = {}

    if request.method == "POST":
        if "add_variable" in request.form:
            # Get the values from the form and create integer variables
            name = request.form["name"]
            lower_bound = int(request.form["lower_bound"]) if request.form["lower_bound"] else None
            upper_bound = int(request.form["upper_bound"]) if request.form["upper_bound"] else None
            profit = float(request.form["profit"])
            integer = bool(request.form.get("integer"))
            multiplier = int(request.form["multiplier"])
            
            create_integer_variable(name, lower_bound, upper_bound, profit, integer, multiplier)
            flash("Variable added successfully!", "success")
        
        elif "optimize" in request.form:
            # Perform the optimization when the button is clicked
            if variables_list:
                max_profit, result = optimize(variables_list)
            else:
                flash("No variables to optimize. Add variables first.", "error")

    return render_template("index.html", variables=variables_list, max_profit=max_profit, result=result)

if __name__ == "__main__":
    app.run(debug=True)
