from Solution_Visu import *
import pandas as pd

def save_stats_to_file(file_path):
    with open(file_path, 'w') as file:

        # Computing some stats
        total_mileage_of_circuit = sum([edge[2]['distance'] for edge in euler_circuit])
        total_mileage_on_orig_trail_map = sum(nx.get_edge_attributes(g, 'distance').values())
        total_retraced_mileage = total_mileage_of_circuit - total_mileage_on_orig_trail_map
        percent_mileage_retraced = (total_retraced_mileage / total_mileage_on_orig_trail_map) * 100

        # Count the number of nodes and edges
        num_nodes_original = len(g.nodes())
        num_edges_original = len(g.edges())
        num_edges_circuit = len(euler_circuit)

        # Count the number of edges traversed more than once
        num_edges_traversed_more_than_once = num_edges_circuit - num_edges_original

        # Writing stats to file
        file.write('Mileage of circuit: {0:.2f}\n'.format(total_mileage_of_circuit))
        file.write('Mileage on original trail map: {0:.2f}\n'.format(total_mileage_on_orig_trail_map))
        file.write('Mileage retracing edges: {0:.2f}\n'.format(total_retraced_mileage))
        file.write('Percent of mileage retraced: {0:.2f}%\n\n'.format(percent_mileage_retraced))

        file.write('Number of edges in circuit: {}\n'.format(num_edges_circuit))
        file.write('Number of edges in original graph: {}\n'.format(num_edges_original))
        file.write('Number of nodes in original graph: {}\n\n'.format(num_nodes_original))

        file.write('Number of edges traversed more than once: {}\n\n'.format(num_edges_traversed_more_than_once))

        # Compute the number of times each node is visited
        _vcn = pd.Series([(e[0]) for e in euler_circuit]).value_counts(sort=False)
        node_visits = pd.DataFrame({'Node': _vcn.index, 'Number of Visits': _vcn.values})
        file.write('Number of times visiting each node:\n')
        file.write(node_visits.to_string(index=False) + '\n\n')

        # Compute the number of times each edge is visited
        _vce = pd.Series([sorted(e)[0] + sorted(e)[1] for e in nx.MultiDiGraph(euler_circuit).edges()]).value_counts()
        edge_visits = pd.DataFrame({'Edge': _vce.index, 'Number of Visits': _vce.values})
        file.write('Number of times visiting each edge:\n')
        file.write(edge_visits.to_string(index=False) + '\n')

    print("Stats saved to", file_path)


