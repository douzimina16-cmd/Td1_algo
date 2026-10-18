"--le problème du voyageur de commerce--!"
import math
import random
"--dictionnare contient les distances entre certaines paires de sommets--!"
DONNEES = {
    (1, 2): 14, (1, 3): 15, (1, 8): 17,
    (2, 3): 13, (2, 4): 14, (2, 5): 20, (2, 8): 21,
    (3, 4): 11, (3, 5): 21, (3, 6): 17, (3, 7): 9, (3, 8): 9,
    (4, 5): 11, (4, 6): 10, (4, 7): 8, (4, 8): 20,
    (5, 6): 15, (5, 7): 18,
    (6, 7): 9,
    (7, 8): 13,
}


N = 8
INITIAL = [1, 2, 3, 4, 5, 6, 7, 8]
"!--liste  intial de sommets!--"


# Récupérer la distance entre deux sommets, quel que soit leur ordre
def distance(a, b):
    return DONNEES.get((min(a, b), max(a, b)))


def cout(tour):
    # Fermer le circuit en revenant au sommet de départ
    route = tour + [tour[0]]
    total = 0  #inialiser le cout totale

    # Parcourir les paires de sommets
    for a, b in zip(route, route[1:]):
        d = distance(a, b)

        if d is None:
            return math.inf

        total += d

    return total

"--!génère les solutions voisines d'un circuit--!"
def voisins(tour):
    result = []

    for i in range(1, N - 1):
        for j in range(i + 1, N):
            v = tour[:]
            v[i], v[j] = v[j], v[i]

            if math.isfinite(cout(v)):
                mouvement = (
                    min(tour[i], tour[j]),
                    max(tour[i], tour[j])
                )
                result.append((v, mouvement))

    return result

#une méthode d'optimisation locale
# Effectuer plusieurs départs pour diversifier la recherche
def recherche_taboue(iterations=100, taille_tabou=10, seed=11):
    random.seed(seed)
    meilleur_global = INITIAL[:]

    for depart in range(30):
        if depart == 0:
            courant = INITIAL[:]
        else:
            courant = [1] + random.sample(
                list(range(2, N + 1)), N - 1
            )

            essais = 0

            while not math.isfinite(cout(courant)) and essais < 500:
                courant = [1] + random.sample(
                    list(range(2, N + 1)), N - 1
                )
                essais += 1

            if not math.isfinite(cout(courant)):
                continue

        meilleur_local = courant[:]
        tabou = []

        for _ in range(iterations):
            candidats = []

            for v, mouvement in voisins(courant):
                if (mouvement not in tabou
                        or cout(v) < cout(meilleur_local)):
                    candidats.append((cout(v), v, mouvement))

            if not candidats:
                break

            candidats.sort(key=lambda x: x[0])
            valeur, courant, mouvement = candidats[0]

            tabou.append(mouvement)

            if len(tabou) > taille_tabou:
                tabou.pop(0)

            if valeur < cout(meilleur_local):
                meilleur_local = courant[:]

        if cout(meilleur_local) < cout(meilleur_global):
            meilleur_global = meilleur_local[:]

    return meilleur_global

# choisir aléatoirement un voisin à chaque itération
# qui dépend de la température
def recuit_simule(iterations=5, temperature_initiale=20.0,
                  alpha=0.8, seed=7):
    random.seed(seed)

    courant = INITIAL[:]
    meilleur = courant[:]
    temperature = temperature_initiale
    historique = []

    for k in range(iterations):
        candidats = voisins(courant)

        if not candidats:
            break

        voisin, _ = random.choice(candidats)

        delta = cout(voisin) - cout(courant)

        accepte = (
            delta <= 0
            or random.random() < math.exp(
                -delta / max(temperature, 1e-9)
            )
        )

        if accepte:
            courant = voisin

        if cout(courant) < cout(meilleur):
            meilleur = courant[:]

        historique.append(
            (k + 1, temperature, cout(courant), accepte)
        )

        temperature *= alpha

    return meilleur, historique

#affiche le nom de la méthode, le circuit et son coût
def afficher(nom, tour):
    print(nom)
    print("Circuit :", "-".join(map(str, tour + [tour[0]])))

    if math.isfinite(cout(tour)):
        print("Coût :", cout(tour))
    else:
        print("Coût : circuit non réalisable")

    print()


if __name__ == "__main__":
    print("Solution initiale :")
    afficher("Circuit initial", INITIAL)

    afficher("Recherche taboue", recherche_taboue())

    solution_rs, historique = recuit_simule()
    afficher("Recuit simulé (5 itérations)", solution_rs)

    print("Historique (itération, T, coût courant, voisin accepté) :")

    for ligne in historique:
        print(ligne)

    print()