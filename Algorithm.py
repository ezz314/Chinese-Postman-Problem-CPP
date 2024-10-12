from Graph import *

#CPP Step 1: Find Nodes of Odd Degree

# Calculate list of nodes with odd degree
nodes_odd_degree = [v for v, d in g.degree() if d % 2 == 1]
'''
# Preview
#print(nodes_odd_degree[0:5])
#print('Number of nodes of odd degree: {}'.format(len(nodes_odd_degree)))
#print('Number of total nodes: {}'.format(len(g.nodes())))
'''

#CPP Step 2: Find Min Distance Pairs
#Step 2.1: Compute Node Pairs

# Compute all pairs of odd nodes. in a list of tuples
odd_node_pairs = list(itertools.combinations(nodes_odd_degree, 2))
'''
Preview pairs of odd degree nodes
print(odd_node_pairs[0:10])
# Counts
print('Number of pairs: {}'.format(len(odd_node_pairs)))
'''

#Step 2.2: Compute Shortest Paths between Node Pairs
def get_shortest_paths_distances(graph, pairs, edge_weight_name):
    """Compute shortest distance between each pair of nodes in a graph.  Return a dictionary keyed on node pairs (tuples)."""
    distances = {}
    for pair in pairs:
        distances[pair] = nx.dijkstra_path_length(graph, pair[0], pair[1], weight=edge_weight_name)
    return distances

# Compute shortest paths.  Return a dictionary with node pairs keys and a single value equal to shortest path distance.
odd_node_pairs_shortest_paths = get_shortest_paths_distances(g, odd_node_pairs, 'distance')

#Step 2.3: Create Complete Graph
def create_complete_graph(pair_weights, flip_weights=True):
    """
    Create a completely connected graph using a list of vertex pairs and the shortest path distances between them
    Parameters:
        pair_weights: list[tuple] from the output of get_shortest_paths_distances
        flip_weights: Boolean. Should we negate the edge attribute in pair_weights?
    """
    g = nx.Graph()
    for k, v in pair_weights.items():
        wt_i = - v if flip_weights else v
        g.add_edge(k[0], k[1], **{'distance': v, 'weight': wt_i})
    return g
# Generate the complete graph
g_odd_complete = create_complete_graph(odd_node_pairs_shortest_paths, flip_weights=True)

def plot_odd_G():
    # Plot the complete graph of odd-degree nodes
    plt.figure(figsize=(8, 6))
    pos_random = nx.random_layout(g_odd_complete)
    nx.draw_networkx_nodes(g_odd_complete, node_positions, node_size=20, node_color="red")
    nx.draw_networkx_edges(g_odd_complete, node_positions, alpha=0.1)
    plt.axis('off')
    plt.title('Complete Graph of Odd-degree Nodes')
    plt.show()
#plot_odd_G()

#Step 2.4: Compute Minimum Weight Matching

# Compute min weight matching.
# Note: max_weight_matching uses the 'weight' attribute by default as the attribute to maximize.
odd_matching_dupes = nx.algorithms.max_weight_matching(g_odd_complete, True)

'''
#print('Number of edges in matching: {}'.format(len(odd_matching_dupes)))
#for edge in odd_matching_dupes:
#    print(edge)
'''

# Convert matching set to list of deduped tuples
odd_matching = list({tuple(sorted(pair)) for pair in odd_matching_dupes})
# Create a new graph to overlay on g_odd_complete with just the edges from the min weight matching
g_odd_complete_min_edges = nx.Graph(odd_matching)

#computing min weights
def plot_min_weight_K():
    plt.figure(figsize=(8, 6))
    # Plot the complete graph of odd-degree nodes
    nx.draw(g_odd_complete, pos=node_positions, node_size=20, alpha=0.05)
    g_odd_complete_min_edges = nx.Graph(odd_matching)
    nx.draw(g_odd_complete_min_edges, pos=node_positions, node_size=20, edge_color='blue', node_color='red')
    plt.title('Min Weight Matching on Complete Graph')
    plt.show()
#plot_min_weight_K()

#Min weight matching on orginal graph
def plot_min_weight():
    plt.figure(figsize=(8, 6))
    # Plot the original trail map graph
    nx.draw(g, pos=node_positions, node_size=20, alpha=0.1, node_color='black')
    # Plot graph to overlay with just the edges from the min weight matching
    nx.draw(g_odd_complete_min_edges, pos=node_positions, node_size=20, alpha=1, node_color='red', edge_color='blue')
    plt.title('Min Weight Matching on Orginal Graph')
    plt.show()
#plot_min_weight()

#Step 2.5: Augment the Original Graph

#adding min weights on the orginal
def add_augmenting_path_to_graph(graph, min_weight_pairs):
    """
    Add the min weight matching edges to the original graph
    Parameters:
        graph: NetworkX graph (original graph from trailmap)
        min_weight_pairs: list[tuples] of node pairs from min weight matching
    Returns:
        augmented NetworkX graph
    """

    # We need to make the augmented graph a MultiGraph so we can add parallel edges
    graph_aug = nx.MultiGraph(graph.copy())
    for pair in min_weight_pairs:
        graph_aug.add_edge(pair[0],
                           pair[1],
                           **{'distance': nx.dijkstra_path_length(graph, pair[0], pair[1]), 'trail': 'augmented'}
                           # attr_dict={'distance': nx.dijkstra_path_length(graph, pair[0], pair[1]),
                           #            'trail': 'augmented'}  # deprecated after 1.11
                           )
    return graph_aug
# Create augmented graph: add the min weight matching edges to g
g_aug = add_augmenting_path_to_graph(g, odd_matching)


#CPP Step 3: Compute Eulerian Circuit
def create_eulerian_circuit(graph_augmented, graph_original, starting_node=None):
    """Create the eulerian path using only edges from the original graph."""
    euler_circuit = []
    naive_circuit = list(nx.eulerian_circuit(graph_augmented, source=starting_node))

    for edge in naive_circuit:
        edge_data = graph_augmented.get_edge_data(edge[0], edge[1])

        if edge_data[0]['trail'] != 'augmented':
            # If `edge` exists in original graph, grab the edge attributes and add to eulerian circuit.
            edge_att = graph_original[edge[0]][edge[1]]
            euler_circuit.append((edge[0], edge[1], edge_att))
        else:
            aug_path = nx.shortest_path(graph_original, edge[0], edge[1], weight='distance')
            aug_path_pairs = list(zip(aug_path[:-1], aug_path[1:]))

            #print('Filling in edges for augmented edge: {}'.format(edge))
            #print('Augmenting path: {}'.format(' => '.join(aug_path)))
            #print('Augmenting path pairs: {}\n'.format(aug_path_pairs))

            # If `edge` does not exist in original graph, find the shortest path between its nodes and
            #  add the edge attributes for each link in the shortest path.
            for edge_aug in aug_path_pairs:
                edge_aug_att = graph_original[edge_aug[0]][edge_aug[1]]
                euler_circuit.append((edge_aug[0], edge_aug[1], edge_aug_att))

    return euler_circuit

euler_circuit = create_eulerian_circuit(g_aug, g)
