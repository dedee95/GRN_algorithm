import sys
import pandas as pd
import networkx as nx
from pyvis.network import Network
import gravis as gv
import matplotlib.pyplot as plt
import argparse

def main(network_file, output_html):
    # Load data
    df = pd.read_csv(network_file, sep='\t', names=['TF', 'TG', 'weight'])

    # Create graph
    G = nx.from_pandas_edgelist(df, 'TF', 'TG', edge_attr='weight')

    # Starting node
    starting_node = df.iloc[0, 0]  # Ambil node pertama dari kolom 'TF'
    bfs_tree_edges = nx.bfs_edges(G, source=starting_node)

    # Create BFS tree graph
    bfs_tree = nx.Graph()
    for u, v in bfs_tree_edges:
        bfs_tree.add_edge(u, v, weight=G[u][v]['weight'])

    # Group nodes by BFS level
    node_groups = {}
    for node, level in nx.shortest_path_length(bfs_tree, source=starting_node).items():
        if level not in node_groups:
            node_groups[level] = []
        node_groups[level].append(node)

    # Create result DataFrame
    result_mat = {'TF': [], 'TG': [], 'weight': [], 'Levels in GCN': []}
    for u, v, data in bfs_tree.edges(data=True):
        result_mat['TF'].append(u)
        result_mat['TG'].append(v)
        result_mat['weight'].append(data['weight'])
        result_mat['Levels in GCN'].append(nx.shortest_path_length(bfs_tree, source=starting_node)[v])

    result_table = pd.DataFrame(result_mat)

    # Save result to TSV
    output_tsv_file = output_html.replace('.html', '_bfs_levels.tsv')
    result_table.to_csv(output_tsv_file, sep='\t', index=False)

    # Calculate layout for visualization
    pos = nx.drawing.layout.shell_layout(bfs_tree, nlist=list(node_groups.values()), scale=600)

    # Assign colors to nodes based on BFS levels
    for nodes, clr in zip(node_groups.values(), plt.get_cmap('RdBu', len(node_groups))([i for i in range(len(node_groups))])):
        r, g, b, a = clr
        color = f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"
        for node in nodes:
            bfs_tree.nodes[node]['color'] = color

    # Set node sizes based on degrees
    degree_dict = dict(bfs_tree.degree())
    nx.set_node_attributes(bfs_tree, degree_dict, 'size')

    # Add coordinates as node annotations recognized by gravis
    for name, (x, y) in pos.items():
        node = bfs_tree.nodes[name]
        node['x'] = x
        node['y'] = y

    # Visualize graph using gravis
    fig = gv.d3(bfs_tree, 
                use_node_size_normalization=True, 
                node_size_normalization_max=30, 
                use_edge_size_normalization=True, 
                edge_size_data_source='weight', 
                edge_curvature=0.3, 
                layout_algorithm_active=False)

    # Export visualization as an HTML file
    fig.export_html(output_html)
    print(f"Visualization saved to {output_html}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize network data and export to HTML")
    parser.add_argument("network_file", help="Path to the network file (TSV format)")
    parser.add_argument("output_html", help="Name of the output HTML file")
    args = parser.parse_args()
    main(args.network_file, args.output_html)