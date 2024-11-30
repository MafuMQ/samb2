import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

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
    investmentReturn = 0.2

    newProductivity = current_productivity
    newProductivity += investmentAllocation*investmentReturn #only 20 percent of investment amount is added to productivity
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


def add_edges_from_tree(graph, node, edge_labels):
    """Recursively traverse the tree and add edges to the graph."""
    for child in node.children:
        graph.add_edge(node.nodeName, child.nodeName)  # Add edge
        edge_label = f"{child.generationPercentage}"
        edge_labels[(node.nodeName, child.nodeName)] = edge_label  # Example edge label
        add_edges_from_tree(graph, child, edge_labels)


def get_node_labels_from_tree(node):
    """Recursively collect labels for nodes in the tree."""
    labels = {node.nodeName: f"{node.nodeName}\nProductivity: {node.productivity:.2f}\nSavings: {node.savings:.2f}"}
    for child in node.children:
        labels.update(get_node_labels_from_tree(child))
    return labels

# Create the tree using BFS
num_levels = 3
step = 100
tree_root = create_tree_bfs("Root", num_levels,step)

# Display the tree
tree = Tree(tree_root)
tree.display_bfs()

# Create a directed graph
G = nx.DiGraph()
edge_labels = {}

# Add edges from the tree
add_edges_from_tree(G, tree_root, edge_labels)

# Get labels with attributes
labels = get_node_labels_from_tree(tree_root)

# Plot the tree
pos = nx.nx_agraph.graphviz_layout(G, prog="dot")  # Hierarchical layout
nx.draw(G, pos, with_labels=True, labels=labels, arrows=True, 
        node_size=2000, node_color="lightblue", font_size=8, font_weight="bold")

# Draw edge labels
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, font_color="red")

plt.show()