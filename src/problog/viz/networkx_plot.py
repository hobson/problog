import networkx as nx
import matplotlib.pyplot as plt

# Create a directed graph
G = nx.DiGraph()

# Define the edge list
edge_list = [["President", "Joe"], ["President", "Joseph"], ["President", "Donald"], ["President", "Barack"],
             ["Barack", "Obama"], ["Joe", "Biden"], ["Joseph", "Biden"], ["Joseph", "Robinnette"]]

# Add edges to the graph
G.add_edges_from(edge_list)

# Draw the graph
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=2000, node_color='skyblue', font_size=10, font_weight='bold', edge_color='gray', arrowsize=20)

# Display the graph
plt.show()
