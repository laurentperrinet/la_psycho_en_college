# la_psycho_en_college
Introduction à la psychophysique en collège
===========================================

Une expérience utilisant http://www.psychopy.org pour mesurer son acuité visuelle en fonction de l'excentricité.



Pour les instructeurs:
----------------------

Il suffit :

 1. d'installer le programme PsychoPy depuis les instructions du site,
 2. de télécharger le fichier d'expérimentation (finissant par un ``.py``),
 3. d'ouvrir ce fichier à partir de ce programme (en utilisant la fonction *Ouvrir...* dans le menu *Fichier*,
 4. de le lancer en utilisant la fonction *Lancer* dans le menu *Outil*.

Contactez-nous (laurent.perrinet@univ-amu.fr et anna.montagnini@univ-amu.fr) en cas du moindre souci pour appliquer ces instructions.

Expérience eccentricité
-----------------------

Je propose de commencer par la première manip ("ophtalmo") qui a pour but de familiariser les étudiants avec les mesures psychophysiques en se concentrant sur l'analyse de l'acuité visuelle (donc de la capacité à reconnaitres de petits détails) à differents endroits du champs visuel (on parle de differente eccentricité et on mesure ça en degrés d'angle visuel). Cette manip est fortement liee a' une partie importante traitee dans votre livre de texte en SVT, c'est a' dire la composition non uniforme de la retine, avec beaucoup plus de recepteurs sensibles aux valiations de la lumiere dans l'espace (les cones) concentres dans la region centrale par rapport a' la peripherie. La reconnaissance de la lettre (entre E et 3) repose sur cette sensibilite' et elle est donc meilleure a' petite eccentricite'.

Pour passer l'expérience, chaque étudiant doit se mettre bien devant l'écran et se concentrer pendant toute la durée.  Au début il faut rentrer des infos à la main:
nombre d'essais par condition - > mettre 5 au minimum, mais si possible 10 (conseil faire une manip "pilote" avec 1 seul essai par condition pour se rendre compte de comment ça marche)
largeur de l'écran -> mettre la votre
distance de l'écran -> mettre la votre
repertoire de sauvegarde ... vous savez maintenant!

Après la manip: visualiser la feuille excel pour chaque étudiant
Pour évaluer l'acuité on trace des courbes psychométriques pour eventuellement en déduire un seuil de discrimination. Dans notre cas, pour une valeur d'eccentricité donnée (première colonne du fichier excel: valeurs 5, 10 ou 15 avec signe positif si à droite ou négatif si à gauche du centre) on calcule la fraction de réponses correctes (quatrième colonne et suivantes: 1=correct, 0=faux) en fonction de la taille de la cible (deuxième colonne:, cinq valeurs qui vont de 1 jusqu'à 2.828...).
En pratique les élèves devraient:
1) grouper les essais qui correspondent à une même eccentricité (en pratique, filtre sur la première colonne pour prendre 3 groupes avec: eccentricité=(+5 ou - 5) , (+10 ou - 10), (+15 ou - 15)) 
2) visualisation: valeurs ordonnées de taille de la lettre sur l'axe X ; moyenne des reponses (les 0 ert les 1 des colonnes résultats) correspondant à chaque valeur de taille - conseil utiliser des couleurs differentes pour les trois goupes correspondants aux trois valeurs d'eccentricité
3) tracer des courbes (fit) à travers les points: typiquement on utilise des gaussiennes cumulatives, mais une autre fonction raisonnable peut aller aussi (voir les exemples de courbe psychometrique sur internet, par ex:
http://www.google.fr/imgres?imgurl=http%3A%2F%2Fwebvision.med.utah.edu%2Fimageswv%2FKall04.jpeg&imgrefurl=http%3A%2F%2Fwebvision.med.utah.edu%2Fbook%2Fpart-viii-gabac-receptors%2Fpsychophysics-of-vision%2F&h=601&w=652&tbnid=-MwjAm68cgLGcM%3A&zoom=1&docid=1V4pJlXAqQ4BtM&ei=HXQJVcjHJMHzas-SgKAH&tbm=isch&iact=rc&uact=3&dur=2758&page=1&start=0&ndsp=19&ved=0CC0QrQMwBA): cette partie est plus compliquée et on pourra revenir la-dessus. Moi personellement, je ne sais pas faire des ajustement de fonctions aux donnees avec excel, mais on doit pouvoir trouver :-)
4) dependant de (3): estimer le seuil de discrimination de la lettre pour les trois eccentricites: le seul est definit comme la valeur de X (taille de la lettre) pour laquelle la probabilite' de donner une reponse correcte (Y dans notre figure) est egale a' 0.75.
