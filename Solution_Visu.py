from Algorithm import *
import os
import copy
import glob
import imageio.v2 as imageio  # Importing imageio.v2 explicitly to avoid DeprecationWarning
import numpy as np  # Add this import statement for NumPy

# Define the directory paths
png_directory = 'fig/png/'
gif_directory = 'fig/gif/'

# Create the directories if they don't exist
os.makedirs(png_directory, exist_ok=True)
os.makedirs(gif_directory, exist_ok=True)

def create_cpp_edgelist(euler_circuit):
    """
    Create the edgelist without parallel edge for the visualization
    Combine duplicate edges and keep track of their sequence and # of walks
    Parameters:
        euler_circuit: list[tuple] from create_eulerian_circuit
    """
    cpp_edgelist = {}

    for i, e in enumerate(euler_circuit):
        edge = frozenset([e[0], e[1]])

        if edge in cpp_edgelist:
            cpp_edgelist[edge][2]['sequence'] += ', ' + str(i)
            cpp_edgelist[edge][2]['visits'] += 1

        else:
            cpp_edgelist[edge] = e
            cpp_edgelist[edge][2]['sequence'] = str(i)
            cpp_edgelist[edge][2]['visits'] = 1

    return list(cpp_edgelist.values())
cpp_edgelist = create_cpp_edgelist(euler_circuit)

# Create CPP solution graph
g_cpp = nx.Graph(cpp_edgelist)

#Visualization 1: Retracing Steps
def Retracing_Gcpp():
    plt.figure(figsize=(10, 8))

    visit_colors = {1: 'lightgray', 2: 'blue'}
    edge_colors = [visit_colors[e[2]['visits']] for e in g_cpp.edges(data=True)]
    node_colors = ['red' if node in nodes_odd_degree else 'black' for node in g_cpp.nodes()]

    nx.draw_networkx(g_cpp, pos=node_positions, node_size=20, node_color=node_colors, edge_color=edge_colors,
                     with_labels=False)
    plt.axis('off')
    plt.show()
#Retracing_Gcpp()
#Visualization 2: CPP Solution Sequence

def Sequence_Gcpp():
    plt.figure(figsize=(12, 8))
    bbox = {'ec': [1, 1, 1, 0], 'fc': [1, 1, 1, 0]}
    edge_colors = [e[2]['color'] for e in g_cpp.edges(data=True)]
    nx.draw_networkx(g_cpp, pos=node_positions, node_size=10, node_color='black', edge_color=edge_colors,
                     with_labels=False, alpha=0.5)

    # shortest distance labels
    '''for (u, v, d) in g_cpp.edges(data=True):
        if 'distance' in d:
            x1, y1 = node_positions[u]
            x2, y2 = node_positions[v]
            x = (x1 + x2) / 2
            y = (y1 + y2) / 2
            plt.text(x, y - 0.05, s=f"{d['distance']:.2f}", color='black', horizontalalignment='center', fontsize=6, bbox= bbox ,fontstyle='italic')
    '''
    plt.title('CPP Graph Map')
    plt.axis('off')
    plt.show()
#Sequence_Gcpp()

#Visualization 3: Movie
def Generating_Frames():
    visit_colors = {1: 'black', 2: 'red'}
    edge_cnter = {}
    total_distance = 0  # Initialize total distance covered
    for i, e in enumerate(euler_circuit, start=1):

        edge = frozenset([e[0], e[1]])
        if edge in edge_cnter:
            edge_cnter[edge] += 1
        else:
            edge_cnter[edge] = 1

        # Full graph (faded in background)
        plt.figure(figsize=(12, 8))
        nx.draw_networkx(g_cpp, pos=node_positions, node_size=6, node_color='gray', with_labels=False, alpha=0.07)

        # Edges walked as of iteration i
        euler_circuit_i = copy.deepcopy(euler_circuit[0:i])
        for j in range(len(euler_circuit_i)):
            edge_j = frozenset([euler_circuit_i[j][0], euler_circuit_i[j][1]])
            euler_circuit_i[j][2]['visits_i'] = edge_cnter[edge_j]
            # Update total distance covered
            total_distance += euler_circuit_i[j][2]['distance']
        g_i = nx.Graph(euler_circuit_i)
        g_i_edge_colors = [visit_colors[e[2]['visits_i']] for e in g_i.edges(data=True)]

        nx.draw_networkx_nodes(g_i, pos=node_positions, node_size=6, alpha=0.6, node_color='lightgray', label=False,
                               linewidths=0.1)
        nx.draw_networkx_edges(g_i, pos=node_positions, edge_color=g_i_edge_colors, alpha=0.8)

        # Add labels for shortest distances
        '''for (u, v, d) in g_i.edges(data=True):
            if 'distance' in d:
                x1, y1 = node_positions[u]
                x2, y2 = node_positions[v]
                x = (x1 + x2) / 2
                y = (y1 + y2) / 2
                plt.text(x, y - 0.05, s=f"{d['distance']:.2f}", color='blue', horizontalalignment='center', fontsize=6)
            '''
        # Display total distance label in the corner
        #plt.text(0.05, 0.05, f'Total Distance: {total_distance:.2f}', transform=plt.gca().transAxes, color='black',fontstyle='oblique')

        plt.axis('off')
        plt.savefig('fig/png/img{}.png'.format(i), dpi=120, bbox_inches='tight')
        plt.close()
#Generating_Frames()
def Animating_Gcpp(image_path, movie_filename, fps=5):
    # sorting filenames in order
    filenames = glob.glob(image_path + 'img*.png')
    filenames_sort_indices = np.argsort([int(os.path.basename(filename).split('.')[0][3:]) for filename in filenames])
    filenames = [filenames[i] for i in filenames_sort_indices]

    # make movie
    with imageio.get_writer(movie_filename, mode='I', fps=fps) as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)

#Animating_Gcpp(png_directory, gif_directory + 'cpp_route_animation.gif', fps=3)
