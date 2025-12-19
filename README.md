# Subdivision des Îlots - Méthode Kusiak

## Description
Projet appliquant la **méthode Kusiak** pour la subdivision des îlots de production.  
Ensuite, les **antériorités et chaînons** sont utilisés pour optimiser l’ordonnancement et la performance des postes.

## Objectifs
- Optimiser la répartition des machines en îlots.
- Minimiser les temps de déplacement et les conflits de tâches.
- Améliorer la performance globale de la ligne de production.

## Méthodes et Algorithmes
- **Méthode Kusiak** : pour regrouper les machines selon les produits.
- **Analyse des antériorités** : pour respecter les contraintes de séquence.
- **Chaînons** : pour optimiser les flux et la continuité des opérations.

## Technologies et Outils
- Python / Jupyter Notebook
- Excel / CSV pour données
- Matplotlib / Seaborn pour visualisation
- VS Code ou Jupyter pour le développement
  
## NB!!!
Dans ce projet, la méthode des antériorités et des chaînons doit être appliquée sur chaque îlot individuellement, et non pas sur l’ensemble de la gamme de production. Cela permet d’optimiser localement les séquences et flux de chaque îlot, en respectant les contraintes spécifiques à chaque regroupement de machines, et d’améliorer la performance globale de la ligne.
