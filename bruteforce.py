from regles import chiffre_absent_ligne, chiffre_absent_colonne, chiffre_absent_bloc

####### Vérification de la force brute
def verif_grille_bruteforce(grille):
    for case in range(81):
        chiffre = grille[case]

        # Si une case a zéro, grille fausse.
        if chiffre == 0:
            return False
        
        ligne = case // 9
        colonne = case % 9

        if not (chiffre_absent_ligne(grille, ligne, chiffre) and chiffre_absent_colonne(grille, colonne, chiffre) and chiffre_absent_bloc(grille, case, chiffre)):
            return False
    return True # Toutes les cases validée : grille résolue