"""
1B-PuLP-B-flask/app.py

A Flask web application for defining and solving integer linear programming problems (e.g., maximizing profit for cake production under a budget constraint).

Features:
- Add, import, export, and download optimization variables (e.g., cakes).
- Set a budget constraint and maximize profit using PuLP.
- Web interface for user interaction.

Classes:
    IntegerVariable: Represents a variable in the optimization problem.

Functions:
    create_integer_variable: Helper to create and store IntegerVariable instances.
    optimize: Sets up and solves the optimization problem using PuLP.
    Flask routes: index, export_variables, import_variables, download_variables.

@author: Mafu
@date: 2024-10-11
"""

import os
import json
import threading
import time
from flask import Flask, render_template, request, flash, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from pulp import LpProblem, LpVariable, LpMaximize, lpSum, PULP_CBC_CMD
import webbrowser

app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'uploads'
EXPORT_FOLDER = 'exports'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXPORT_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['EXPORT_FOLDER'] = EXPORT_FOLDER

budget = 97
# List to store the IntegerVariable instances
variables_list = []

# IntegerVariable class
class IntegerVariable:
    """
    Represents an integer (or continuous) variable for optimization.

    Attributes:
        name (str): Name of the variable.
        lowerBound (int): Minimum value.
        upperBound (int or None): Maximum value (None for unbounded above).
        profit (float): Profit per unit.
        integer (bool): Whether the variable is integer (default True).
        multiplier (int): Multiplier for scaling (e.g., batch size).
    """
    def __init__(self, name: str, lowerBound: int = 0, upperBound: int | None = None, profit: float = 0.0, integer: bool = True, multiplier: int = 1):
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

# Function to create an IntegerVariable instance and add it to the list

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

# Optimize function to process variables in the list

def optimize(variables):
    """
    Set up and solve the integer programming problem to maximize profit.

    Args:
        variables (list[IntegerVariable]): List of variables to optimize.
    Returns:
        max_profit (float): The maximum profit achieved.
        result (dict): Dictionary of variable names and their optimal scaled values.
    """
    model = LpProblem("Cake_Production", LpMaximize)
    lp_vars = {}

    # Create PuLP variables for each IntegerVariable
    for var in variables:
        lp_vars[var.name] = LpVariable(var.name, lowBound=var.lowerBound, upBound=var.upperBound, cat='Integer' if var.integer else 'Continuous')
    
    # Constraints of available pounds sterlings (GBP) with multiplier applied
    sumOfAllVariables = lpSum([var.multiplier * lp_vars[var.name] for var in variables])
    model += (sumOfAllVariables <= budget, "Budget_Constraint")  # Budget limit
    
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

# Routes
@app.route("/", methods=["GET", "POST"])
def index():
    """
    Main page for adding variables, updating budget, and running optimization.
    Handles form submissions for all main actions.
    """
    global budget
    max_profit = None
    result = {}

    if request.method == "POST":
        if "update_budget" in request.form:
            try:
                budget = int(request.form["budget"])
                flash("Budget updated successfully!", "success")
            except ValueError:
                flash("Invalid budget value. Please enter a valid number.", "error")
        
        elif "add_variable" in request.form:
            name = request.form["name"]
            lower_bound = int(request.form["lower_bound"]) if request.form["lower_bound"] else 0
            upper_bound = int(request.form["upper_bound"]) if request.form["upper_bound"] else None
            profit = float(request.form["profit"])
            integer = bool(request.form.get("integer"))
            multiplier = int(request.form["multiplier"])
            
            create_integer_variable(name, lower_bound, upper_bound, profit, integer, multiplier)
            flash("Variable added successfully!", "success")
        
        elif "optimize" in request.form:
            if variables_list:
                max_profit, result = optimize(variables_list)
            else:
                flash("No variables to optimize. Add variables first.", "error")

    return render_template("index.html", variables=variables_list, max_profit=max_profit, result=result, budget=budget)


@app.route("/export", methods=["POST"])
def export_variables():
    """
    Export the current variables_list to a JSON file in the exports folder.
    """
    filename = request.form.get("filename", "variables.json")
    filepath = os.path.join(app.config['EXPORT_FOLDER'], secure_filename(filename))
    with open(filepath, "w") as f:
        json.dump([var.to_dict() for var in variables_list], f, indent=4)
    flash(f"Variables exported to {filepath}!", "success")
    return redirect(url_for("index"))

@app.route("/import", methods=["POST"])
def import_variables():
    """
    Import variables from a JSON file uploaded by the user.
    """
    if "file" not in request.files:
        flash("No file selected for importing.", "error")
        return redirect(url_for("index"))

    file = request.files["file"]
    filename = file.filename or ""
    if filename == "":
        flash("No file selected for importing.", "error")
        return redirect(url_for("index"))

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
    file.save(filepath)

    global variables_list
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
            variables_list = [IntegerVariable.from_dict(item) for item in data]
        flash(f"Variables imported from {file.filename}!", "success")
    except Exception as e:
        flash(f"Error importing variables: {e}", "error")

    return redirect(url_for("index"))

@app.route("/download", methods=["POST"])
def download_variables():
    """
    Export variables as a downloadable JSON file with a specified filename.
    """
    filename = request.form.get("filename", "variables.json").strip()  # Get filename from form input
    if not filename.endswith(".json"):
        filename += ".json"  # Ensure the filename has a .json extension

    filepath = os.path.join(app.config['EXPORT_FOLDER'], secure_filename(filename))
    with open(filepath, "w") as f:
        json.dump([var.to_dict() for var in variables_list], f, indent=4)

    flash(f"Variables saved as {filename}!", "success")
    return send_file(filepath, as_attachment=True, download_name=filename)

if __name__ == "__main__":
    url = "http://localhost:5000"
    def open_browser():
        time.sleep(1)
        webbrowser.open(url)

    threading.Thread(target=open_browser).start()
    app.run(debug=True, use_reloader=False) #prevents opening 2 tabs on start, disables automatic refreshing/restarting when changes are made to code
