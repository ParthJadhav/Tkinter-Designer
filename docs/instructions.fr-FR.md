# Comment utiliser Tkinter Designer

#### Traductions:
- [简体中文](/docs/instructions.zh-CN.md)
- [English](/docs/instructions.md)
- [Français](/docs/instructions.fr-FR.md)

___

## Sommaire:
1. [**Commencer**](#commencer-haut)
   1. [Installer Python](#getting-started-1)
   2. [Installer Tkinter Designer](#getting-started-2)
   3. [Créer un compte Figma](#getting-started-3)
   
2. [**Formater votre design Figma**](#formater-votre-design-figma-haut)
   1. [Référence](#formatting-1)
   2. [Guide des éléments](#formatting-2)
   
3. [**Utiliser Tkinter Designer**](#utiliser-tkinter-designer-haut)
   1. [Clé d'accès personnelle](#using-1)
   2. [URL du fichier](#using-2)
   3. [Tester votre code généré](#using-3)
   
4. [**Diagnostic des anomalies**](#diagnostic-des-anomalies-haut)

<br><br>

# Commencer <small>[[Haut](#Sommaire)]</small>

<a id="getting-started-1"></a>
## 1. Installer Python
Avant d'utiliser Tkinter Designer, vous devez installer Python.
* [Voici un lien vers la page de téléchargement de Python.](https://www.python.org/downloads)  
* [Voici un guide utile pour installer Python sur divers systèmes d'exploitation.](https://wiki.python.org/moin/BeginnersGuide/Download)

*Plus loin dans ce guide, vous utiliserez le programme d'installation de packages pour Python (pip), ce qui peut vous obliger à ajouter Python à votre PATH système.*

___
<br>

<a id="getting-started-2"></a>
## 2. Installer Tkinter Designer
Une fois Python installé, vous pouvez télécharger Tkinter Designer depuis le [dépôt officiel](https://github.com/ParthJadhav/Tkinter-Designer).

Dans la barre latérale de droite, cliquez sur la dernière version et, sous **Assets**, choisissez `tkinter_designer.exe`. Une fois l'exécutable téléchargé, vous êtes prêt à exécuter le programme !

*Pour exécuter Tkinter Designer à partir du code source, suivez les instructions ci-dessous.* 

1. Téléchargez les fichiers sources de Tkinter Designer 

2. Décompressez les fichiers source dans un répertoire de votre système
   
3. Ouvrez un terminal/invite de commande dans ce répertoire
   * Vous pouvez accéder à ce dossier à l'aide de la commande `cd`.
   * Vous pouvez également utiliser un IDE avec un terminal intégré, tel que [Visual Studio Code](https://code.visualstudio.com/).

4. Installez les dépendances nécessaires en exécutant `pip install -r requirements.txt`
   * Si pip ne fonctionne pas, essayez également les commandes suivantes :
     * `pip3 install -r requirements.txt`
     * `python -m pip install -r requirements.txt`
     * `python3 -m pip install -r requirements.txt`
   * Si cela ne fonctionne toujours pas, assurez-vous que Python est ajouté au PATH.
  
5. Vous pouvez lancer Tkinter Designer en exécutant `python tkinter_designer.py`

___
<br>

<a id="getting-started-3"></a>
## 3. Créer un compte Figma
1. Dans un navigateur web, rendez-vous sur [figma.com](https://www.figma.com/) et cliquez sur 'Sign up'
2. Entrez vos informations, puis vérifiez votre email
3. Créez un nouveau fichier de design Figma
4. Commencez à créer votre interface graphique
   * La section suivante couvre le formatage requis pour l'entrée de Tkinter Designer.
     * [Série officielle de tutoriels Figma pour les débutants](https://www.youtube.com/watch?v=Cx2dkpBxst8&list=PLXDU_eVOJTx7QHLShNqIXL1Cgbxj7HlN4)
     * [Chaîne YouTube officielle Figma](https://www.youtube.com/c/Figmadesign/featured)
     * [Centre d'aide Figma](https://help.figma.com/hc/en-us)

<br><br>

# Formater votre design Figma <small>[[Haut](#Sommaire)]</small>

<a id="formatting-1"></a>
## 1. Référence
<br>

### L'importance du nom

| Nom de l'élément Figma | Élément Tkinter |
| --- | --- |
| Button | Button |
| Rectangle | Rectangle |
| TextArea | Text Area |
| TextBox | Entry |
| Background | Canvas.Image() |

<br>

Le code généré par Tkinter Designer est basé sur les noms des éléments de votre design Figma et, en tant que tel, vous devez nommer vos éléments en conséquence. Dans Figma, renommez vos éléments en double-cliquant dessus dans le panneau Calques.

___
<br>

<a id="formatting-2"></a>
## 2. Guide des éléments
<br>

1. **Tout d'abord, créez une Frame qui servira de fenêtre Tkinter.**
<br><br>

2. **Créer un arrière-plan**
    * Les arrière-plans peuvent être créés à l'aide de formes et/ou d'images
    * Si vous utilisez plusieurs formes/images, vous devez les regrouper en les sélectionnant toutes et en appuyant sur <kbd>CTRL/&#8984; + G</kbd>
    * <br><br>

3. **Texte (Texte normal)**
   * Utilisez la touche <kbd>T</kbd> pour activer l'outil texte, puis ajoutez du texte comme vous le souhaitez
   * Le texte n'a pas besoin d'être renommé pour être utilisé dans Tkinter Designer
   * Appuyez explicitement sur la touche <kbd>Retour</kbd> ou <kbd>Entrée</kbd> pour passer à la ligne suivante.
<br><br>

4. **Entrée de texte (Entrée utilisateur sur une seule ligne)**
   * Activez l'outil Rectangle avec <kbd>R</kbd>
   * Ajustez le rectangle à votre convenance
   * Assurez-vous que le rectangle est nommé "TextBox" 
<br><br>

5. **Zone de texte (Entrée utilisateur sur plusieurs lignes)**
   * Activez l'outil Rectangle avec <kbd>R</kbd>
   * Ajustez le rectangle à votre convenance
   * Assurez-vous que le rectangle est nommé "TextArea"

6. **Rectangle**
   * Activez l'outil Rectangle avec <kbd>R</kbd>
   * Ajustez le rectangle à votre convenance
   * Assurez-vous que le rectangle est nommé "Rectangle"
<br><br>

7. **Bouton normal**
   * Ajouter un rectangle pour servir de bouton dans votre interface graphique
     * Facultatif : ajoutez du texte au bouton
   * Sélectionnez le bouton (Rectangle) et tout texte facultatif, puis regroupez-les avec <kbd>CTRL/&#8984; + G</kbd>
   * Nommez le groupe "Button"

#### Référez vous à [cette vidéo](https://youtu.be/mFjE2-rbpm8?t=275) si vous rencontrez tout problème

<br><br>

8. **Bouton arrondi** 
   * Ajouter un rectangle pour servir de bouton dans votre interface graphique
     * Facultatif : ajoutez du texte au bouton
   * Arrondissez-le en ajoutant un rayon d'angle en sélectionnant le rectangle et en ajoutant un rayon d'angle à partir du côté droit. [En savoir plus](https://help.figma.com/hc/en-us/articles/360050986854-Adjust-corner-radius-and-smoothing)
   * Créez un rectangle avec la même taille de votre bouton. Ne l'arrondissez pas.
   * Changez la couleur du rectangle pour qu'elle corresponde à l'arrière-plan
   * Déplacez maintenant le rectangle nouvellement créé sous le bouton principal (Rectangle).
   * Sélectionnez le bouton (Rectangle) et tout texte facultatif, puis regroupez-les avec <kbd>CTRL/&#8984; + G</kbd>
   * Nommez le groupe "Button"

#### Référez vous à [cette vidéo](https://youtu.be/mFjE2-rbpm8?t=275) si vous rencontrez tout problème

<br><br>

# Utiliser Tkinter Designer <small>[[Haut](#sommaire)]</small>

### Ouvrez Tkinter Designer avant de suivre les étapes suivantes.
<br>

<a id="using-1"></a>
## 1. Clé d'accès personnelle
1. Connectez-vous à votre compte Figma
2. Accédez à Paramètres
3. Dans l'onglet **Compte**, faites défiler jusqu'à **Personnal access tokens**
4. Saisissez le nom de votre clé d'accès dans le formulaire de saisie et appuyez sur <kbd>Entrée</kbd>
5. Votre clé d'accès personnelle sera créé.
    * Copiez cette clé et conservez-la dans un endroit sûr.
    * **Vous n'aurez pas d'autre chance de copier cette clé.**
6. Collez votre clé d'accès personnelle dans le formulaire **Token ID** dans Tkinter Designer
___
<br>

<a id="using-2"></a>
## 2. URL du fichier
1. Dans votre fichier de conception Figma, cliquez sur le bouton **Partager** dans la barre supérieure, puis cliquez sur **&#x1f517; Copier le lien**
2. Collez le lien dans la zone **File URL** au sein de Tkinter Designer
___
<br>

<a id="using-3"></a>
## 3. Tester votre code généré
1. In Tkinter Designer, cliquez sur la zone **Output Path** pour ouvrir l'explorateur de fichier
2. Choisissez le chemin de sortie et cliquez **Select Folder**
3. Appuyez sur **Generate**

Les fichiers de sortie de Tkinter Designer seront placés dans le répertoire de votre choix, dans un nouveau dossier appelé **generated_code**. Félicitations, vous avez maintenant créé votre interface graphique Tkinter à l'aide de Tkinter Designer !

<br><br>

# Diagnostic des anomalies <small>[[Haut](#sommaire)]</small>

* Éléments non visibles ? Mal placés ?
  * Veuillez vous assurer que votre Frame de niveau supérieur est positionné avec ses coordonnées X et Y à (0, 0) 
    * Vérifiez la barre latérale droite, sous **Design**

* Le bouton a un arrière-plan gris non désiré ?
  * Assurez-vous que vous avez ajouté un rectangle derrière votre élément de bouton et que sa couleur de remplissage est la même que celle de l'arrière-plan

* Éléments incorrects ?
  * Assurez-vous d'avoir nommé correctement vos éléments dans Figma
    * Se référer à [Formater votre design Figma, &sect;1](#formatting-1)

* La fenêtre est plus grande que l'écran ?
  * Réduisez la taille de vos éléments dans Figma

* Les fichiers ne se génèrent pas ?
  * Redémarrez Tkinter Designer
  * Vérifiez la clé d'API et l'URL
  * Assurez-vous que votre design a une Frame 

* Autre chose ?
  * [Signalez des problèmes non répertoriés ici sur GitHub](https://github.com/ParthJadhav/Tkinter-Designer/issues/new)
