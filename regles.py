def trouver_case_vide(grille):
    for i in range(9):
        for j in range(9):
            if grille[i][j] == 0:
                return (i, j)
    return None

def chiffre_absent_ligne(grille, ligne, chiffre):
    # Une ligne = 9 cases consécutives
    # La ligne 0 commence à l'index  0, la ligne 1 à l'index 9, etc.
    debut = ligne*9
    for i in range(debut, debut+9):
        if grille[i] == chiffre:
            # return False — retourné à l'intérieur de la boucle, dès qu'une case de la ligne contient déjà le chiffre cherché. On sort immédiatement, inutile de continuer à vérifier.
            return False
    # return True — retourné après la boucle, uniquement si on a parcouru les 9 cases sans jamais trouver le chiffre. Il est donc absent de la ligne.
    return True

def chiffre_absent_colonne(grille, colonne, chiffre):
    #  Toutes les 9 cases, espacées de 9
    for i in range(colonne, 81, 9):
        if grille [i]== chiffre:
            return False
    return True

def chiffre_absent_bloc(grille, case, chiffre):
    # Trouver le coin supérieur gauche du bloc
    ligne = (case // 9 // 3) * 3
    colonne = (case % 9// 3) * 3

    for l in range(ligne, ligne+3):
        for c in range(colonne, colonne+3):
            if grille[l*9+c] == chiffre:
                return False
    return True

def est_valide(grille, case, chiffre):
    ligne = case // 9
    colonne = case % 9
    return (chiffre_absent_ligne(grille, ligne, chiffre) and chiffre_absent_colonne(grille, colonne, chiffre) and chiffre_absent_bloc(grille, case, chiffre))
