import networkx as nx
import matplotlib.pyplot as plt

#GAMMES DE FABRICATION
gammes = {
    "P1": ["M1", "M3", "M5", "M8", "M11"],
    "P2": ["M2", "M4", "M6", "M9", "M14"],
    "P3": ["M1", "M3", "M8", "M11"],
    "P4": ["M7", "M10", "M12", "M13", "M15"],
    "P5": ["M2", "M4", "M6", "M9", "M14"],
    "P6": ["M1", "M2", "M3", "M9", "M11"],
    "P7": ["M7", "M10", "M12", "M15"],
    "P8": ["M1", "M5", "M8", "M11"],
    "P9": ["M4", "M6", "M9", "M14"],
    "P10": ["M10", "M12", "M13", "M15"]
}
#LISTE DES MACHINES
machines = sorted({m for gamme in gammes.values() for m in gamme})

#CONSTRUCTION DES RELATIONS D’ANTÉRIORITÉ
def build_precedence_relations(gammes):
    precedences = {m: set() for m in machines}

    for gamme in gammes.values():
        for i in range(len(gamme)):
            for j in range(i + 1, len(gamme)):
                precedences[gamme[j]].add(gamme[i])

    return precedences

#METHODE DES NIVEAUX (ANTÉRIORITÉS)
def compute_levels(precedences):
    precedences = {k: set(v) for k, v in precedences.items()}
    levels = []
    remaining = set(precedences.keys())

    while remaining:
        level = sorted([m for m in remaining if precedences[m].issubset(set().union(*levels) if levels else set())])
        levels.append(level)
        remaining -= set(level)

    return levels

#EXECUTION
precedences = build_precedence_relations(gammes)
levels = compute_levels(precedences)

#AFFICHAGE STRUCTURÉ 
print("\n====== MISE EN LIGNE PAR METHODE DES ANTERIORITES ======\n")

for i, level in enumerate(levels, start=1):
    print(f"Niveau {i} : {', '.join(level)}  (en parallèle)")


#Graphe des antériorités
G = nx.DiGraph()

for produit, sequence in gammes.items():
    for i in range(len(sequence) - 1):
        G.add_edge(sequence[i], sequence[i+1])

# Positionnement manuel par niveaux
pos = {}
y_max_per_level = {}

for lvl_idx, level in enumerate(levels):
    n = len(level)
    spacing = 2.0  # espacement vertical
    start_y = (n - 1) * spacing / 2
    for mach_idx, machine in enumerate(level):
        pos[machine] = (lvl_idx * 4, start_y - mach_idx * spacing)

# Affichage
plt.figure(figsize=(16, 10))
plt.title("Graphe des antériorités – Mise en ligne par niveaux", fontsize=18, pad=30)

nx.draw_networkx_nodes(G, pos, node_size=3500, node_color="#A0CBE2", 
                edgecolors="black", linewidths=2)

nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold")

nx.draw_networkx_edges(G, pos, arrows=True, arrowsize=30, arrowstyle="-|>",
                edge_color="darkblue", width=2.5)

# Annotation des niveaux
max_y = max(y for x, y in pos.values())
for i in range(len(levels)):
    plt.text(i * 4, max_y + 1.5, f"Niveau {i+1}", 
        fontsize=15, weight="bold", ha="center", va="center",
        bbox=dict(facecolor="lightyellow", alpha=0.9, boxstyle="round,pad=0.8"))

plt.axis("off")
plt.tight_layout()
plt.show()

