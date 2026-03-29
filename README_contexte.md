# Sudoku-Solver


## Un résolveur de Sudoku en Python

### Présentation :

SUDOKU-SOLVER est un projet en Python qui permet tester des algorithme dans la perspective de résoudre des grilles de sudoku.

A ce titre, deux algorithme sont proposés dans l'énoncé du projet : 
- le Backtracking
- Le bruteforce

#### Les conditions de présentation du projet : 
- Codage en python orienté objet
- Etude de la complexité algorithmique des méthodes de résolution choisies
- Affichage des statistiques de temps et de mémoire
- Prendre en entrée les grilles de Sudoku données dans le cadre de l'exercice  


#### Affichage :
le programme devra être affiché en terminal ainsi que via Pygame.


### 1) Les algorithmes
Dans le contexte du sujet de l'exercice, il nous est demandé d'appliquer au minimum deux sortes d'algorithme : le bruteforce et le backtracking.

**1.a) Le bruteforce :** il s'agit de tester un nombre de combinaison dont le nombre est astronomiquement élevé. Le nombre de combinaison est lié aux nombre de cases vides. Soit k le nombre de cases vides, le calcul du nombre de combinaison est de 9 exposant k.
Par exemple dans le cas de 45 cases libres dans une grille de sudoku, le nombre de combinaison possible sera de 9 exposant 45, soit 8,73 * 10^42 combinaisons. Le fonctionnement du bruteforce pure applique les règles APRES le remplissage de la grille.   
**Note** : ici la récursivité n'est pas utile car une simple boucle <ins>**for**</ins> est suffisante.

**1.b) Le backtracking et la récursivité :** il s'agit de faire évoluer l'algorithme en lui permettant de corriger ses tentatives grâce à un retour en arrière, pour un nouvel essai dans les candidats possibles. De fait la suppression des combinaison liées au chiffres non candidats réduit drastiquement le nombre de combinaisons possibles. la récursivité intervient par l'appel de cette fonction par elle même : la condition d'arrêt est déterminée par la grille de sudoku remplie (plus de cases vides). La limite des 1000 appels est donc une limite qui n'est jamais atteinte car, avec au maximum 81 cases vides, il y aurait 81 appels en attente.

**2) La complexité algorithmique**
Dans les deux cas, la complexité algorithmique est la suivante :  
Force brute exhaustive : O(9^k)  
Backtracking : entre O(k) et O(9^k) selon la difficulté de la grille.

**Le "coût en mémoire"** est, dans le contexte de  l'utilisation de variation de bruteforce (voir autre fichier README_comparaison) affecté par  :    
- L'utilisation de deepcopy : en effet, il est nécessaire pour certains des algorithmes de créer une copie vide de la grille originale à chaque passe pour permettre que l'originale ne soit pas affectée.
- Mémorisation des combinaisons utilisées : utilisation importante de la mémoire dans les versions de bruteforce avec mémoire (aléatoire et exhaustive aléatoire).

**3) Axes d'amélioration et veille technique**   
Le dlx : c'est une approche par la transformation du sudoku et de ses contraintes en une matrice de 729 lignes (81 cases de 9 possibilités) et 324 colonnes (81 cases par 4 contraintes), remplies en grande majorité de zéros (dit "grille creuse")issus de la non-concordance des 4 règles du Sudoku). Dans cet espace, il y a 729 placements possibles, qui génèrent 4 "1" chacunes. Donc 2916 cases avec un "1". Les "1" représentent des noeuds, chaînés entre eux. 

**Interface joueur / machine :** avec un timsleep adéquat et réglable,  un joueur pourrait jouer contre l'algorithme : le même grille serait proposée à un joueur et à l'algorithme, le premier qui fini sa grille a gagné.
Par ailleurs, la difficulté pourrait être réglée aussi sur le réglages des ressources allouées à l'algorithme, afin de "plafonner" sa vitesse.


