from regles import chiffre_absent_ligne, chiffre_absent_colonne, chiffre_absent_bloc

def verif_grille_bruteforce(grille):
    for i in range(9):
        for j in range(9):
            chiffre = grille[i][j]   # matrice 9x9

            # Si une case est vide, grille incomplète
            if chiffre == 0:
                return False

            # On exclut la case elle-même de la vérification
            # en vérifiant via les fonctions de regles.py
            # mais en retirant temporairement son chiffre
            grille[i][j] = 0
            valide = (chiffre_absent_ligne(grille, i, chiffre) and
                      chiffre_absent_colonne(grille, j, chiffre) and
                      chiffre_absent_bloc(grille, i, j, chiffre))
            grille[i][j] = chiffre   # on remet le chiffre

            if not valide:
                return False

    return True  # toutes les cases validées : grille résolue