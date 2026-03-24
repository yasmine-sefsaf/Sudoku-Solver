def est_valide(mat, i, j, num):
    """Vérifie si num peut être placé en mat[i][j] sans violer les règles."""
    n = 9

    # Vérifier la ligne
    for x in range(n):
        if mat[i][x] == num:
            return False

    # Vérifier la colonne
    for x in range(n):
        if mat[x][j] == num:
            return False

    # Vérifier le bloc 3x3
    start_i = 3 * (i // 3)
    start_j = 3 * (j // 3)
    for x in range(3):
        for y in range(3):
            if mat[start_i + x][start_j + y] == num:
                return False

    return True


def solve_sudoku(mat):
    """Résout le Sudoku avec backtracking."""
    n = 9

    for i in range(n):
        for j in range(n):
            if mat[i][j] == 0:
                # Essayer les chiffres 1 à 9
                for num in range(1, 10):
                    if est_valide(mat, i, j, num):
                        mat[i][j] = num
                        if solve_sudoku(mat):
                            return True
                        mat[i][j] = 0  # retour en arrière
                return False  # aucune valeur ne marche
    return True  # grille complète


# --- Grille donnée en chaînes avec '_' pour les vides ---
lines = [
    "_729___3_",
    "__1__6_8_",
    "____4__6_",
    "96___41_8",
    "_487_5_96",
    "__56_8__3",
    "___4_2_1_",
    "85__6_327",
    "1__85____"
]

# Conversion en grille 9x9 avec 0 pour les cases vides
grille = []
for line in lines:
    row = []
    for c in line:
        if c == "_":
            row.append(0)
        else:
            row.append(int(c))
    grille.append(row)

# Affichage de la grille initiale
print("Grille initiale :")
for row in grille:
    print(row)

# Résolution
if solve_sudoku(grille):
    print("\nSolution trouvée :")
    for row in grille:
        print(row)
else:
    print("Aucune solution possible.")
