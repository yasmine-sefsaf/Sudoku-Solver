from itertools import product
from regles import (
    chiffre_absent_ligne,
    chiffre_absent_colonne,
    chiffre_absent_bloc,
    grille_valide
)
import copy
import random

def resoudre_force_brute_iterative(grille):
    # Force brute itérative : répète des passes sur la grille.Chaque passe place le premier chiffre valide dans chaque case vide.S'arrête quand la grille est résolue ou quand aucun progrès n'est fait.vRapide mais ne résout pas les grilles complexes.
    while True:
        cases_remplies_ce_tour = 0
        cases_vides_restantes = 0

        for i in range(9):
            for j in range(9):
                if grille[i][j] == 0:
                    cases_vides_restantes += 1
                    for chiffre in range(1, 10):
                        if (chiffre_absent_ligne(grille, i, chiffre) and
                            chiffre_absent_colonne(grille, j, chiffre) and
                            chiffre_absent_bloc(grille, i, j, chiffre)):
                            grille[i][j] = chiffre
                            cases_remplies_ce_tour += 1
                            break

        if cases_vides_restantes == 0:
            return True

        if cases_remplies_ce_tour == 0:
            return False


def resoudre_force_brute_exhaustive(grille):
    # Test toutes les combinaisons possibles (8,73 * 10e43) en incrémentant chaque combinaison de 1
    cases_vides = []
    for i in range(9):
        for j in range(9):
            if grille[i][j] == 0:
                cases_vides.append((i, j))
    # Pour les stats
    combinaisons_testees = 0
    total = 9 ** len(cases_vides)

    # Mise en route  du processus, avec prise en compte des combinaisons pour stats
    try:
        for combinaison in product(range(1, 10), repeat=len(cases_vides)):
            combinaisons_testees += 1
            grille_test = copy.deepcopy(grille)
            for k, (i, j) in enumerate(cases_vides):
                grille_test[i][j] = combinaison[k]

            if grille_valide(grille_test):
                for i in range(9):
                    for j in range(9):
                        grille[i][j] = grille_test[i][j]
                return True, combinaisons_testees, total

    except KeyboardInterrupt:
        pass

    return False, combinaisons_testees, total


def bruteforce_aleatoire_memoire(grille, max_tentatives=100000, stats=None):
    # Force brute aléatoire avec mémoire.Tire au hasard parmi les candidats valides à chaque case.Stocke les combinaisons testées pour ne jamais les refaire (garantie par set).S'arrête après max_tentatives combinaisons uniques (condition d'arrêt).

    # 
    combinaisons_testees = set()
    tentatives = 0

    while tentatives < max_tentatives:
        grille_test = copy.deepcopy(grille)
        combinaison = []
        bloquee = False

        if stats is not None:
            if len(stats) == 0:
                stats.append(tentatives)
                stats.append(len(combinaisons_testees))
            else:
                stats[0] = tentatives
                stats[1] = len(combinaisons_testees)
        # Optimisation des candidats possibles par case
        for i in range(9):
            for j in range(9):
                if grille_test[i][j] == 0:
                    candidats = [
                        c for c in range(1, 10)
                        if (chiffre_absent_ligne(grille_test, i, c) and
                            chiffre_absent_colonne(grille_test, j, c) and
                            chiffre_absent_bloc(grille_test, i, j, c))
                    ]

                    if not candidats:
                        bloquee = True
                        break
                    # Création de la sortie random par case
                    random.shuffle(candidats)
                    grille_test[i][j] = candidats[0]
                    combinaison.append(candidats[0])

            if bloquee:
                break
        # On encapsule la solution générée en random
        cle = tuple(combinaison)

        # Combinaison déjà testée → on repart sans compter
        if cle in combinaisons_testees:
            continue

        # Nouvelle combinaison → on stocke et on compte
        combinaisons_testees.add(cle)
        tentatives += 1

        # Vérifie si la grille est complète et valide
        if not bloquee and grille_valide(grille_test):
            for i in range(9):
                for j in range(9):
                    grille[i][j] = grille_test[i][j]
            return True, tentatives, len(combinaisons_testees)

    return False, tentatives, len(combinaisons_testees)


def bruteforce_exhaustif_aleatoire_memoire(grille, max_tentatives=100000):

    # Force brute exhaustive aléatoire avec mémoire. Tire 45 chiffres au hasard (De 1 à 9 pour chaque chiffre) sans vérifier les règles pendant le remplissage. Vérifie la grille complète seulement à la fin. Condition d'arrêt : max_tentatives combinaisons uniques testées. Illustre la saturation mémoire et l'importance de la condition d'arrêt.

    # mémoire des combinaisons vues, et garantie que les combinaisons testées ne soient pas répétées.
    combinaisons_testees = set()  

    # Préparation des stats 
    tentatives = 0
    total_generees = 0

    # Récupère les positions des cases vides
    cases_vides = []
    for i in range(9):
        for j in range(9):
            if grille[i][j] == 0:
                cases_vides.append((i, j))

    # Préparation des cases disponibles pour réceptionner le random généré
    nb_cases_vides = len(cases_vides)

    while tentatives < max_tentatives:   # ← CONDITION D'ARRÊT

        # Tire au hasard sans vérifier les règles
        combinaison = tuple(random.randint(1, 9) for _ in range(nb_cases_vides))
        total_generees += 1
        # Combinaison déjà testée → on repart sans compter
        if combinaison in combinaisons_testees:
            continue

        # Nouvelle combinaison → on stocke et on compte
        combinaisons_testees.add(combinaison)
        tentatives += 1

        # On remplit la grille test
        grille_test = copy.deepcopy(grille)
        for k, (i, j) in enumerate(cases_vides):
            grille_test[i][j] = combinaison[k]

        # On vérifie les règles seulement maintenant
        if grille_valide(grille_test):
            for i in range(9):
                for j in range(9):
                    grille[i][j] = grille_test[i][j]
            return True, tentatives, len(combinaisons_testees)

    # Condition d'arrêt atteinte
    return False, tentatives, len(combinaisons_testees)