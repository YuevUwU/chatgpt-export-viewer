import json
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout

CHAT_FILE = "chats/6832e47a-4068-8004-a657-e48531c85711.json"

# ---------- Load JSON file (replace with your own file if needed) ----------
with open(CHAT_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)
mapping = data['mapping']
G = nx.DiGraph()

# ---------- Build the graph ----------
for node_id, node_info in mapping.items():
    G.add_node(node_id)

    parent = node_info.get('parent')
    if parent:
        G.add_edge(parent, node_id)

# ---------- Simplify node IDs for labeling ----------
def short_id(uid):
    return uid[:6]

labels = {node: short_id(node) for node in G.nodes}

# ---------- Set node colors based on role ----------
colors = []
for node_id in G.nodes:
    message = mapping[node_id].get('message', {}) or {}
    role = message.get('author', {}).get('role', None)
    if role == 'user':
        colors.append('lightgreen')
    elif role == 'assistant':
        colors.append('lightblue')
    elif role == 'system':
        colors.append('orange')
    else:
        colors.append('gray')

# ---------- Draw the graph ----------
plt.figure(figsize=(16, 12))

try:
    pos = graphviz_layout(G, prog='dot')
except:
    print("Please install pygraphviz: pip install pygraphviz")
    exit()

nx.draw(G, pos, with_labels=False, arrows=True, node_color=colors, node_size=1200)
nx.draw_networkx_labels(G, pos, labels=labels, font_size=8)

plt.title("Node Relationship Graph (Layered + Role-based Coloring)", fontsize=14)
plt.axis('off')

# ---------- Save the graph image ----------
plt.savefig("node_graph.png", dpi=300)
print("Saved as node_graph.png")
