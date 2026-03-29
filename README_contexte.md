# Sudoku-Solver


## Un résolveur de Sudoku en Python

### Présentation :

SUDOKU-SOLVER est un projet en Python qui permet tester des algorithme dans la perspective de résoudre des grilles de soduku.

A ce titre, deux algorithme sont proposés dans l'énoncé du projet : 
- le Backtracking
- Le bruteforce

#### Les conditions de présentation du projet : 
- Codage en python orienté objet
- Etude de la complexité algorithmique des méthodes de résolution choisies
- Affichage des statistiques de temps et de mémoire
- Prendre en entrée les grilles de Sudoku données dans le cadre de l'exercice  


#### Affichage :
le programme devra être affiché en terminal ainsi que via Pyagme.


### 1) Les algorithmes
Dans le contexte du sujet de l'exercice, il nous est demandé d'applliquer au minimum deux sortes d'algorithme : le bruteforce et le backtracking.

**1.a) Le bruteforce :** il s'agit de tester un nombre de combinaison dont le nombre est astronomiquement élevé. Le nombre de combinaison est lié aux nombre de cases vides. Soit k le nombre de cases vides, le calcul du nombre de combinaison est de 9 exposant k.
Par exemple dans le cas de 45 cases libres dans une grille de sudoku, le nombre de combinaison possible sera de 9 exposant 45, soit 8,73 * 10 exp 43 combinaisons. Le fonctionnement du bruteforce pure applique les règles APRES le remplissage de la grille.   
**Note** : Python est limité à 1000 appels récursifs imbriqués. Dans le contexte des limites à 100000 essais pour donner des stats intéressants, la récursivité n'aurait pas été pertinante.

**1.b) Le backtracking et la récursivité :** il s'agit de faire évoluer l'algorithme en lui permettant de corriger ses tentatives grâce à un retour en arrière, pour un nouvel essai dans les candidats possibles. De fait la suppression des combinaison liées au chiffres non candidats réduis drastiquement le nombre de combinaisons possibles. la récursivité intervient par l'appel de cette fonction par elle même : la condition d'arrêt est déterminée par la grille de sudoku remplie (plus de cases vides). La limite des 1000 appels est donc une limite qui n'est jamais atteint

**2) La complexité algorithmique**
Dans les deux cas, la complexité algorithmique est la suivante :  
Force brute exhaustive : O(9^k)  
Backtracking : entre O(k) et O(9^k) selon la grille   

**Le "coût en mémoire"** est, dans le contexte de  l'utilisation de variation de bruteforce (voir autre fichier README_comparaison) affecté par l'utilisation de deepcopy. En effet, il est nécessaire pour certains des algorithmes de créer une copie vide de la grille originale à chaque passe (récursivité) pour permettre que l'originale ne soit pas affectée. 

**3) Axes d'amélioration et veille technique**   
Le dlx, une approche liée à la théorie des graphes.

Interface joueur / machine : avec un timsleep adéquat et réglable,  un joueur pourrait jouer contre l'algorithme : le même grille serait proposée à un joueur et à l'algorithme, le premier qui fini sa grille a gagné.
Par ailleurs, la difficulté pourrait être réglée aussi sur le réglages des ressources allouées à l'algorithme, afin de "plafonner" sa vitesse.


