import json
from flask import Flask, render_template, request, flash, redirect, url_for
from pulp import LpProblem, LpVariable, LpMaximize, lpSum, PULP_CBC_CMD
import webbrowser

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for flashing messages

# List to store the IntegerVariable instances
variables_list = []

# IntegerVariable class
class IntegerVariable:
    def __init__(self, name: str, lowerBound: int = 0, upperBound: int = None, profit: float = 0.0, integer: bool = True, multiplier: int = 1):
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

    def to_dict(self):
        """Convert to a dictionary for JSON export."""
        return {
            "name": self.name,
            "lowerBound": self.lowerBound,
            "upperBound": self.upperBound,
            "profit": self.profit,
            "integer": self.integer,
            "multiplier": self.multiplier,
        }

    @staticmethod
    def from_dict(data):
        """Create an IntegerVariable from a dictionary."""
        return IntegerVariable(
            name=data["name"],
            lowerBound=data["lowerBound"],
            upperBound=data["upperBound"],
            profit=data["profit"],
            integer=data["integer"],
            multiplier=data["multiplier"],
        )

# Export variables to a JSON file
def export_variables(filename="variables.json"):
    with open(filename, "w") as f:
        json.dump([var.to_dict() for var in variables_list], f, indent=4)
    flash(f"Variables exported to {filename}!", "success")

# Import variables from a JSON file
def import_variables(filename="variables.json"):
    global variables_list
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            variables_list = [IntegerVariable.from_dict(item) for item in data]
        flash(f"Variables imported from {filename}!", "success")
    except FileNotFoundError:
        flash(f"File {filename} not found.", "error")
    except json.JSONDecodeError:
        flash("Error decoding JSON file.", "error")

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
        optimal_value = lp_vars[var.name].varValue
        if optimal_value is None:
            optimal_value = 0
        else:
            optimal_value = int(optimal_value)
        scaled_value = optimal_value * var.multiplier
        result[var.name] = scaled_value
        max_profit += var.profit * scaled_value

    return max_profit, result

# Combined route for input, optimization, import, and export
@app.route("/", methods=["GET", "POST"])
def index():
    max_profit = None
    result = {}

    if request.method == "POST":
        if "add_variable" in request.form:
            # Get the values from the form and create integer variables
            name = request.form["name"]
            lower_bound = int(request.form["lower_bound"]) if request.form["lower_bound"] else 0
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

        elif "export" in request.form:
            # Export variables to a file
            export_variables()

        elif "import" in request.form:
            # Import variables from a file
            import_variables()

    return render_template("index.html", variables=variables_list, max_profit=max_profit, result=result)

if __name__ == "__main__":
    url = "http://localhost:5000"
    webbrowser.open(url)
    app.run(debug=True)
