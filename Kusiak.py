import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
# MATRICE MACHINE × PIECE

data = {
    "P1": [1,0,1,0,1,0,0,1,0,0,1,0,0,0,0],
    "P2": [0,1,0,1,0,1,0,0,1,0,0,0,0,1,0],
    "P3": [1,0,1,0,0,0,0,1,0,0,1,0,0,0,0],
    "P4": [0,0,0,0,0,0,1,0,0,1,0,1,1,0,1],
    "P5": [0,1,0,1,0,1,0,0,1,0,0,0,0,1,0],
    "P6": [1,1,1,0,0,0,0,0,1,0,1,0,0,0,0],
    "P7": [0,0,0,0,0,0,1,0,0,1,0,1,1,0,1],
    "P8": [1,0,0,0,1,0,0,1,0,0,0,0,0,0,0],
    "P9": [0,0,0,1,0,1,0,0,1,0,0,0,0,1,0],
    "P10": [0,0,0,0,0,0,0,0,0,1,0,1,1,0,1]
}

machines = ["M1","M2","M3","M4","M5","M6","M7",
            "M8","M9","M10","M11","M12","M13","M14","M15"]

df = pd.DataFrame(data, index=machines)

def get_machines_of_piece(df, piece):
    return set(df.index[df[piece] == 1])

def get_pieces_of_machines(df, machines):
    machines = list(machines)
    sub = df.loc[machines]
    return set(sub.columns[sub.sum(axis=0) > 0])

def percentage(machine, pieces, df):
    total = len(pieces)
    if total == 0: 
        return 0
    return df.loc[machine, list(pieces)].sum() / total

# ALGORITHME MODIFIÉ DE KUSIAK AVEC TRAÇAGE

def kusiak_with_steps(df):
    df_work = df.copy()
    ilots = []
    step_logs = []  # Pour stocker les étapes

    ilot_number = 1

    while df_work.shape[0] > 0 and df_work.shape[1] > 0:

        log = []
        log.append(f"\n ILÔT {ilot_number} \n")

        # Étape 1 : choisir la première pièce 
        piece = df_work.columns[0]
        log.append(f"Étape 1 : Première pièce sélectionnée = {piece}")

        machines_selected = get_machines_of_piece(df_work, piece)
        log.append(f"Machines de la pièce {piece} : {sorted(machines_selected)}")

        #Étape 2 : récupérer les pièces des machines
        pieces_selected = get_pieces_of_machines(df_work, machines_selected)
        log.append(f"Étape 2 : Pièces produites par ces machines = {sorted(pieces_selected)}")

        #Étape 3 : critère 50% 
        log.append("Étape 3 : Ajout des machines ayant ≥ 50% des pièces de l’îlot")
        for m in df_work.index:
            if m not in machines_selected:
                pct = percentage(m, pieces_selected, df_work)
                if pct >= 0.5:
                    machines_selected.add(m)
                    log.append(f" → Machine {m} ajoutée (pourcentage = {pct:.2f})")

        #Étape 4 : boucle d’expansion
        log.append("Étape 4 : Expansion jusqu’à stabilisation")
        changed = True
        while changed:
            changed = False
            pieces_selected = get_pieces_of_machines(df_work, machines_selected)

            for m in df_work.index:
                if m not in machines_selected:
                    pct = percentage(m, pieces_selected, df_work)
                    if pct >= 0.5:
                        machines_selected.add(m)
                        changed = True
                        log.append(f" → Nouvelle machine ajoutée {m} (pct={pct:.2f})")

        log.append(f"Machines finales de l’îlot : {sorted(machines_selected)}")

        pieces_selected = get_pieces_of_machines(df_work, machines_selected)
        log.append(f"Pièces finales de l’îlot : {sorted(pieces_selected)}")

        #Sauvegarde
        ilots.append((machines_selected.copy(), pieces_selected.copy()))
        step_logs.append("\n".join(log))

        #Suppression
        df_work = df_work.drop(index=list(machines_selected),
                            columns=list(pieces_selected),
                            errors="ignore")

        ilot_number += 1

    return ilots, step_logs
# EXECUTION
ilots, logs = kusiak_with_steps(df)

print("\n=== ILÔTS FORMÉS ===\n")
for i, (mach, pieces) in enumerate(ilots, start=1):
    print(f"Ilot {i}: Machines={sorted(mach)} | Pièces={sorted(pieces)}")

print("\n DÉTAILS DE TOUTES LES ÉTAPES \n")
for log in logs:
    print(log)

print("\n=== MATRICE TRIÉE PAR ÎLOTS ===\n")

ordered_machines = []
ordered_pieces = []
for mach_set, pieces_set in ilots:
    ordered_machines.extend(sorted(mach_set))
    ordered_pieces.extend(sorted(pieces_set))

df_sorted = df.loc[ordered_machines, ordered_pieces]

print(df_sorted.to_string())

# ==================== NOUVEAU CODE POUR LA FIGURE ====================

# Calcul des séparateurs entre îlots
mach_counts = [len(mach_set) for mach_set, _ in ilots]
piece_counts = [len(pieces_set) for _, pieces_set in ilots]

mach_separators = np.cumsum(mach_counts)[:-1]   # Positions des lignes horizontales
piece_separators = np.cumsum(piece_counts)[:-1]  # Positions des lignes verticales

# Création de la figure avec seaborn
plt.figure(figsize=(12, 10))
ax = sns.heatmap(df_sorted,
                 annot=True,                    # Affiche 0 et 1
                 fmt="d",
                 cmap="binary",                 # Noir = 1, Blanc = 0
                 linewidths=0.5,
                 linecolor='lightgray',
                 cbar=False,
                 annot_kws={"size": 11})

# Colorer les 1 en rouge et les 0 en gris clair
for text in ax.texts:
    if text.get_text() == '1':
        text.set_color('red')
        text.set_weight('bold')
    elif text.get_text() == '0':
        text.set_color('lightgray')

# Lignes bleues épaisses pour séparer les îlots
for sep in mach_separators:
    ax.axhline(sep, color='blue', linewidth=4)
for sep in piece_separators:
    ax.axvline(sep, color='blue', linewidth=4)

# Titres et labels
plt.title("Matrice Machine-Pièce triée par îlots\n(Algorithme de Kusiak modifié)",
        fontsize=16, pad=20)
plt.xlabel("Pièces", fontsize=13)
plt.ylabel("Machines", fontsize=13)

# Labels des axes
plt.xticks(rotation=0, fontsize=10)
plt.yticks(rotation=0, fontsize=10)

plt.tight_layout()
plt.show()
