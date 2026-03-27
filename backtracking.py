from typing import Optional, Tuple

from regles import (
    chiffre_absent_ligne,
    chiffre_absent_colonne,
    chiffre_absent_bloc
)


def possibles(mat, i, j):
    """Renvoie la liste des chiffres possibles pour la case (i,j)."""
    res = []
    for num in range(1, 10):
        if (chiffre_absent_ligne(mat, i, num) and
            chiffre_absent_colonne(mat, j, num) and
            chiffre_absent_bloc(mat, i, j, num)):
            res.append(num)
    return res


def trouver_case_les_plus_contraignante(mat) -> Optional[Tuple[int, int]]:
    """Renvoie la case vide avec le moins de chiffres possibles."""
    meilleure = None
    meilleur_nb_possibles = 10
    for i in range(9):
        for j in range(9):
            if mat[i][j] == 0:
                nb = len(possibles(mat, i, j))
                if nb < meilleur_nb_possibles:
                    meilleur_nb_possibles = nb
                    meilleure = (i, j)
    return meilleure


def resoudre_backtracking(mat, compteur=None):
    if compteur is None:
        compteur = [0]

    case = trouver_case_les_plus_contraignante(mat)
    if case is None:
        return True  # plus de case vide → solution trouvée

    i, j = case
    candidates = possibles(mat, i, j)

    for num in candidates:
        compteur[0] += 1
        mat[i][j] = num
        if resoudre_backtracking(mat, compteur):
            return True
        mat[i][j] = 0  # backtrack

    return False