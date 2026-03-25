def compte_a_rebours(n):
    #11. La condition d'arrêt
    if n<=0:
        print("Décollage!")
        return #on arrête tout la fonction est terminée
    
    # L'actioin et l'appel récursif
    else :
        print(n)
        compte_a_rebours(n-1)

#On lance : 
compte_a_rebours(100)