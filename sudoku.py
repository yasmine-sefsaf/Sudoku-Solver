from bruteforce import verif_grille_bruteforce
from backtracking import solve_sudoku
from grilles import (
    grille1_affichage, grille2_affichage, grille3_affichage,
    grille4_affichage, grille5_affichage
)
import time
import tracemalloc
import copy

class SudokuGrid:
    def __init__(self, numero_grille: int = 1):
        if numero_grille < 1 or numero_grille > 5:
            raise ValueError("Grille 1 à 5")
        self.numero = numero_grille
        self.affichage = self._choisir_affichage()
    
    def _choisir_affichage(self):
        return {
            1: grille1_affichage,
            2: grille2_affichage,
            3: grille3_affichage,
            4: grille4_affichage,
            5: grille5_affichage
        }[self.numero]
    
    def afficher_grille(self):
        """TON format exact"""
        for ligne in self.affichage:
            print(ligne)
    
    def _affichage_vers_9x9(self):
        """| _ 7 2 | → [[0,7,2,...]]"""
        grille = []
        for ligne in self.affichage:
            if "-------" not in ligne:
                row = [int(c) if c.isdigit() else 0 for c in ligne if c.isdigit() or c == '_']
                grille.append(row[:9])  # Sécurité 9 colonnes
        return grille
    
    def resoudre_backtracking(self):
        """ 1 = BACKTRACKING"""
        grille = copy.deepcopy(self._affichage_vers_9x9())
        print(f"\n=== BACKTRACKING - GRILLE {self.numero} ===")
        self.afficher_grille()
        
        tracemalloc.start()
        start_time = time.perf_counter()
        solved = solve_sudoku(grille)
        end_time = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        print(f"Temps : {end_time-start_time:.6f}s")
        print(f"Mémoire : {current/1024:.2f}Ko (max {peak/1024:.2f}Ko)")
        
        if solved:
            print("\n SOLUTION:")
            self._afficher_solution(grille)
        return solved
    
    def resoudre_forcebrute(self):
        """ 2 = FORCE BRUTE"""
        grille = copy.deepcopy(self._affichage_vers_9x9())
        print(f"\n=== FORCE BRUTE - GRILLE {self.numero} ===")
        self.afficher_grille()
        
        tracemalloc.start()
        start_time = time.perf_counter()
        solved = verif_grille_bruteforce(grille)
        end_time = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        print(f"Temps : {end_time-start_time:.6f}s")
        print(f"Mémoire : {current/1024:.2f}Ko (max {peak/1024:.2f}Ko)")
        
        if solved:
            print("\n SOLUTION:")
            self._afficher_solution(grille)
        return solved
    
    def _afficher_solution(self, grille_9x9):
        """9x9 → TON format"""
        for i, row in enumerate(grille_9x9):
            ligne = "| " + " ".join(map(str, row)) + " |"
            print(ligne.replace(" 0 ", " _ "))
            if i in [2, 5]:
                print("-----------------------")
