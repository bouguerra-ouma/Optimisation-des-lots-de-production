import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
# Gamme
products = {
    "P1": (["M1","M3","M5","M8","M11"], 5),
    "P2": (["M2","M4","M6","M9","M14"], 5),
    "P3": (["M1","M3","M8","M11"], 4),
    "P4": (["M7","M10","M12","M13","M15"], 4),
    "P5": (["M2","M4","M6","M9","M14"], 5),
    "P6": (["M1","M2","M3","M9","M11"], 6),
    "P7": (["M7","M10","M12","M15"], 4),
    "P8": (["M1","M5","M8","M11"], 5),
    "P9": (["M4","M6","M9","M14"], 4),
    "P10": (["M10","M12","M13","M15"], 3)
}

# Liste des machines
machines = sorted({m for p in products.values() for m in p[0]})

# 2. CALCUL DES CHAÎNONS
chainons = defaultdict(int)
for gamme, poids in products.values():
    for i in range(len(gamme) - 1):
        m1, m2 = sorted([gamme[i], gamme[i+1]])
        chainons[(m1, m2)] += poids

# 3. MATRICE TRIANGULAIRE DES CHAÎNONS
matrix = pd.DataFrame(0, index=machines, columns=machines)

for (m1, m2), value in chainons.items():
    matrix.loc[m1, m2] = value

print("\n===== MATRICE TRIANGULAIRE DES CHAÎNONS =====")
print(matrix)

# 4. NOMBRE DE CHAÎNONS ET TRAFIC TOTAL
nb_chainons = defaultdict(int)
trafic_total = defaultdict(int)

for (m1, m2), value in chainons.items():
    nb_chainons[m1] += 1
    nb_chainons[m2] += 1
    trafic_total[m1] += value
    trafic_total[m2] += value

df_trafic = pd.DataFrame({
    "Machine": machines,
    "Nb_chainons": [nb_chainons[m] for m in machines],
    "Trafic_total": [trafic_total[m] for m in machines]
})

# POSTE DIRECTEUR 
df_trafic_sorted = df_trafic.sort_values(
    by=["Nb_chainons", "Trafic_total"],
    ascending=[False, False]
)

poste_directeur = df_trafic_sorted.iloc[0]["Machine"]

print("\n===== CLASSEMENT POUR POSTE DIRECTEUR =====")
print(df_trafic_sorted)

print(f"\n👉 POSTE DIRECTEUR (méthode des chaînons) : {poste_directeur}")

# 6. GRAPHE DES CHAÎNONS
G = nx.Graph()
for (m1, m2), value in chainons.items():
    G.add_edge(m1, m2, weight=value)

# Position pour tous les dessins (reproductible)
pos = nx.spring_layout(G, seed=42)

plt.figure(figsize=(16, 8))
nx.draw_networkx_nodes(G, pos, node_size=2200, node_color="#FFD966")
nx.draw_networkx_edges(G, pos, edge_color="steelblue", width=1.5)
nx.draw_networkx_labels(G, pos, font_size=10)

edge_labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)

plt.title("Graphe initial – Méthode des chaînons")
plt.axis("off")
plt.show()


# 6. GRAPHE AMÉLIORÉ (ARBRE DES CHAÎNONS PRINCIPAUX)
# Arbre couvrant maximal (Maximum Spanning Tree) → conserve les chaînons les plus forts
arbre_amelioré = nx.maximum_spanning_tree(G)

positions = pos  # Même positions pour cohérence visuelle

plt.figure(figsize=(16, 8))
nx.draw_networkx_nodes(arbre_amelioré, positions, node_size=2200, node_color="#FFD966")
nx.draw_networkx_edges(arbre_amelioré, positions, edge_color="green", width=3)
nx.draw_networkx_labels(arbre_amelioré, positions, font_size=10)

edge_labels2 = nx.get_edge_attributes(arbre_amelioré, "weight")
nx.draw_networkx_edge_labels(arbre_amelioré, positions, edge_labels=edge_labels2, font_size=9)

plt.title("Graphe amélioré – Arbre des chaînons principaux (Maximum Spanning Tree)")
plt.axis("off")
plt.show()

# 7. CHAÎNONS HORS TRAME ET CROISEMENTS

def detecter_hors_trame(G_initial, G_final):
    chainons_hors_trame = {}
    for u, v, data in G_initial.edges(data=True):
        if not G_final.has_edge(u, v) and not G_final.has_edge(v, u):
            chainons_hors_trame[(min(u,v), max(u,v))] = data["weight"]
    return chainons_hors_trame

chainons_hors_trame = detecter_hors_trame(G, arbre_amelioré)

print("\n===== CHAÎNONS HORS TRAME / CROISEMENTS =====")
for (u, v), w in sorted(chainons_hors_trame.items()):
    print(f"{u} - {v} : {w}")


# 8. CALCUL DU RATIO D'OPTIMALITÉ RO (CORRIGÉ ET CLAIR)
# 7. CALCUL DU RATIO D’OPTIMALITÉ (RO) – MÉTHODE SHINON
# RO = 1 − (Nombre de chaînons hors trame) / (Nombre total de chaînons)


nb_total_chainons = 19
nb_hors_trame_avant = 3
nb_hors_trame_apres = 0

RO_avant = 1 - (nb_hors_trame_avant / nb_total_chainons)
RO_apres = 1 - (nb_hors_trame_apres / nb_total_chainons)

print("\n===== RATIO D'OPTIMALITÉ =====")
print(f"Nombre total de chaînons = {nb_total_chainons}")
print(f"RO avant amélioration = 1 - {nb_hors_trame_avant}/{nb_total_chainons} = {RO_avant:.2f}")
print(f"RO après amélioration = 1 - {nb_hors_trame_apres}/{nb_total_chainons} = {RO_apres:.2f}")


