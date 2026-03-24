from sudoku import SudokuGrid

while True:
    print("\n" + "="*50)
    print("🎮 SUDOKU SOLVER")
    print("="*50)
    print("1. Grille 1")
    print("2. Grille 2")
    print("3. Grille 3")
    print("4. Grille 4")
    print("5. Grille 5")
    print("0. Quitter")
    
    choix_grille = input("\n👉 Choisir grille (0-5) : ").strip()
    
    if choix_grille == "0":
        print(" Au revoir !")
        break
    
    try:
        numero_grille = int(choix_grille)
        sudoku = SudokuGrid(numero_grille)
        
        # 2️ AFFICHE SEULEMENT LA GRILLE CHOISIE
        print(f"\n GRILLE {numero_grille} SÉLECTIONNÉE")
        sudoku.afficher_grille()
        
        # 3️ CHOISIR L'ALGO
        print("\n🔧 ALGORITHMES")
        print("1. Backtracking (rapide)")
        print("2. Force Brute (lent)")
        choix_algo = input("\n Choisir algo (1-2) : ").strip()
        
        numero_algo = int(choix_algo)
        sudoku.resoudre(numero_algo)
        
    except ValueError:
        print(" Erreur : tape 1-5 pour grille, 1-2 pour algo")
    except Exception as e:
        print(f" Erreur : {e}")
    
    input("\n  Appui Entrée pour continuer...")
