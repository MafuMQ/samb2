# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 21:39:41 2024

@author: Mafu
"""

import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from pulp import LpProblem, LpVariable, LpMaximize, lpSum, PULP_CBC_CMD

# Assuming the IntegerVariable class is already defined
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

# List to store the IntegerVariable instances
variables_list = []

# Function to create an IntegerVariable instance and add it to the list
def create_integer_variable(name: str, lowerBound: int, upperBound: int, profit: float, integer: bool = True, multiplier: int = 1):
    var = IntegerVariable(name=name, lowerBound=lowerBound, upperBound=upperBound, profit=profit, integer=integer, multiplier=multiplier)
    variables_list.append(var)
    print(f"Added variable: {var}")

# Optimize function to process variables in the list
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
    resultTest = ''
    for var in variables:
        optimal_value = int(lp_vars[var.name].varValue)
        scaled_value = optimal_value * var.multiplier
        resultTest += f'Optimal number of {var.name}: {scaled_value}\n'
        max_profit += var.profit * scaled_value
    
    messagebox.showinfo("Optimization Result", f"Maximum profit: £{max_profit:.2f}\n{resultTest}")

# GUI Application
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Optimizer")
        
        # Treeview to display variables in table format
        self.variable_table = ttk.Treeview(self, columns=("Name", "Lower Bound", "Upper Bound", "Profit", "Integer", "Multiplier"), show='headings')
        self.variable_table.heading("Name", text="Name")
        self.variable_table.heading("Lower Bound", text="Lower Bound")
        self.variable_table.heading("Upper Bound", text="Upper Bound")
        self.variable_table.heading("Profit", text="Profit")
        self.variable_table.heading("Integer", text="Integer")
        self.variable_table.heading("Multiplier", text="Multiplier")
        
        self.variable_table.pack(pady=10, padx=10)
        
        # Add button to add a new variable
        self.add_button = tk.Button(self, text="Add Variable", command=self.open_add_dialog)
        self.add_button.pack(pady=5)
        
        # Optimize button to call the optimize function
        self.optimize_button = tk.Button(self, text="Optimize", command=self.call_optimize)
        self.optimize_button.pack(pady=5)

    # Function to update the table with the current variables_list
    def update_table(self):
        self.variable_table.delete(*self.variable_table.get_children())
        for var in variables_list:
            self.variable_table.insert("", "end", values=(var.name, var.lowerBound, var.upperBound, var.profit, var.integer, var.multiplier))

    # Function to open the add variable dialog
    def open_add_dialog(self):
        AddVariableDialog(self)

    # Function to call optimize and show result
    def call_optimize(self):
        if variables_list:
            optimize(variables_list)
        else:
            messagebox.showwarning("No Variables", "No variables to optimize!")

# Dialog window to add variables
class AddVariableDialog(simpledialog.Dialog):
    def __init__(self, parent):
        super().__init__(parent, "Add Integer Variable")
        self.parent = parent
    
    def body(self, master):
        self.name_label = tk.Label(master, text="Variable Name")
        self.name_label.grid(row=0, column=0)
        self.name_entry = tk.Entry(master)
        self.name_entry.grid(row=0, column=1)

        self.lb_label = tk.Label(master, text="Lower Bound")
        self.lb_label.grid(row=1, column=0)
        self.lb_entry = tk.Entry(master)
        self.lb_entry.grid(row=1, column=1)
        self.lb_none_var = tk.BooleanVar()
        self.lb_none_check = tk.Checkbutton(master, text="None", variable=self.lb_none_var, command=self.toggle_lb_entry)
        self.lb_none_check.grid(row=1, column=2)

        self.ub_label = tk.Label(master, text="Upper Bound")
        self.ub_label.grid(row=2, column=0)
        self.ub_entry = tk.Entry(master)
        self.ub_entry.grid(row=2, column=1)
        self.ub_none_var = tk.BooleanVar()
        self.ub_none_check = tk.Checkbutton(master, text="None", variable=self.ub_none_var, command=self.toggle_ub_entry)
        self.ub_none_check.grid(row=2, column=2)

        self.profit_label = tk.Label(master, text="Profit per Cake")
        self.profit_label.grid(row=3, column=0)
        self.profit_entry = tk.Entry(master)
        self.profit_entry.grid(row=3, column=1)

        self.int_label = tk.Label(master, text="Is Integer?")
        self.int_label.grid(row=4, column=0)
        self.int_var = tk.BooleanVar(value=True)
        self.int_check = tk.Checkbutton(master, variable=self.int_var)
        self.int_check.grid(row=4, column=1)

        self.multiplier_label = tk.Label(master, text="Multiplier")
        self.multiplier_label.grid(row=5, column=0)
        self.multiplier_entry = tk.Entry(master)
        self.multiplier_entry.grid(row=5, column=1)
    
    # Disable/enable lower bound entry
    def toggle_lb_entry(self):
        if self.lb_none_var.get():
            self.lb_entry.config(state='disabled')
        else:
            self.lb_entry.config(state='normal')

    # Disable/enable upper bound entry
    def toggle_ub_entry(self):
        if self.ub_none_var.get():
            self.ub_entry.config(state='disabled')
        else:
            self.ub_entry.config(state='normal')
    
    # Function that is called when "OK" button is pressed
    def apply(self):
        name = self.name_entry.get()
        lower_bound = None if self.lb_none_var.get() else int(self.lb_entry.get())
        upper_bound = None if self.ub_none_var.get() else int(self.ub_entry.get())
        profit = float(self.profit_entry.get())
        integer = self.int_var.get()
        multiplier = int(self.multiplier_entry.get())
        
        # Create the variable and add to list
        create_integer_variable(name, lower_bound, upper_bound, profit, integer, multiplier)
        
        # Update the table in the main window
        self.parent.update_table()

# Run the application
if __name__ == "__main__":
    app = App()
    app.mainloop()
