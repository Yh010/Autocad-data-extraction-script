import ezdxf
import networkx as nx
import matplotlib.pyplot as plt


def extract_lwpolylines(file_path):
    lwpolylines = []
    doc = ezdxf.readfile(file_path)
    modelspace = doc.modelspace()

    for entity in modelspace:
        if entity.dxftype() == "LWPOLYLINE":
            vertices = []
            for vertex in entity.get_points():
                vertices.append((vertex[0], vertex[1]))  # Extract x and y coordinates
            lwpolylines.append(vertices)

    return lwpolylines


def create_graph_from_lwpolylines(lwpolylines):
    graph = nx.Graph()

    for polyline in lwpolylines:
        prev_vertex = None
        for vertex in polyline:
            if prev_vertex is not None:
                graph.add_edge(prev_vertex, vertex)
            prev_vertex = vertex

    return graph


def dijkstra_shortest_path(graph, source, target):
    if source not in graph.nodes or target not in graph.nodes:
        return None

    shortest_path = nx.dijkstra_path(graph, source, target)

    return shortest_path


# Provide the path to your DXF file
file_path = "/content/nodes1.dxf"

lwpolylines = extract_lwpolylines(file_path)
graph = create_graph_from_lwpolylines(lwpolylines)

# Print the graph as a linked list
print("Graph:")
for node in sorted(graph.nodes):
    neighbors = list(graph.neighbors(node))
    if neighbors:
        print(f"Node {node}: {neighbors}")
    else:
        print(f"Node {node}: None")

# Get user input for source and target nodes
source_input = input("Enter the source node (x, y): ")
target_input = input("Enter the target node (x, y): ")

# Parse the user input as (x, y) coordinates
source = tuple(map(float, source_input.strip("() ").split(",")))
target = tuple(map(float, target_input.strip("() ").split(",")))

# Find the shortest path using Dijkstra's algorithm
shortest_path = dijkstra_shortest_path(graph, source, target)

# Print the shortest path
print("Shortest path:")
if shortest_path:
    for node in shortest_path:
        print(node)
else:
    print("No path found.")

# Draw the graph with the shortest path highlighted
pos = nx.spring_layout(graph)
plt.figure(figsize=(8, 6))
nx.draw_networkx(graph, pos, with_labels=True, node_size=200)
if shortest_path:
    nx.draw_networkx_edges(graph, pos, edgelist=[(shortest_path[i], shortest_path[i + 1]) for i in range(len(shortest_path) - 1)],
                           edge_color='r', width=2)
plt.title("Graph with Shortest Path")
plt.axis("off")
plt.show()
