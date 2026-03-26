from regles import (
    chiffre_absent_ligne,
    chiffre_absent_colonne,
    chiffre_absent_bloc
)

def resoudre_backtracking(mat, compteur=None):
    if compteur is None:
        compteur = [0]

    for i in range(9):
        for j in range(9):
            if mat[i][j] == 0:
                for num in range(1, 10):
                    compteur[0] += 1        # on compte chaque chiffre testé
                    if (chiffre_absent_ligne(mat, i, num) and
                        chiffre_absent_colonne(mat, j, num) and
                        chiffre_absent_bloc(mat, i, j, num)):
                        mat[i][j] = num
                        if resoudre_backtracking(mat, compteur):
                            return True
                        mat[i][j] = 0
                return False
    return True