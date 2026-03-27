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
Par exemple dans le cas de 45 cases libres dans une grille de sudoku, le nombre de combinaison possible sera de 9 exposant 45, soit 8,73 * 10 exp 43 combinaisons. Le fonctionnement du bruteforce pure applique les règles APRES le remplissage de la grille

**1.b) Le backtracking :** il s'agit de faire évoluer l'algorithle en lui permettant de corriger ses tentatives grâce à un retour en arrière, pour un nouvel essai dans les candidats possibles. De fait la suppression des combinaison liées au chiffres non candidats réduis drastiquement le nombre de combinaisons possibles.

**2) La complexité algorithmique**
Dans les deux cas, la complexité algorithmique est la suivante :  
Force brute exhaustive : O(9^k)  
Backtracking : entre O(k) et O(9^k) selon la grille   
Le "coût en mémoire" est, dans le contexte de  l'utilisation de variation de bruteforce (voir autre fichier README_comparaison) est affecté par l'utilisation de deepcopy. En effet, il est nécessaire pour certains des algorythme de créer une copie vide de la grille original

Note



