import copy
import time
import tracemalloc

from bruteforce import resoudre_force_brute_iterative, resoudre_force_brute_exhaustive, bruteforce_aleatoire_memoire, bruteforce_exhaustif_aleatoire_memoire
from backtracking import resoudre_backtracking


class SudokuGrid:

    def __init__(self, chemin: str, numero: int):
        self.grille = self._lire_fichier(chemin, numero)

    # ------------------------------------------------------------------
    # PARSING
    # ------------------------------------------------------------------

    def _lire_fichier(self, chemin, numero):
        """
        Lit la grille numéro 'numero' dans grilles.txt.
        Les grilles sont séparées par '---'.
        Les cases vides sont représentées par '_'.
        """
        with open(chemin, 'r') as f:
            contenu = f.read()

        blocs = contenu.strip().split('---')

        if numero < 1 or numero > len(blocs):
            raise ValueError(f"Grille {numero} inexistante — fichier contient {len(blocs)} grilles")

        bloc = blocs[numero - 1].strip()
        grille = []
        for ligne in bloc.splitlines():
            ligne = ligne.strip()
            if not ligne:
                continue
            row = [int(c) if c.isdigit() else 0 for c in ligne]
            if len(row) == 9:
                grille.append(row)

        if len(grille) != 9:
            raise ValueError(f"Grille {numero} invalide : {len(grille)} lignes trouvées")

        return grille

    # ------------------------------------------------------------------
    # AFFICHAGE
    # ------------------------------------------------------------------

    def afficher(self, grille=None, originale=None):
        """
        Affiche la grille dans le terminal.
        Les chiffres ajoutés par l'algorithme sont affichés entre crochets.
        """
        if grille is None:
            grille = self.grille
        print()
        for i, row in enumerate(grille):
            if i in [3, 6]:
                print("---------+----------+---------")
            ligne = ""
            for j, val in enumerate(row):
                if j in [3, 6]:
                    ligne += "| "
                if val == 0:
                    ligne += "_  "
                elif originale and originale[i][j] == 0:
                    ligne += f"[{val}]"  # chiffre ajouté
                else:
                    ligne += f"{val}  "
            print(ligne)
        print()

    # ------------------------------------------------------------------
    # RÉSOLUTION
    # ------------------------------------------------------------------

    def resoudre(self, methode: str):
        if methode not in ('backtracking', 'bruteforce_iterative', 'bruteforce_exhaustive', 'bruteforce_aleatoire_memoire', 'bruteforce_exhaustif_aleatoire_memoire'):
            raise ValueError("methode invalide")

        grille_travail = copy.deepcopy(self.grille)
        originale = copy.deepcopy(self.grille)
        solved = False
        stats_exhaustive = None
        stats_aleatoire = []

        print(f"\n=== {methode.upper()} ===")
        print("Grille de départ :")
        self.afficher()

        tracemalloc.start()
        debut = time.perf_counter()
        nb_operations = [0]
        try:
            if methode == 'backtracking':
                solved = resoudre_backtracking(grille_travail, nb_operations)
            elif methode == 'bruteforce_iterative':
                solved = resoudre_force_brute_iterative(grille_travail)
            elif methode == 'bruteforce_aleatoire_memoire':
                solved, tentatives, nb_stockees = bruteforce_aleatoire_memoire(grille_travail, stats=stats_aleatoire)
                stats_aleatoire = (tentatives, nb_stockees)
            elif methode == 'bruteforce_exhaustif_aleatoire_memoire':
                solved, tentatives, nb_stockees = bruteforce_exhaustif_aleatoire_memoire(grille_travail, stats=stats_aleatoire)
                stats_aleatoire = (tentatives, nb_stockees)
            else:
                solved, combinaisons, total = resoudre_force_brute_exhaustive(grille_travail)
                stats_exhaustive = (combinaisons, total)

        except KeyboardInterrupt:
            pass

        finally:
            # S'exécute toujours — interruption ou pas

            print("résultat : ")
            self.afficher(grille_travail, originale)
            fin = time.perf_counter()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            print("\nStats :")
            print(f"\nTempss   : {fin - debut:.6f}s")
            print(f"Mémoire : {current/1024:.2f} Ko (pic : {peak/1024:.2f} Ko)")
            
            if methode == 'backtracking':
                print(f"Nb opérations : {nb_operations[0]:,}")
            elif methode in ('bruteforce_aleatoire_memoire', 'bruteforce_exhaustif_aleatoire_memoire'):
                if stats_aleatoire:
                    print(f"Tentatives            : {stats_aleatoire[0]:,}")
                    print(f"Combinaisons stockées : {stats_aleatoire[1]:,}")
                else:
                    print("Interrompu avant la première tentative")

            if not solved:
                if stats_exhaustive:
                    combinaisons, total = stats_exhaustive
                    print(f"Combinaisons testées : {combinaisons:,}")
                    print(f"Total possible       : {total:.2e}")
                    print(f"Progression          : {combinaisons/total*100:.8f}%")
                    print("Attention : Grille non résolue complètement")
                    
        return solved, grille_travail