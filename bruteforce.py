from itertools import product
from regles import (
    chiffre_absent_ligne,
    chiffre_absent_colonne,
    chiffre_absent_bloc,
    grille_valide
)
import copy

def resoudre_force_brute_iterative(grille):
    """
    Force brute itérative : répète des passes sur la grille.
    Chaque passe place le premier chiffre valide dans chaque case vide.
    S'arrête quand la grille est résolue ou quand aucun progrès n'est fait.
    Rapide mais ne résout pas les grilles complexes.
    """
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
    cases_vides = []
    for i in range(9):
        for j in range(9):
            if grille[i][j] == 0:
                cases_vides.append((i, j))

    combinaisons_testees = 0
    total = 9 ** len(cases_vides)

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

