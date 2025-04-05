import networkx as nx

G = nx.Graph()
edges = [(0,1), (0,2), (0,5), (6,0), (1,5), (1,2), (1,3),
         (2,3), (3,6), (7,3), (3,4), (4,5), (5,6), (6,7)]
G.add_edges_from(edges)

L = nx.line_graph(G)
print("Рёбра рёберного графа:", L.edges())
