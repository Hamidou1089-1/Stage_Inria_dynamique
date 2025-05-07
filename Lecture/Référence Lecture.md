


Alors comment je me place dans la litterature, 
J'essaie de reproduire le model d'eisenberg et NOE pour simuler une crise par la contagion a travers les canaux de dette. 



Le model d'eisenberg et noe est l'un des premiers model (peut etre le premier meme) qui a modeliser les banques et les relations qui les lis, avec un reseau où les liens c'est les obligations d'une banque a une autre.
Elle fournit un algorithme qui permet en cas de default d'une banque d'avoir un vecteur de payements (si chaque banque fais default, on fait une simulation ou a chaque incrément on regarde si une banque fais default, il paye ce qu'il doit et on regarde si avec ce payement de nouvelle banque sont en default, puis on passe a l'etape d'apres, jusqu'a ne plus avoir de nouvelle banque en default)

# Introduction
Le risque systemic depuis la crise 2007-2009 est devenu un sujet essentiel dans le domaine de la finance et pour la recherche en finance.
Le risque systemic c'est le risque d'effondrement du systeme financier, une proportion importante de banque d'un pays en default pouvant mener a une crise fatal que ce soit au niveau economique que politique et social. C'est un sujet important a comprendre et a quantifié. 
Ainsi cet etude ce situe entre l'informatique et la theorie de probabilité avec la theorie graphe appliqué à la finance, on cherche a quantifier la robustesse/resillience d'un réseau interbancaire à different shock. 
Pour cela on se base sur le modele d'Eisenberg et Noe (reference precis à l'article). 
Après avoir assimiler le model, on fait une implémentation avec une architecture MVC en python pour faire des simulations sur le reseau interbancaire. 

Enfaite on veut tirer des informations du reseau interbancaire modeliser a travers les dettes, chaque noeud a des attribut (un bilan simplifié, actif passif, dette interieur et exterieur et actif interieur et exterieur.
A partir de cette modelisation du reseau interbancaire, on se demande plusieur chose, est ce que cette structure de lien est resiliente a certain shock (un élément exterieur qui est un actif exterieur qui n'est pas remboursé dans la totalité). Est ce qu'il existe une structure de reseau resiliente ou du moins qui minimise quelque soit l'ampleur du shock. Comment modeliser ce shock pour voir l'impact dans la réalité ? 
Toute ces questions sont à la base de ce domaine de recherche qui est la contagion dans un reseau financier. 
Chaque chercheur du domaine change soit de granularité sur les hypotheses (une hiearchie des obligations, une difference dans les prix en actifs, un bilan plus complexe -> les banques n'ont pas que des actifs a travers des dettes, mais ils investissent également (meme si on peut mettre cela sur le compte des actifs exterieur et passif exterieur)), soit change la maniere de modeliser les relations, soit un reseau, ou autre chose (faut trouvé, y'avait le mean field que j'avais lu qui est equivalent mais j'ai pas approfondie plus que ca). 

Et donc un aspect important de cette structure est la densité du reseau, car on "observe aujourd'hui" que les reseaux interbancaire sont tres denses. 
Or la dépendance d'une banque au remboursement de credit quel a faite détermine enormement la solvabilité de son bilan. 

Un reseau dense actif diversifier des banques, dilue t'il un shock de remboursement ? ou bien y a t il un seuil où cette densité permet de diluer et ensuite amplifie la contagion de non remboursement ? 

Nous on va s'interesser a ces question dans cet article, quel est ce seuil ? dans quel cas il existe ? 
La theorie de formation de reseau est un domaine qui nous servira pour fixer un reseau qui se rapproche le plus de la réalité, et faire varier sa densité 

Ce que le model d'eisenberg nous apporte, c'est de resourdre le vecteur de payement du a l'aspect cyclique des reseau financier : Je te dois 10€ mais je n'ai plus que 5€ tu dois 11€ a un autre mais tu n'auras plus que 6€ or lui il me devait 6€, ainsi on voit la un probleme de payement cyclique. Le model d'eisenberg et Noe apporte une solution de payement. 

Peter Young permet justement d'utiliser cela pour l'appliquer et mesurer donc la robustesse d'un reseau financier. 

On se place du meme point de vue que Young, et on simplifie certaine methode mise en place pour mesurer cette robustesse. 

## Contexte de recherche : 
- Importance du risque systemic
- Eisenberg Noe -> Systemic Risk in Financial Systems : Premier article sur la contagion sur les reseaux financiers
- Peter Young ->  Contagion in Financial Networks : Article qui complete 


# Banaliser pour faire une introduction qui donne envie

J'ai un peu fais ca juste avant. 



# Coeur techniques
On considere d'abord l'article d'eisenberg et Noe qui formalise 




>  # Relecture d'article 
>  - Eisenberg & Noe

    Default in a single clearing mechanism
    Obligations determined simultaneously with priority of **debt claims** and **Limited liability of equity** (un Noeud ne paye pas plus que ses resources)
    Via a *Fixed-Point argument* there always exits a **Clearing payment vector** that clears the obligations of the members of the clearing system
    Under *Mild refularity conditions* that clearing vector is *Unique*
    The algorithm developed by the paper both clears the **Financial system** and provides information on *the systemic risk faced by individual system firms*
    
**The value of most firms is dependent on the payoffs they receive from their claims on other firms. The value of these claims depends, in turn, on the financial health of yet other firms in the system.**
*Moreover, linkages between firms can be cyclical*
example:
**A default by Firm A on its obligations to Firm B may lead B to default on its obligations to C.A default by C may, in turn, have a feedback effect on A.**

This illustrates a geenral feature of financial system architectures : *cyclical interdependence*


debt : dette creancier
equity : parts des actionnaires
priorité : debt > equity

This clearing vector can be
computed through a *"fictitious sequential default"*
algorithm. Moreover, the algorithm corresponds to a
*process of dynamic adjustment* in which the *set of defaulting firms* at the **start** of each round is fixed by
the adjustments of the system in the previous round.
In each *new round*, an **attempt is made to clear** the
system **assuming that only nodes that defaulted in the last round default**. *If, in fact, no new defaults occur*,
the *algorithm terminates*. **Otherwise**, the *new wave* of
*defaults is recorded and the process is iterated again.*



This algorithm, as well as quickly yielding the clearing
vector, produces a natural *measure of systemic risk*-
**the exposure of a given node in the system to defaults by other firms**. This *measure of systemic risk* is **based**
on *how many "waves" of defaults are required to induce a given firm in the system to fail.*

C'est la *Methode comparative statique*
Dans ce papier, on analysent specifiquement comment le vecteur de compensation d'équilibre change quand:
    - Le flux de tresorie operationnels changent
    - La structure des obligations financieres entre les noeuds change
    - les niveaux d'obligations nominales changent.
    

Resultat de la domiannce stochastique de second ordre:

le papier donne un resultat : 
le vecteur de compensation d'equilibre (*Vecteur de paiement d'equilibre*) est fonction concave des flux de tresorie operationnels et du vecteur des obligations nominales. 


*une interpretation de $\phi$ (fonction du vecteur p, matrice relative de payement, vecteur de payement du, et des actif exterieur) represente les fonds a utiliser pour satisfaire les obligations de dettes en assumant la reception des payements promis.*



PLan :


# Tous ceci c'est l'intro
Intro :
- Colaboration ? Inria  & Gips-Lab, Nicolas gast, Hamidou, Federica, Paolo, --
- Faire une présentation du risque systemique,--
    -> la definir comme un indicateur de crise assez parlant.--
- faire une présentation rapide de la modelisation, --
- pourquoi un reseau ? pourquoi le risque systemique ?  -> les cycles, probleme de payements en cas de défaut.--
- Poser la problématique : seuil de diversification vs amplification 
- qu'est ce qui a deja été effectuer sur le sujet ? == prochaine question
- y a til d'autre approches pour repondre a la problematique ? 
    -> Etat de l'art :
    On utilise trois papiers de recherche principalement, mais c'est un domaine de recherche tres dense, ainsi on peut tres facilement trouver des article differents de ces choix. 
    - Pour le probleme de payement, l'algorithme d'Eisenberg et Noe nous permettra de determiner le vecteur de payements d'equilibre. 
    - Peter Young et Glasserman nous permettrons de formaliser la contagion financière, et on adoptera ces notations, 
    - Le papier qui permet de faire une ouverture avec le papier de pter young. 

-> Un aspect de contribution, on discutera plus de ce que papier nous a apporté que ce qu'on a apporté. 
- En quoi ce papier apporte quelque chose de nouveau ? 
- qu'elles sont les resultats obtenu ? 
- comment interpreter ces resultats ? 
- Répondent elle a la question ? 
- On annonce le plan ensuite. 




# Coeur technique
Méthodologie et l'aspect technique:
On va en profiter pour poser le probleme plus rigoureusement, 
definir un reseau financier dans notre cas, exprimer les propriétés les plus simple du reseau, en faire des preuves, puis formuler dans une certaine extension des definitions et propriété, la problematique po justifier notre approche.

- On formalise un reseau, comme un graphe
- On formalise comment on genere ce graphe ?
- Pourquoi ce choix simplificateur ?
- ensuite dans ce graphe le choix des poids ? 
- Comment on fait pour les isoler ? pour essayer de reduire leur impact sur la contagion, meme si c'est presqu'impossible
- Faire un tableau pour decrire l'entité banque
- Ensuite on presente le choix du simulateur ? quel langage ? quel paradigme
- Pourquoi simuler d'ailleur ? c'etait pas possible de faire des calculs rapide qu'on pouvait extrapoler ? 
- Conclure sur cette approche, la comparer à l'etat de l'art. 




Résultats
ON est dans le cas ou la croissance du choc est linéaire, ainsi c'est un cas où on part du principe le choc est exogène, on ne s'interesse pas à la probabilité que cela ce produise, mais on part du principe que cela ce produit.

1. Dans un graphe non connexe ( non connecter ) on ne voit pas de phenome de dilution ou d'amplification, ainsi pour un choc lineaire, le default 
- expliqué les mesures mise en place pour le plot, les parametres, expliqué le choix des parametres economiquement parlant, et traduire le resultat concretement. 

On aura plusieurs figure : 

- Avoir un graphe complet, et un graphe pas connecter: discuter de cela, :
Traduire economique ceque cela signifie, est ce realiste ? 

- Une forme de simulation de monte carlo pour ->
Ensuite trouvé pour un graphe connecter, le seuil d'interconnexion le plus optimale. 

Discussion : 
L'ouverture sera justement une critique de mon approche, qui pour moi n'est pas complêt sur beaucoup d'aspect, comme par exemple dans le papier de Peter young (Financial contagion) on sait que il ya tout une etude pour savoir quel parametre est le plus significatif pour decrire le risque systemique, enfaite il ya meme plusieur parametre qui intervienne, et chacun permet de decrire avec une meilleure precision le risque systemique. 

Conclusion: 
On va resumer le papier avec la disvusion, etc etc
Dans la conclusion on va parler de la suite qu'on developpera, et quel implementation on fera dessus etc. 











j'assume trop de truc:

diversifié, si je le vois comment le reconnaitre ? 

Cas ou le choc est ciblé:

    un choc a été diversifié si pour un choc x sur R (ie C - x entry wise) le rayon de default engendré par le choc ne depasse pas un certain seuil, 
    Il ya plusieur niveau de diversification, 

    Niveau 0: Notre defaut se limite a nous
    Niveau 1: ========== plus court chemin = 2
    ....
    Niveau n; =======================   = n +1
    
Si le choc est exogène:

    Un choc exogène a été diversifié 


On voit la dilution de maniere temporelle ou par la proportion de default ? 
plusieur parametre peuvent infuencer cet effet de dilution, la presence de cycle court et long, l'aspect etoile d'un reseau peut mener a un effet d'accumulation qui mene a une amplification

mais meme l'amplification, comment le definir, 

je rentre un choc x, on dit que le reseau amplifie x si 
la dependance, la presence de cycle est l'amplification:
A doit 100 B, B doit 100 a C et C doit 100 a A, A ne peut plus rembourser la totalité de sa dette a B disons elle ne peut rembourser que 50, mais ce 50 prenait en compte le fait de recevoir 100 de C, ainsi un choc de 50, ce fait amplifier par ce cylce de dependance. 

Maintenant pour les meme raison, on va ilustrer l'effet inverse, la dilution, puisque la dilution c'est cet effet contraire, disons si A ne peut plus rembourser son du, que son default n'engendre pas une sequence de baisse de payement pour tous le monde










