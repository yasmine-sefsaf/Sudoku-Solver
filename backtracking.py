# from regles import (
#     chiffre_absent_ligne,
#     chiffre_absent_colonne,
#     chiffre_absent_bloc
# )

# def resoudre_backtracking(mat):
    
#     for i in range(9):
#         for j in range(9):
#             if mat[i][j] == 0:
#                 for num in range(1, 10):
#                     # On passe mat directement — regles.py attend une matrice
#                     if (chiffre_absent_ligne(mat, i, num) and
#                         chiffre_absent_colonne(mat, j, num) and
#                         chiffre_absent_bloc(mat, i, j, num)):
                        
#                         mat[i][j] = num
#                         if resoudre_backtracking(mat):
#                             return True
#                         mat[i][j] = 0       # backtrack
#                 return False
#     return True

# from regles import (
#     chiffre_absent_ligne,
#     chiffre_absent_colonne,
#     chiffre_absent_bloc
# )

# def resoudre_backtracking(mat, compteur=None):
#     if compteur is None:
#         compteur = [0]

#     for i in range(9):
#         for j in range(9):
#             if mat[i][j] == 0:
#                 for num in range(1, 10):
#                     compteur[0] += 1        # on compte chaque chiffre testé
#                     if (chiffre_absent_ligne(mat, i, num) and
#                         chiffre_absent_colonne(mat, j, num) and
#                         chiffre_absent_bloc(mat, i, j, num)):
#                         mat[i][j] = num
#                         if resoudre_backtracking(mat, compteur):
#                             return True
#                         mat[i][j] = 0
#                 return False
#     return True
from regles import (
    chiffre_absent_ligne,
    chiffre_absent_colonne,
    chiffre_absent_bloc
)


def valeurs_possibles(mat, i, j):
    possibles = []
    for num in range(1, 10):
        if (chiffre_absent_ligne(mat, i, num) and
            chiffre_absent_colonne(mat, j, num) and
            chiffre_absent_bloc(mat, i, j, num)):
            possibles.append(num)
    return possibles


def trouver_meilleure_case(mat):
    best_i, best_j = None, None
    best_possibles = None

    for i in range(9):
        for j in range(9):
            if mat[i][j] == 0:
                possibles = valeurs_possibles(mat, i, j)
                if len(possibles) == 0:
                    return None, None, []
                if best_possibles is None or len(possibles) < len(best_possibles):
                    best_i, best_j = i, j
                    best_possibles = possibles

    return best_i, best_j, best_possibles


def resoudre_backtracking(mat, compteur=None):
    if compteur is None:
        compteur = [0]

    # Choisir la meilleure case vide (MRV)
    i, j, possibles = trouver_meilleure_case(mat)

    # Plus de case vide -> sudoku résolu
    if i is None and j is None:
        return True

    # Si aucune valeur possible pour cette case -> impasse
    if not possibles:
        return False

    # Essayer uniquement les valeurs possibles
    for num in possibles:
        compteur[0] += 1
        mat[i][j] = num
        if resoudre_backtracking(mat, compteur):
            return True
        mat[i][j] = 0  # backtrack

    return False
