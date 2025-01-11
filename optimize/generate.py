from collections import deque
from LP_Interface import addVariablesToModel, LP_optimizeCall
addVariablesToModel()

"""

"""
# Investment handler function
def investmentHandler(current_productivity, current_savings, percentage):
    percentage = percentage / 100

    newSavings = current_savings
    newSavings -= current_savings * percentage
    #print("after usage for investment",newSavings)
    newSavings += current_productivity #this assumes productivity is net, not gross 
    #print("after productivity",newSavings)
    investmentAllocation = current_savings*percentage

    #replace 0.2 with function call to optimizer, with 'investmentAllocation' as parameter for budget constraint
    investmentReturn = LP_optimizeCall(Budget=investmentAllocation)

    newProductivity = current_productivity
    newProductivity += investmentReturn #only 20 percent of investment amount is added to productivity
    #print(newProductivity, newSavings)
    return (newProductivity, newSavings)

class Node:
    def __init__(self, parent, nodeName, month = 0, productivity = 0,savings = 0, percentage = None):
        self.parent = parent
        self.nodeName = nodeName

        self.month = month
        self.productivity = productivity
        self.savings = savings
        self.generationPercentage = percentage

        self.children = []  # List to hold child nodes

    def create_child(self, nodeName, percentage = 0):
        #print("create_child method called from object",self,"with parameters:",nodeName,percentage)
        newProductivity, newSavings = investmentHandler(self.productivity, self.savings, percentage)
        #childname = f"{(self.nodeName) + str(percentage)} -> "
        child = Node(self, nodeName, self.month + 1, newProductivity, newSavings,percentage)
        self.children.append(child)  # Add a child node
        return child

    def __repr__(self):
        parent_data = self.parent.nodeName if self.parent else None
        return f"Node({self.nodeName!r}) Parent:{parent_data!r}"
        #uncomment below to show parental linage to root:
        #return f"Node({self.data!r}) who's parent is:{self.parent!r}"

class Tree:
    def __init__(self, root):
        self.root = root  # Root node of the tree

    def display_bfs(self):
        queue = deque([self.root])  # Start with the root node in the queue
        while queue:
            node = queue.popleft()  # Dequeue the front node
            print(node.nodeName, "Month:",node.month, "Productivity:", node.productivity, "Savings:", node.savings)  # Display the current node
            queue.extend(node.children)  # Enqueue all the children

def create_tree_bfs(root_name = "Root", levels = 1, step = 50):
    root = Node(None,root_name,0,10,10)
    if levels == 0:
        return root

    queue = [(root, 0)]  # Queue stores nodes and their current level

    while queue:
        current_node, current_level = queue.pop(0)

        if current_level < levels:  # Add children if within level limit
            for i in range(0,101,step):
                
                childname = f"{current_node.nodeName}-{i}"
                #childname = f"level:{current_level + 1} after {i}% investment from productivity:{current_node.productivity} and savings:{current_node.savings}\t"
                child = current_node.create_child(childname,i)
                queue.append((child, current_level + 1))

    return root

from collections import deque

def find_highest_nodes(root):
    """
    Traverse the tree and find nodes with highest savings, productivity, and total sum.
    Returns dictionaries containing the highest values and their corresponding nodes.
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
tree_root = create_tree_bfs("R", num_levels,step)

# Display the tree

# tree = Tree(tree_root)
# tree.display_bfs()

# Display Highest

display_highest_nodes(tree_root)