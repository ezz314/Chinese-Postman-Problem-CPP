import itertools
import copy
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

# Load edge list data
edgelist = pd.read_csv('_edgelist.csv')

# Load node list data
nodelist = pd.read_csv('_nodelist.csv')


# Create empty graph
g = nx.Graph()

# Add edges and edge attributes
for _, elrow in edgelist.iterrows():
    # Extract node1, node2, and edge attributes
    node1 = elrow.iloc[0]
    node2 = elrow.iloc[1]
    attrs = elrow.iloc[2:].to_dict()
    # Add edge to the graph
    g.add_edge(node1, node2, **attrs)

# Add node attributes
for _, nlrow in nodelist.iterrows():
    # Extract node id and node attributes
    node_id = nlrow.iloc[0]
    attrs = nlrow.iloc[1:].to_dict()
    # Set node attributes
    nx.set_node_attributes(g, {node_id: attrs})

# Define node positions data structure (dict) for plotting
node_positions = {node[0]: (node[1]['X'], -node[1]['Y']) for node in g.nodes(data=True)}

# Define data structure (list) of edge colors for plotting
edge_colors = [e[2]['color'] for e in list(g.edges(data=True))]

# Define edge labels (distance)
edge_labels = {(e[0], e[1]): e[2]['distance'] for e in list(g.edges(data=True))}

def plot_MainG():
    plt.figure(figsize=(12, 8))  # Increase figure size for better readability
    nx.draw(g, pos=node_positions, edge_color=edge_colors, node_size=10, node_color='black')
    bbox = {'ec': [1, 1, 1, 0], 'fc': [1, 1, 1, 0]}  # hack to label edges over line (rather than breaking up line)
    # Add node labels
    nx.draw_networkx_labels(g, pos=node_positions, labels={node: node for node in g.nodes()}, font_size=8, font_color='black')
    '''
    # Add edge weight (distance) manually
    for (n1, n2), label in edge_labels.items():
        x1, y1 = node_positions[n1]
        x2, y2 = node_positions[n2]
        x = (x1 + x2) / 2
        y = (y1 + y2) / 2
        plt.text(x, y - 0.05, s=f"{label:.2f}", color='green', horizontalalignment='center', bbox=bbox, fontsize=6, fontstyle='italic')
    '''
    # Add title with adjusted position
    plt.title('Graph Map',  fontdict={'fontsize': 14, 'fontweight': 'bold', 'color': 'black'}, loc='left', pad=20)  # Adjust the 'pad' parameter for distance of the title from the plot
    plt.show()
#plot_MainG()