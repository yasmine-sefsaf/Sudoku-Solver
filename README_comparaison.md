# Sudoku-Solver


## Un résolveur de Sudoku en Python

### Comparaison des différents algorithmes

**1) Le backtracking**


**2) Le DLX**


**3) La force brute**   
Nous avons choisi de créer des variations autour de l'algorithme de force brute, afin de créer une sorte de progression dans les tentatives de résolution, et ce jusqu'à la plus rapide des résolutions (backtracking).

Comme soulevé dans l' autre document de synthèse (READAME_contexte.md), l'utilisation de deepcopy, nécessaire à l'application de certains algorithmes, représente une coût mémoire.   
Celui-ci est inhérent à l'architecture de cet algorithme. En effet, chaque tentative étant indépendante, une copie fraîche est nécessaire. C'est une limite structurelle par rapport au backtracking qui travaille en place.

**3.1) Bruteforce exhaustive**

Fonctionnement : remplissage des case de la valeur la plus basse autorisée, puis incrémentation de 1 à chaque tentatives.
Nombre de combinaisons possibles : 9⁴⁵ soit 8,73 *10⁴² solutions. 
ValeurCombinaisons à tester :8.73 × 10^42   Vitesse du PC : 42 517 551 combinaisons/heure   
Temps nécessaire : 2.05 × 10^35 heures soit2.34 × 10^31 années.   
Âge de l'univers : 1.38 × 10^10 années   
Ratio : 1.70 × 10^21 fois l'âge de l'univers
Résultat : aucune grilles résolue

Les valeurs sont identiques pour les 6 grilles : irresolvables dans le temps de vie humain 

