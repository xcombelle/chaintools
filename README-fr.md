**Attention the README-fr.md n'est qu'une traduction incomplète du README.md plus complet**

# Présentation

Le but de cette bibliothèque est de créer des outils type unix avec une syntaxe pythonique. Le seul mécanisme disponible est le pipeline

Un exemple d'utilisation

    chain(cat(),
          filter(lambda s: s and s[0] != '#'),
          map(float),
          sort(),
          head(n=10),
          output())

Le secret d'utilisation est d'une part la fonction `chain` qui fait un pipeline de générateur et les générateurs qui sont créés par des usines à générateur (que j'appelle outil). Plusieurs outils sont disponibles. Il est facile de créer sont propre outil.

# Statut

Cette bibliothèque est en pre-0.1. Il y aura donc probablement des changements.

# Pourquoi cette syntaxe

J'ai l'espoir d'avoir tous les pouvoir des outils unix d'une manière pythonique

Pourquoi tous les générateurs utilisent une notation de type fonction:

* une notation uniforme: pas de question sur les quels ont besoin de parenthèse ou pas 
* les générateurs font quelque chose

Je crois que les usine à générateur ont des caractéristiques correspondant aux outils unix comme les options (en utilisant les paramètre) les code d'erreur (en utilisant les exception). La seule partie manquante est la sortie d'erreur standard.

La principale différence est qu'il n'y a pas un processus par outil (sauf quand on lance un programme externe):
* Il n'y a pas de parallélisation native des outils
* Il n'y a pas besoin de créer un processus pour chaque outil

Un grand avantage des chaintools est que les type ne sont pas limités à des
flux d'octet. Par exemple les outil join et split n'ont pas d'équivalent (à ma
connaissance) parmi les outils unix.

# Qu'est-ce qu'on peut importer ?

On peut importer

    from chaintools import (
        chain,
        grep,
        sub,
        run,
        cat,
        output,
        split,
        sort,
        join,
        map,
        filter,
        head,
        tail,
        null,
    )

attention, cet import **remplace les builtins map et filter**.
