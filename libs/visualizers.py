import networkx as nx
import matplotlib.pyplot as plt

def visualize_graph(G: nx.Graph, title: str="Graph Visualization", dims: tuple = (20, 20)):
    plt.figure(figsize=dims)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', 
            node_size=500, font_size=10, font_weight='bold')
    plt.title(title)
    plt.show()

def visualize_graph_customized(G: nx.Graph, title: str="Graph Visualization", 
                   color: bool = True, 
                   node_size: int = 1000,
                   font_size: int = 12,
                   layout: str = 'spring',
                   dims: tuple = (5, 5),
                   save: bool = False ):
   
    plt.figure(figsize=dims)
    
    layout_funcs: dict = {
        'spring': nx.spring_layout,
        'circular': nx.circular_layout,
        'random': nx.random_layout,
        'shell': nx.shell_layout
    }
    
    layout_func = layout_funcs.get(layout, nx.spring_layout)
    pos = layout_func(G)
    colors = None

    if color:
        colors = []
        cliques = list(nx.find_cliques(G))
        cliques.sort(key=len, reverse=True)
    
        for node in G.nodes():
            for i, clique in enumerate(cliques):
                if node in clique:
                    colors.append(i)
                    break
    else:
        colors = "lightblue"

    nx.draw(G, pos,
            with_labels=True,
            node_color=colors,
            node_size=node_size,
            font_size=font_size,
            font_weight='bold',
            edge_color='gray',
            width=2,
            alpha=0.8)
    
    plt.title(title, fontsize=16, pad=20)

    if save:
        plt.savefig(f'graph_pictures/{title}', transparent=True)
    plt.show()

def visualize_graph_customized_metrics(G: nx.Graph, title: str="Graph Visualization", 
                   color: bool = True, 
                   node_size: int = 1000,
                   font_size: int = 12,
                   layout: str = 'spring',
                   dims: tuple = (5, 5),
                   save: bool = False):
    """
    Visualize a graph with legacy metrics that scale based on plot dimensions.
    
    Args:
        G (nx.Graph): NetworkX graph object to visualize
        title (str): Title of the visualization
        color (bool): Whether to color nodes based on clique membership
        node_size (int): Size of nodes in the visualization
        font_size (int): Size of node labels
        layout (str): Layout algorithm to use ('spring', 'circular', 'random', 'shell')
        dims (tuple): Figure dimensions as (width, height)
        save (bool): Whether to save the visualization to a file
    """
    # Create figure and calculate the scaled font size based on dimensions
    fig = plt.figure(figsize=dims)
    
    # Calculate a scaled font size based on the plot dimensions
    # We use the geometric mean of width and height to account for both dimensions
    # The multiplier (0.8) can be adjusted to change the relative size
    base_scale = (dims[0] * dims[1]) ** 0.5  # geometric mean of width and height
    scaled_font_size = base_scale * 1.5
    
    scaled_pad = None
    # Calculate scaled padding based on dimensions
    if dims[0] >= 20 or dims[1] >= 20:
        scaled_pad = base_scale * 0.04
    elif dims[0] >= 10 or dims[1] >= 10:
        scaled_pad = base_scale * 0.12
    else:
        scaled_pad = base_scale * 0.2  # 10% of the base scale
    
    layout_funcs: dict = {
        'spring': nx.spring_layout,
        'circular': nx.circular_layout,
        'random': nx.random_layout,
        'shell': nx.shell_layout
    }
    
    layout_func = layout_funcs.get(layout, nx.spring_layout)
    pos = layout_func(G)
    
    # Handle node coloring
    colors = None
    if color:
        colors = []
        cliques = list(nx.find_cliques(G))
        cliques.sort(key=len, reverse=True)
    
        for node in G.nodes():
            for i, clique in enumerate(cliques):
                if node in clique:
                    colors.append(i)
                    break
    else:
        colors = "lightblue"

    # Draw the main graph
    nx.draw(G, pos,
            with_labels=True,
            node_color=colors,
            node_size=node_size,
            font_size=font_size,
            font_weight='bold',
            edge_color='gray',
            width=2,
            alpha=0.8)
    
    plt.title(title, fontsize=scaled_font_size, pad=20)

    # Calculate legacy metrics
    metrics_text = (
        f"Metrics:\n"
        f"Nodes: {G.number_of_nodes()}\n"
        f"Edges: {G.number_of_edges()}\n"
        f"Density: {nx.density(G):.3f}"
    )
    
    # Add metrics text box with scaled parameters
    plt.text(0.05, 0.98, metrics_text,
             transform=plt.gca().transAxes,
             bbox=dict(facecolor='white',
                      edgecolor='gray',
                      boxstyle=f'round,pad={scaled_pad}',
                      alpha=0.8),
             fontsize=scaled_font_size,
             verticalalignment='top')

    if save:
        plt.savefig(f'graph_pictures/{title}', transparent=True, bbox_inches='tight')
    
    plt.show()