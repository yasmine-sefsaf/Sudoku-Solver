def trouver_case_vide(grille):
    for i in range(9):
        for j in range(9):
            if grille[i][j] == 0:
                return (i, j)
    return None

def chiffre_absent_ligne(grille, ligne, chiffre):
    for j in range(9):
        if grille[ligne][j] == chiffre:
            # return False — retourné à l'intérieur de la boucle, dès qu'une case de la ligne contient déjà le chiffre cherché. On sort immédiatement, inutile de continuer à vérifier.
            return False
    # return True — retourné après la boucle, uniquement si on a parcouru les 9 cases sans jamais trouver le chiffre. Il est donc absent de la ligne.
    return True

def chiffre_absent_colonne(grille, colonne, chiffre):
    #  Toutes les 9 cases, espacées de 9
    for i in range(9):
        if grille [i][colonne]== chiffre:
            return False
    return True

def chiffre_absent_bloc(grille, ligne, colonne, chiffre):
    # Trouver le coin supérieur gauche du bloc
    debut_ligne = (ligne // 3) * 3
    debut_colonne = (colonne // 3) * 3

    for i in range(debut_ligne, debut_ligne+3):
        for j in range(debut_colonne, debut_colonne+3):
            if grille[i][j] == chiffre:
                return False
    return True


def est_valide(grille, ligne, colonne, chiffre):
    return (chiffre_absent_ligne(grille, ligne, chiffre) and
            chiffre_absent_colonne(grille, colonne, chiffre) and
            chiffre_absent_bloc(grille, ligne, colonne, chiffre))
# def est_valide(grille, case, chiffre):
#     ligne = case // 9
#     colonne = case % 9
#     return (chiffre_absent_ligne(grille, ligne, chiffre) and chiffre_absent_colonne(grille, colonne, chiffre) and chiffre_absent_bloc(grille, case, chiffre))

def grille_valide(grille):
    """
    Vérifie que toute la grille respecte les règles du Sudoku.
    Utilisée par la force brute exhaustive pour valider une combinaison complète.
    """
    for i in range(9):
        for j in range(9):
            chiffre = grille[i][j]
            grille[i][j] = 0
            if not est_valide(grille, i, j, chiffre):
                grille[i][j] = chiffre
                return False
            grille[i][j] = chiffre
    return True