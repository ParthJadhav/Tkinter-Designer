# Como usar o Tkinter Designer

#### Traduções:
- [简体中文](/docs/instructions.zh-CN.md)
- [Frances](/docs/instructions.fr-FR.md)
- [ગુજરાતી](docs/instructions.gu-GU.md)
- [عربية](/docs/instructions.ar-DZ.md)
- [Turco](/docs/instructions.tr-TR.md)

___

## Índice:
1. [**Comece por aqui**](#getting-started-1)
   1. [Instalação do Python](#getting-started-1)
   2. [Instalação do Tkinter Designer](#getting-started-2)
   3. [Faça uma conta no Figma](#getting-started-3)
   
2. [**Formatando seu design Figma**](#formatting-1)
   1. [Referência](#formatting-1)
   2. [Guia de elementos](#formatting-2)
   
3. [**Usando o Tkinter Designer**](#Using-Tkinter-Designer)
   1. [Token de acesso pessoal](#using-1)
   2. [Obtendo o URL do seu arquivo](#using-2)
   3. [Usando a CLI](#using-cli)
   4. [Usando a GUI](#using-gui)
   
4. [**Solução de problemas**](#Troubleshooting)

<br><br>

# Começando <small>[[Top](#table-of-contents)]</small>

<a id="getting-started-1"></a>
## 1. Instalando Python
Antes de usar o Tkinter Designer, você precisará instalar o Python.  
* [Aqui está um link para a página de downloads do Python.](https://www.python.org/downloads)  
* [Aqui está um guia útil para instalar o Python em vários sistemas operacionais.](https://wiki.python.org/moin/BeginnersGuide/Download)

*Mais adiante neste guia, você usará o Package Installer for Python (pip), que pode exigir que você adicione o Python ao PATH do seu sistema.*

___
<br>

<a id="getting-started-2"></a>
## 2. Instalando Tkinter Designer

*Três opções:*

1. `pip install tkdesigner`

2. Instale [poetry](https:python-poetry.org)
   * `poetry new <gui_project_name> && cd <gui_project_name>`
   * `poetry add tkdesigner`
   * `poetry install`

3. Para executar o Tkinter Designer a partir do código-fonte, siga as instruções abaixo.

   1. Baixe os arquivos de origem do Tkinter Designer, você pode baixar manualmente ou usar o GIT.

      ` git clone https://github.com/ParthJadhav/Tkinter-Designer.git `

   2. Altere seu diretório de trabalho para Tkinter Designer.

      `cd tkinter-designer`
      
   3. Instale as dependências necessárias executando 

      * `pip install -r requirements.txt`
         * In the event that pip doesn't work, also try the following commands:
         * `pip3 install -r requirements.txt`
         * `python -m pip install -r requirements.txt`
         * `python3 -m pip install -r requirements.txt`
         * If this still doesn't work, ensure that Python is added to the PATH.
   
   Isso instalará todos os requisitos e o Tkinter Designer. Antes de usar o Tkinter Designer, você precisa criar um arquivo Figma com as instruções abaixo.

  Se você já criou um arquivo, pule para [**Usando o Tkinter Designer**](#Using-Tkinter-Designer).

___
<br>

<a id="getting-started-3"></a>
## 3. Faça uma conta no Figma
1. Em um navegador da Web, navegue até [figma.com](https://www.figma.com/) e clique em 'Sign up'
2. Insira suas informações e, em seguida, verifique seu e-mail
3. Crie um novo arquivo Figma Design
4. Comece a fazer sua GUI
   * A próxima seção abrange a formatação necessária para a entrada do Tkinter Designer.
     * [Aqui está a série oficial de tutoriais do Figma para iniciantes.](https://www.youtube.com/watch?v=Cx2dkpBxst8&list=PLXDU_eVOJTx7QHLShNqIXL1Cgbxj7HlN4)
     * [Aqui está o canal oficial da Figma no YouTube.](https://www.youtube.com/c/Figmadesign/featured)
     * [Aqui está o Centro de Ajuda Figma.](https://help.figma.com/hc/en-us)

<br><br>

<a id="formatting-1"></a>
# Formatando seu design Figma <small>[[Top](#table-of-contents)]</small>

## 1. Referência
<br>

### Nomear é importante

| Figma Element Name | Tkinter Element |
| --- | --- |
| Button | Button |
| Text | Name it anything |
| Rectangle | Rectangle |
| TextArea | Text Area |
| TextBox | Entry |
| Image | Canvas.Image() |

<br>

O código gerado pelo Tkinter Designer é baseado nos nomes dos elementos do seu design Figma e, como tal, você precisa nomear seus elementos de acordo. No Figma, renomeie seus elementos clicando duas vezes neles no painel Camadas.

___
<br>

<a id="formatting-2"></a>
## 2. Guia de elementos
<br>

1. **Primeiro, crie um Frame que servirá como sua janela Tkinter.**
<br><br>

2. **Adicionando imagens**
   * As imagens podem ser criadas usando shapes and/or images
   * Se você usar vários shapes/images, você selecionar todos e pressionar <kbd>CTRL/&#8984; + G</kbd>
   * Depois disso nomeie o elemento ou grupo como "Image".
<br><br>

3. **Texto (Texto normal)**
   * Use o atalho <kbd>T</kbd> para ativar a ferramenta de texto e, em seguida, adicione o texto conforme desejado
   * O texto não precisa ser renomeado para uso no Tkinter Designer
   * Para pular linhas pressione <kbd>Return</kbd>  ou  <kbd>Enter</kbd> 
<br><br>

4. **Entrada (Single-Line User Input)**
   * Pressione <kbd>R</kbd> para habilitar a ferramenta Rectangle
   * Ajuste o retângulo ao seu gosto
   * Renomeio o retângulo para "TextBox"
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

<a id="Using-Tkinter-Designer"></a>
# Using Tkinter Designer <small>[[Top](#table-of-contents)]</small>

## Required Inputs
There are some inputs you'll need to collect to be able to use the TKinter Designer.

<a id="using-1"></a>

### 1. Personal Access Token
1. Log into your Figma account
2. Navigate to Settings
3. In the **Account** tab, scroll down to **Personal access tokens**
4. Enter the name of your access token in the entry form and press <kbd>Enter</kbd>
5. Your personal access token will be created.
   * Copy this token and keep it somewhere safe.
   * **You will not get another chance to copy this token.**

<a id="using-2"></a>

### 2. Getting your File URL
1. In your Figma design file, click the **Share** button in the top bar, then click on **&#x1f517; Copy link**

<a id="using-cli"></a>
## Using the CLI

Using the CLI is as simple as installing the package and running the CLI tool. 

### From PyPi

You can use the below command as test by replacing $FILE_URL & $FIGMA_TOKEN by your data. If you haven't got the token and link then refer to [**Required Inputs Section**](#using-1).


``` bash
$ pip install tkdesigner

$ tkdesigner $FILE_URL $FIGMA_TOKEN
```

### From Source

To use CLI from the source code you need to clone the repository and then follow the below instructions.

You can use the below command as test by replacing $FILE_URL & $FIGMA_TOKEN by your data. If you haven't got the token and link then refer to [**Required Inputs Section**](#using-1).

```bash
$ python -m tkdesigner.cli $FILE_URL $FIGMA_TOKEN

# To learn more about how to use the cli, pass the --help flag
$ python -m tkdesigner --help
```

### Output
By default, the GUI code will be written to build/gui.py. You can specify the output path by using `-o` Flag and providing the path.

To run the generated GUI, cd into the directory you built it to (e.g. build/) and run it just as you would any Tkinter GUI.
```bash
$ cd build
$ python3 gui.py
```
<a id="using-gui"></a>
## Using the GUI
### Open Tkinter Designer before doing the following steps.
<br>

1. Open TKinter Designer GUI by
```
cd Tkinter-Designer
cd gui
python3 gui.py
```
2. Paste your *personal access token* into the **Token ID** form in Tkinter Designer
3. Paste the link into the **File URL** form in Tkinter Designer
4. Click the **Output Path** form to open a file browser
5. Choose an output path and click **Select Folder**
6. Press **Generate**

The output files from Tkinter Designer will be placed in your chosen directory, inside a new folder called **build**. Congratulations, you have now created your Tkinter GUI using Tkinter Designer!

<br><br>

<a id="Troubleshooting"></a>

# Troubleshooting <small>[[Top](#table-of-contents)]</small>

* Elements not visible? Misplaced?
  * Please make sure that your Figma File has its elements named correctly. * See [Formatting Your Figma Design, &sect;1](#formatting-1)

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
