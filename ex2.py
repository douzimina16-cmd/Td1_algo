import random
# Matrice des coûts de transport entre les dépôts et les magasins
COUTS = ((5, 3, 4),
         (6, 7, 2))
# Quantité disponible dans chaque dépôt
OFFRES = (8, 9)
# Quantité demandée par chaque magasin

DEMANDES = (4, 5, 8)

#Calcule le coût total d'un plan de transport
def cout_solution(x):
    """Coût total d'un plan x[depot][magasin]."""
    return sum(x[i][j] * COUTS[i][j]
               for i in range(2) for j in range(3))

#Vérifie si un plan respecte toutes les contraintes
def est_faisable(x):
    return (all(sum(x[i]) == OFFRES[i] for i in range(2))
            and all(x[0][j] + x[1][j] == DEMANDES[j] for j in range(3))
            and all(v >= 0 for ligne in x for v in ligne))


def solution_initiale():
    #Retourne un premier plan de transport réalisable
    return [[4, 4, 0],
            [0, 1, 8]]


def voisins(x):
    "Génère les solutions voisines du plan de transport x"
    resultats = []
    # Parcourir les paires de magasins pour construire des mouvements
    for i in range(3):
        for j in range(3):
            if i == j:
                continue
            y = [list(ligne) for ligne in x]

            if y[0][i] > 0 and y[1][j] > 0:
                y[0][i] -= 1
                y[1][i] += 1
                y[1][j] -= 1
                y[0][j] += 1
                if est_faisable(y):
                    resultats.append((y, (i, j, 0)))
            if y is not None and x[1][i] > 0 and x[0][j] > 0:
                z = [list(ligne) for ligne in x]
                z[1][i] -= 1
                z[0][i] += 1
                z[0][j] -= 1
                z[1][j] += 1
                if est_faisable(z):
                    resultats.append((z, (i, j, 1)))

    uniques = {}
    for y, mouvement in resultats:
        cle = tuple(tuple(ligne) for ligne in y)
        uniques[cle] = (y, mouvement)
    return list(uniques.values())

#Recherche une bonne solution en utilisant la méthode taboue
def recherche_taboue(iterations=100, taille_tabou=7, seed=42):
    random.seed(seed)
    courant = solution_initiale()
    meilleur = [ligne[:] for ligne in courant]
    liste_taboue = []

    for _ in range(iterations):
        candidats = []
        for y, mouvement in voisins(courant):
            cle = tuple(tuple(ligne) for ligne in y)
            est_tabou = mouvement in liste_taboue

            if not est_tabou or cout_solution(y) < cout_solution(meilleur):
                candidats.append((cout_solution(y), y, mouvement, cle))
        if not candidats:
            break
        candidats.sort(key=lambda elem: elem[0])
        cout, courant, mouvement, _ = candidats[0]
        liste_taboue.append(mouvement)
        if len(liste_taboue) > taille_tabou:
            liste_taboue.pop(0)
        if cout < cout_solution(meilleur):
            meilleur = [ligne[:] for ligne in courant]

    return meilleur

"Affiche le plan de transport et son coût total"
def afficher(x):
    print("Plan de transport (nombre de conteneurs) :")
    print("       M1  M2  M3 | Offre")
    for i, ligne in enumerate(x):
        print(f"D{i + 1}     " + "  ".join(f"{v:2d}" for v in ligne)
              + f" | {sum(ligne)}")
    print("Dem.   " + "  ".join(f"{DEMANDES[j]:2d}" for j in range(3)))
    print("Coût total =", cout_solution(x))


if __name__ == "__main__":
    solution = recherche_taboue()
    assert est_faisable(solution)
    afficher(solution)