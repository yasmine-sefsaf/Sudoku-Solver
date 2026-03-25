from sudoku import SudokuGrid

while True:
    print("\n" + "="*40)
    print("SUDOKU SOLVER")
    print("="*40)
    print("1-6. Choisir une grille")
    print("0. Quitter")

    choix = input("\n👉 : ").strip()

    if choix == "0":
        print("Au revoir !")
        break

    try:
        numero = int(choix)
        sudoku = SudokuGrid("grilles.txt", numero)

        print("\nAlgorithme :")
        print("1. Backtracking")
        print("2. Force brute itérative (passes multiples)")
        print("3. Force brute exhaustive (toutes les combinaisons)")
        print("4. Force brute aléatoire avec mémoire")
        algo = input("\n👉 (1-3) : ").strip()

        try:
            if algo == "1":
                sudoku.resoudre('backtracking')
            elif algo == "2":
                sudoku.resoudre('bruteforce_iterative')
            elif algo == "3":
                sudoku.resoudre('bruteforce_exhaustive')
            elif algo == "4":
                sudoku.resoudre('bruteforce_aleatoire_memoire')
            else:
                print("Choix invalide")
        except KeyboardInterrupt:
            print("\nInterruption détectée — retour au menu")
            
    except FileNotFoundError:
        print("Fichier grilles.txt introuvable")
    except ValueError as e:
        print(f"Erreur : {e}")

    input("\nEntrée pour continuer...")