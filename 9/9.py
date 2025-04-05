# Создание, анализ, раскраска графов.
import networkx as nx
# Визуализация графа
import matplotlib.pyplot as plt
# Обход графа
from collections import deque

# Исходные данные
edges = [
    (4, 15), (3, 7), (7, 8), (4, 16), (9, 15), (7, 10), (4, 13),
    (10, 12), (8, 13), (6, 11), (5, 13), (6, 13), (10, 11),
    (8, 12), (3, 12), (8, 14), (10, 13), (8, 15), (5, 7), (2, 8),
    (5, 15), (4, 14), (2, 5), (6, 16), (8, 11), (9, 13), (3, 14),
    (5, 14), (9, 16), (10, 15), (2, 3), (3, 15), (9, 14),
    (5, 16), (6, 12)
]

G = nx.Graph()
G.add_edges_from(edges)


# Проверка двудольности
def is_bipartite(graph):
    try:
        color = nx.bipartite.color(graph)
        return True, color
    except nx.NetworkXError:
        return False, None


bipartite, coloring = is_bipartite(G)
print(f"Граф двудольный: {bipartite}")


if not bipartite:
    cycles = list(nx.cycle_basis(G))
    edges_to_remove = set()
    for cycle in cycles:
        if len(cycle) % 2 != 0:
            edges_to_remove.add((cycle[0], cycle[1]))
    print(f"Удаляем рёбра: {edges_to_remove}")
    G.remove_edges_from(edges_to_remove)
    bipartite, coloring = is_bipartite(G)
    print(f"После удаления рёбер граф двудольный: {bipartite}")

if bipartite:
    left = {node for node in coloring if coloring[node] == 0}
    right = set(G.nodes()) - left
    print(f"Левая доля: {left}")
    print(f"Правая доля: {right}")
else:
    print("Не удалось сделать граф двудольным")
    exit()


# Форд-Фалкерсон
def ford_fulkerson_matching(graph, left, right):
    flow_network = nx.DiGraph()

    source = 'source'
    sink = 'sink'
    flow_network.add_node(source)
    flow_network.add_node(sink)

    for node in left:
        flow_network.add_edge(source, node, capacity=1)

    for node in right:
        flow_network.add_edge(node, sink, capacity=1)

    for u, v in graph.edges():
        if u in left and v in right:
            flow_network.add_edge(u, v, capacity=1)
        elif v in left and u in right:
            flow_network.add_edge(v, u, capacity=1)

    flow_value, flow_dict = nx.maximum_flow(flow_network, source, sink)

    matching = []
    for u in flow_dict:
        if u == source or u == sink:
            continue
        for v in flow_dict[u]:
            if v != sink and flow_dict[u][v] == 1:
                matching.append((u, v))

    return matching


# Алгоритм Куна
def kuhn_matching(graph, left, right):
    pair_U = {u: None for u in left}
    pair_V = {v: None for v in right}

    def dfs(u, visited):
        for v in graph.neighbors(u):
            if v not in visited:
                visited.add(v)
                if pair_V[v] is None or dfs(pair_V[v], visited):
                    pair_U[u] = v
                    pair_V[v] = u
                    return True
        return False

    for u in left:
        dfs(u, set())
    matching = [(u, v) for u, v in pair_U.items() if v is not None]
    return matching


ff_matching = ford_fulkerson_matching(G, left, right)
kuhn_matching = kuhn_matching(G, left, right)

print("\nНаибольшее паросочетание (Форд-Фалкерсон):")
print(ff_matching)
print(f"Размер: {len(ff_matching)}")

print("\nНаибольшее паросочетание (Кун):")
print(kuhn_matching)
print(f"Размер: {len(kuhn_matching)}")


def visualize_graph(graph, left, right, matching, title):
    plt.figure(figsize=(12, 8))
    pos = {}
    left_nodes = sorted(left)
    right_nodes = sorted(right)

    for i, node in enumerate(left_nodes):
        pos[node] = (0, -i)

    for i, node in enumerate(right_nodes):
        pos[node] = (1, -i)

    nx.draw_networkx_nodes(graph, pos, nodelist=left, node_color='lightblue', node_size=500)
    nx.draw_networkx_nodes(graph, pos, nodelist=right, node_color='lightgreen', node_size=500)
    nx.draw_networkx_edges(graph, pos, edge_color='gray', width=1)
    nx.draw_networkx_edges(graph, pos, edgelist=matching, edge_color='red', width=2)
    nx.draw_networkx_labels(graph, pos)

    plt.title(title)
    plt.axis('off')
    plt.show()


visualize_graph(G, left, right, ff_matching, "Наибольшее паросочетание (Форд-Фалкерсон)")
visualize_graph(G, left, right, kuhn_matching, "Наибольшее паросочетание (Кун)")
