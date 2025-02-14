# Prise de note 14-02-2025:

Optimisation numérique 8 h = Preuve de l'unicité du minimum local en cas de stricte convexité. 


### Modèle épidémiologique SIR :

Répartitions compartimentaux : 
        - *S* pour les individus susceptible 
        - *I* infecter
        - *R* guerrie
        
Données Initiales : 
        - Proportions de chaque compartiment dans la population. 

Le modèle donne ensuite des règles expliquant comment sont modifiés ces pourcentages au fil du temps. 
    - A quelle vitesse un agent peut passer d'un compartiment a un autre. 


Dans notre cadre à nous, on rajouteras un 4e compartiment pour décès afin de représenter la faillite. 

#### *Les règles sont modéliser par un systeme d'équation différentielle.*

- dR/dt = cI
- dS/dt = -bI
- dI/dt = bIS - cI - mI
- dD/dt = mI

avec : 
 - m le taux de létalité
 - c taux de guerison
 - b force de contamination



Banque : 
  - Je souhaite avoir l'état des banques sur l'année 2011, peut être un peu plutôt pour analyser sur une certaine periode.
  
==> Banques Nationnales de chaque pays -> définir concretement( mathématiquement une banque nationnales affecter par un choc de prix {de maniere non negligeable} )

==> Comprendre la crise de l'euro ! finir un bouquin dessus, et trouve moi un moyen de trouver les données des banques. 
