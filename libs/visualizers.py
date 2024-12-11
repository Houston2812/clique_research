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
                   dims: tuple = (5, 5)):
   
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
    plt.show()