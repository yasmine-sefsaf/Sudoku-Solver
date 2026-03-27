# Sudoku-Solver


## Un résolveur de Sudoku en Python

### Comparaison des différents algorithmes

**1) Le backtracking**


**1.a) Le Backtracking classique**


**1.b) Le backtracking amélioré**


**3) La force brute**   
Nous avons choisi de créer des variations autour de l'algorithme de force brute, afin de créer une sorte de progression dans les tentatives de résolution, et ce jusqu'à la plus rapide des résolutions (backtracking).

Comme soulevé dans l' autre document de synthèse (READAME_contexte.md), l'utilisation de deepcopy, nécessaire à l'application de certains algorithmes, représente une coût mémoire.   
Celui-ci est inhérent à l'architecture de cet algorithme. En effet, chaque tentative étant indépendante, une copie fraîche est nécessaire. C'est une limite structurelle par rapport au backtracking qui travaille en place.

**3.1) Bruteforce exhaustive**

Fonctionnement : remplissage des case de la valeur la plus basse autorisée, puis incrémentation de 1 à chaque tentatives. Les règles du Sudoku soont appliquées sur la grille remplie.   
Dans ce contexte, nous avons implémenté une condition d'arrêt à 100000 (cent mille) tentatives.  
Nombre de combinaisons possibles pour 45 cases : 9⁴⁵ soit 8,73 *10⁴² solutions. 
ValeurCombinaisons à tester :8.73 × 10^42   Vitesse du PC : 42 517 551 combinaisons/heure   
Temps nécessaire : 2.05 × 10^35 heures soit2.34 × 10^31 années.   
Âge de l'univers : 1.38 × 10^10 années   
Ratio : 1.70 × 10^21 fois l'âge de l'univers
Résultat : aucune grille résolvable.   


Voici un exemple avec un temps de 2020 secondes, soit un peu plus de 33 minutes : 
![Exemple pour 2020 secondes](images/Iteration_bruteforce.jpg)   

Les valeurs sont identiques pour les 6 grilles, elles sont irresolvables dans le temps humain :

![Tableau récapitulatif pour les 6 grilles](images/Tableau_comparatif_grilles_bruteforce.jpg)   


**3.2) Bruteforce exhaustive aléatoire à mémoire**
Le principe de cet algorithme est le même que le précédent, à savoir le test de toutes le combinaisons possibles.
Cependant, à la différence de bruteforce exhaustive, les combinaisons sont tirées au hasard et mises en mémoire afin de ne pas être réutilisées lors du test de validation (qui n'a jamais rêvé de gagner au loto?) 

Exemple :    
![Stats pour 100000 tentatives](images/bruteforce_aleatoire_memoire.jpg)


**3.3) Bruteforce aléatoire à mémoire**
Le principe de cet algorithme est de tester toutes les combinaisons possibles, celles ci étant uniquement constituées des candidats possibles pour chaque cases.
Il peut y avoir de grandes différences de temps  de traitement, de relativement courrt à impossible. ceci est différencié par la complexité exponentielle : plus il y  a de cases vides et plsu le nombre de candidats possibles sont élevés, plus le temps de résolution est grand.   

![Comparaison grille 3 et 4](images/Comparatif_griles_3_4.jpg)


