# Comment utiliser Tkinter Designer

## Sommaire:
1. [**Commencer**](#getting-started-top)
   1. [Installer Python](#getting-started-1)
   2. [Installer Tkinter Designer](#getting-started-2)
   3. [Créer un compte Figma](#getting-started-3)
   
2. [**Formater votre design Figma**](#formatting-your-figma-design-top)
   1. [Référence](#formatting-1)
   2. [Guide des éléments](#formatting-2)
   
3. [**Utiliser Tkinter Designer**](#using-tkinter-designer-top)
   1. [Clé d'accès personnelle](#using-1)
   2. [URL du fichier](#using-2)
   3. [Tester votre code généré](#using-3)
   
4. [**Diagnostic des anomalies**](#troubleshooting-top)

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

1. **First, create a Frame that will serve as your Tkinter Window.**
<br><br>

2. **Creating a Background**
   * Backgrounds can be created using shapes and/or images
   * If you use multiple shapes/images, you must group them together by selecting them all and pressing <kbd>CTRL/&#8984; + G</kbd>
<br><br>

3. **Text (Normal Text)**
   * Use the <kbd>T</kbd> key to activate the text tool, then add text as desired
   * Text does not have to be renamed for use in Tkinter Designer
   * Explicitly press the <kbd>Return</kbd>  Or  <kbd>Enter</kbd> Key to move to the next line.
<br><br>

4. **Entry (Single-Line User Input)**
   * Activate the Rectangle tool with <kbd>R</kbd>
   * Adjust the Rectangle to your liking
   * Make sure the Rectangle is named "TextBox"
<br><br>

5. **Text Area (Multi-Line User Input)**
   * Activate the Rectangle tool with <kbd>R</kbd>
   * Adjust the Rectangle to your liking
   * Make sure the Rectangle is named "TextArea"

6. **Rectangle**
   * Activate the Rectangle tool with <kbd>R</kbd>
   * Adjust the Rectangle to your liking
   * Make sure the Rectangle is named "Rectangle"
<br><br>

7. **Normal Button**
   * Add rectangle to serve as a button in your GUI
     * Optional: Add text for the button
   * Select the button(Rectangle), and any optional text, then group them with <kbd>CTRL/&#8984; + G</kbd>
   * Name the group "Button"

#### Refer to [this video](https://youtu.be/mFjE2-rbpm8?t=275) if you face any problem

<br><br>

8. **Rounded Button** 
   * Add rectangle to serve as a button in your GUI
     * Optional: Add text for the button
   * Make it rounded by adding corner radius by selecting the rectangle and adding corner radius from the right side. [Read more on it](https://help.figma.com/hc/en-us/articles/360050986854-Adjust-corner-radius-and-smoothing)
   * Create a Rectangle with same size of your button. Don't make it rounded. 
   * Change the Rectangle's color to match the Background
   * Now move the newly created rectangle below the main button(Rectangle).
   * Select the button, Rectangle, and any optional text, then group them with <kbd>CTRL/&#8984; + G</kbd>
   * Name the group "Button"

#### Refer to [this video](https://youtu.be/mFjE2-rbpm8?t=275) if you face any problem

<br><br>

# Using Tkinter Designer <small>[[Top](#table-of-contents)]</small>

### Open Tkinter Designer before doing the following steps.
<br>

<a id="using-1"></a>
## 1. Personal Access Token
1. Log into your Figma account
2. Navigate to Settings
3. In the **Account** tab, scroll down to **Personal access tokens**
4. Enter the name of your access token in the entry form and press <kbd>Enter</kbd>
5. Your personal access token will be created.
   * Copy this token and keep it somewhere safe.
   * **You will not get another chance to copy this token.**
6. Paste your personal access token into the **Token ID** form in Tkinter Designer
___
<br>

<a id="using-2"></a>
## 2. File URL
1. In your Figma design file, click the **Share** button in the top bar, then click on **&#x1f517; Copy link**
2. Paste the link into the **File URL** form in Tkinter Designer
___
<br>

<a id="using-3"></a>
## 3. Test Your Generated Code
1. In Tkinter Designer, click the **Output Path** form to open a file browser
2. Choose an output path and click **Select Folder**
3. Press **Generate**

The output files from Tkinter Designer will be placed in your chosen directory, inside a new folder called **generated_code**. Congratulations, you have now created your Tkinter GUI using Tkinter Designer!

<br><br>

# Troubleshooting <small>[[Top](#table-of-contents)]</small>

* Elements not visible? Misplaced?
  * Please make sure that your top-level Frame is positioned with its X and Y coordinates at (0, 0)
    * Check the right side bar, under **Design**

* Button has an unintended gray background?
  * Make sure you have added a Rectangle behind your button element, and that its Fill color is the same as the Background's

* Incorrect elements?
  * Make sure you have named your elements correctly in Figma
    * See [Formatting Your Figma Design, &sect;1](#formatting-1)

* Window is larger than the screen?
  * Reduce the size of your elements in Figma

* Files not generating?
  * Restart Tkinter Designer
  * Double-check the token and URL
  * Make sure your design has a Frame

* Something else?
  * [Report issues not listed here on GitHub](https://github.com/ParthJadhav/Tkinter-Designer/issues/new)
