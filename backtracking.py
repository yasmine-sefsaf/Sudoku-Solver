
from regles import (
    chiffre_absent_ligne,
    chiffre_absent_colonne, 
    chiffre_absent_bloc
)

def solve_sudoku(mat):
    """Backtracking - APPELLE DIRECTEMENT regles.py"""
    n = 9
    for i in range(n):
        for j in range(n):
            if mat[i][j] == 0:
                # Conversion pour regles.py
                grille_1d = [cell for row in mat for cell in row]
                case = i * 9 + j
                ligne = i
                colonne = j
                
                for num in range(1, 10):
                    # SUPPRIME est_valide → APPELLE les 3 fonctions de regles.py
                    if (chiffre_absent_ligne(grille_1d, ligne, num) and 
                        chiffre_absent_colonne(grille_1d, colonne, num) and 
                        chiffre_absent_bloc(grille_1d, case, num)):
                        
                        mat[i][j] = num
                        if solve_sudoku(mat):
                            return True
                        mat[i][j] = 0  # backtrack
                return False
    return True

