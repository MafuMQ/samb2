"""
generate.py

Simulates investment and productivity growth using a tree structure and linear programming optimization.

- Uses a tree of Node objects to represent different investment strategies over time.
- Each node represents a state (month, productivity, savings, investment %).
- At each step, a percentage of savings is invested, and the return is calculated using an LP optimizer.
- The tree is built using breadth-first search (BFS) to explore all possible investment strategies.
- Functions are provided to find and display nodes with the highest savings, productivity, and total value.

Dependencies:
- LP_Interface.py (for LP optimization logic)
- LP_PULP.py (backend for optimization)

@author: Mafu
@date: 2025-06-14
"""

from collections import deque
from LP_Interface import addVariablesToModel, LP_optimizeCall
addVariablesToModel()

"""
This script builds a tree of investment decisions and uses LP optimization to simulate returns.
"""

# Investment handler function
def investmentHandler(current_productivity, current_savings, percentage):
    """
    Handles investment allocation and productivity update for a given node.

    Args:
        current_productivity (float): Current productivity value.
        current_savings (float): Current savings value.
        percentage (float): Percentage of savings to invest (0-100).
    Returns:
        tuple: (newProductivity, newSavings) after investment and productivity update.
    """
    percentage = percentage / 100

    newSavings = current_savings
    newSavings -= current_savings * percentage
    newSavings += current_productivity  # assumes productivity is net, not gross
    investmentAllocation = current_savings * percentage

    # Use LP optimizer to determine investment return
    investmentReturn = LP_optimizeCall(Budget=investmentAllocation)

    newProductivity = current_productivity
    newProductivity += investmentReturn
    return (newProductivity, newSavings)

class Node:
    """
    Represents a node in the investment tree.

    Attributes:
        parent (Node): Parent node.
        nodeName (str): Name/label of the node.
        month (int): Time step (month).
        productivity (float): Productivity value at this node.
        savings (float): Savings value at this node.
        generationPercentage (float): Investment percentage used to reach this node.
        children (list): List of child Node objects.
    """
    def __init__(self, parent, nodeName, month = 0, productivity: float = 0.0, savings: float = 0.0, percentage = None):
        self.parent = parent
        self.nodeName = nodeName

        self.month = month
        self.productivity = productivity
        self.savings = savings
        self.generationPercentage = percentage

        self.children = []  # List to hold child nodes

    def create_child(self, nodeName, percentage = 0):
        """
        Create a child node with updated productivity and savings after investment.

        Args:
            nodeName (str): Name/label for the child node.
            percentage (float): Investment percentage for this child.
        Returns:
            Node: The created child node.
        """
        newProductivity, newSavings = investmentHandler(self.productivity, self.savings, percentage)
        child = Node(self, nodeName, self.month + 1, newProductivity, newSavings, percentage)
        self.children.append(child)  # Add a child node
        return child

    def __repr__(self):
        parent_data = self.parent.nodeName if self.parent else None
        return f"Node({self.nodeName!r}) Parent:{parent_data!r}"
        # Uncomment below to show full parental lineage:
        # return f"Node({self.data!r}) who's parent is:{self.parent!r}"

class Tree:
    """
    Represents the investment tree structure.

    Attributes:
        root (Node): The root node of the tree.
    """
    def __init__(self, root):
        self.root = root  # Root node of the tree

    def display_bfs(self):
        """
        Display the tree using breadth-first search (BFS).
        """
        queue = deque([self.root])  # Start with the root node in the queue
        while queue:
            node = queue.popleft()  # Dequeue the front node
            print(node.nodeName, "Month:", node.month, "Productivity:", node.productivity, "Savings:", node.savings)  # Display the current node
            queue.extend(node.children)  # Enqueue all the children

def create_tree_bfs(root_name = "Root", levels = 1, step = 50):
    """
    Build a tree of investment decisions using BFS.

    Args:
        root_name (str): Name for the root node.
        levels (int): Number of levels (months) to simulate.
        step (int): Step size for investment percentage (0-100).
    Returns:
        Node: The root node of the created tree.
    """
    root = Node(None, root_name, 0, 10, 10)
    if levels == 0:
        return root

    queue = [(root, 0)]  # Queue stores nodes and their current level

    while queue:
        current_node, current_level = queue.pop(0)

        if current_level < levels:  # Add children if within level limit
            for i in range(0, 101, step):
                childname = f"{current_node.nodeName}-{i}"
                child = current_node.create_child(childname, i)
                queue.append((child, current_level + 1))

    return root

from collections import deque

def find_highest_nodes(root):
    """
    Traverse the tree and find nodes with highest savings, productivity, and total sum.

    Args:
        root (Node): The root node of the tree.
    Returns:
        tuple: Dictionaries for highest savings, productivity, and total sum nodes.
    """
    highest_savings = {"value": float('-inf'), "node": None}
    highest_productivity = {"value": float('-inf'), "node": None}
    highest_sum = {"value": float('-inf'), "node": None}
    
    queue = deque([root])
    
    while queue:
        node = queue.popleft()
        # Check for highest savings
        if node.savings > highest_savings["value"]:
            highest_savings["value"] = node.savings
            highest_savings["node"] = node
        # Check for highest productivity
        if node.productivity > highest_productivity["value"]:
            highest_productivity["value"] = node.productivity
            highest_productivity["node"] = node
        # Calculate and check for highest sum
        current_sum = node.productivity + node.savings
        if current_sum > highest_sum["value"]:
            highest_sum["value"] = current_sum
            highest_sum["node"] = node
        queue.extend(node.children)
    
    return highest_savings, highest_productivity, highest_sum

def display_highest_nodes(root):
    """
    Display information about nodes with highest values in a formatted way.

    Args:
        root (Node): The root node of the tree.
    """
    highest_savings, highest_productivity, highest_sum = find_highest_nodes(root)
    print("\n=== Nodes with Highest Values ===")
    print("\nHighest Savings:")
    print(f"Node: {highest_savings['node'].nodeName}")
    print(f"Month: {highest_savings['node'].month}")
    print(f"Savings: {highest_savings['value']:.2f}")
    print(f"Productivity: {highest_savings['node'].productivity:.2f}")
    print(f"Investment %: {highest_savings['node'].generationPercentage}%")
    print("\nHighest Productivity:")
    print(f"Node: {highest_productivity['node'].nodeName}")
    print(f"Month: {highest_productivity['node'].month}")
    print(f"Savings: {highest_productivity['node'].savings:.2f}")
    print(f"Productivity: {highest_productivity['value']:.2f}")
    print(f"Investment %: {highest_productivity['node'].generationPercentage}%")
    print("\nHighest Total (Savings + Productivity):")
    print(f"Node: {highest_sum['node'].nodeName}")
    print(f"Month: {highest_sum['node'].month}")
    print(f"Savings: {highest_sum['node'].savings:.2f}")
    print(f"Productivity: {highest_sum['node'].productivity:.2f}")
    print(f"Total Sum: {highest_sum['value']:.2f}")
    print(f"Investment %: {highest_sum['node'].generationPercentage}%")

# Create the tree using BFS
num_levels = 5
step = 100
tree_root = create_tree_bfs("R", num_levels, step)

# Display the tree
# tree = Tree(tree_root)
# tree.display_bfs()

# Display Highest

display_highest_nodes(tree_root)