from regles import (
    chiffre_absent_ligne,
    chiffre_absent_colonne,
    chiffre_absent_bloc
)

def resoudre_backtracking(mat):
    for i in range(9):
        for j in range(9):
            if mat[i][j] == 0:
                for num in range(1, 10):
                    # On passe mat directement — regles.py attend une matrice
                    if (chiffre_absent_ligne(mat, i, num) and
                        chiffre_absent_colonne(mat, j, num) and
                        chiffre_absent_bloc(mat, i, j, num)):
                        
                        mat[i][j] = num
                        if solve_sudoku(mat):
                            return True
                        mat[i][j] = 0       # backtrack
                return False
    return True

