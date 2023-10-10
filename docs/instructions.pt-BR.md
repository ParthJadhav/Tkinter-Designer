# Como usar o Tkinter Designer
___

## Índice

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
- [Aqui está um link para a página de downloads do Python.](https://www.python.org/downloads)  
- [Aqui está um guia útil para instalar o Python em vários sistemas operacionais.](https://wiki.python.org/moin/BeginnersGuide/Download)

*Mais adiante neste guia, você usará o Package Installer for Python (pip), que pode exigir que você adicione o Python ao PATH do seu sistema.*

___
<br>

<a id="getting-started-2"></a>

## 2. Instalando Tkinter Designer

*Três opções:*

1. `pip install tkdesigner`

2. Instale [poetry](https:python-poetry.org)
   - `poetry new <gui_project_name> && cd <gui_project_name>`
   - `poetry add tkdesigner`
   - `poetry install`

3. Para executar o Tkinter Designer a partir do código-fonte, siga as instruções abaixo.

   1. Baixe os arquivos de origem do Tkinter Designer, você pode baixar manualmente ou usar o GIT.

      ` git clone https://github.com/ParthJadhav/Tkinter-Designer.git `

   2. Altere seu diretório de trabalho para Tkinter Designer.

      `cd tkinter-designer`

   3. Instale as dependências necessárias executando

      - `pip install -r requirements.txt`
         - No evento do pip não funcionar, tente também os seguintes comandos:
         - `pip3 install -r requirements.txt`
         - `python -m pip install -r requirements.txt`
         - `python3 -m pip install -r requirements.txt`
         - Se ainda assim não funcionar, se certifique de que o Python está adicionado ao PATH.

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
   - A próxima seção abrange a formatação necessária para a entrada do Tkinter Designer.
     - [Aqui está a série oficial de tutoriais do Figma para iniciantes.](https://www.youtube.com/watch?v=Cx2dkpBxst8&list=PLXDU_eVOJTx7QHLShNqIXL1Cgbxj7HlN4)
     - [Aqui está o canal oficial da Figma no YouTube.](https://www.youtube.com/c/Figmadesign/featured)
     - [Aqui está o Centro de Ajuda Figma.](https://help.figma.com/hc/en-us)

<br><br>

<a id="formatting-1"></a>

# Formatando seu design Figma <small>[[Top](#table-of-contents)]</small>

## 1. Referência

<br>

### Nomear é importante

| Nome do Elemento no Figma | Elemento no Tkinter |
| --- | --- |
| Button | Button |
| Text | Qualquer nome |
| Rectangle | Rectangle |
| Line | Line |
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
   - As imagens podem ser criadas usando formatos e/ou imagens
   - Se você usar vários formatos/imagens, você selecionar todos e pressionar <kbd>CTRL/&#8984; + G</kbd>
   - Depois disso nomeie o elemento ou grupo como "Image".
<br><br>

3. **Texto (Texto normal)**
   - Use o atalho <kbd>T</kbd> para ativar a ferramenta de texto e, em seguida, adicione o texto conforme desejado
   - O texto não precisa ser renomeado para uso no Tkinter Designer
   - Para pular linhas pressione <kbd>Return</kbd>  ou  <kbd>Enter</kbd>
<br><br>

4. **Entrada de texto (Uma linha para entrada do usuario)**
   - Pressione <kbd>R</kbd> para habilitar a ferramenta Retângulo
   - Ajuste o retângulo ao seu gosto
   - Renomeio o retângulo para "TextBox"
<br><br>

5. **Entrada de texto (Entrada de usuário de várias linhas)**
   - Pressione <kbd>R</kbd> para habilitar a ferramenta Retângulo
   - Ajuste o retângulo ao seu gosto
   - Renomeio o retângulo para "TextArea"

6. **Retângulo**
   - Pressione <kbd>R</kbd> para habilitar a ferramenta Retângulo
   - Ajuste o retângulo ao seu gosto
   - Renomeio o retângulo para "Rectangle"
<br><br>

7. **Botão normal**
   - Adicione um retângulo para servir como um botão em sua GUI
     - Opcional: adicione texto para o botão
   - Selecione o botão (Retângulo) e qualquer texto opcional e agrupe-os com <kbd>CTRL/&#8984; + G</kbd>
   - Nomeie o grupo "Button"

#### Consulte [este vídeo](https://youtu.be/Qd-jJjduWeQ) se tiver algum problema

<br><br>

8. **Botão arredondado**
   - Adicione um retângulo para servir como um botão em sua GUI
     - Opcional: adicione texto para o botão
   - Para fazer o arredondamento no botão modifique o raio (´Corner radius´) [Leia mais sobre isso](https://help.figma.com/hc/en-us/articles/360050986854-Adjust-corner-radius-and-smoothing)
   - Crie um retângulo com o mesmo tamanho do seu botão. Não o torne arredondado.
   - Altere a cor do retângulo para corresponder ao plano de fundo
   - Agora mova o retângulo recém-criado abaixo do botão principal (Retângulo).
   - Selecione o botão, Retângulo e qualquer texto opcional e, em seguida, agrupe-os com <kbd>CTRL/&#8984; + G</kbd>
   - Nomeie o grupo "Button"

#### Consulte [este vídeo](https://youtu.be/Qd-jJjduWeQ) se tiver algum problema

<br><br>

<a id="Using-Tkinter-Designer"></a>

# Usando o Tkinter Designer <small>[[Top](#table-of-contents)]</small>

## Entradas Necessárias

Existem algumas entradas que você precisará coletar para poder usar o TKinter Designer.

<a id="using-1"></a>

### 1. Token de acesso pessoal

1. Faça login na sua conta Figma
2. Navegue até Configurações
3. Na guia **Account** role para baixo até **Personal access tokens**
4. Digite o nome do seu token de acesso no formulário de entrada e pressione <kbd>Enter</kbd>
5. Seu token de acesso pessoal será criado.
   - Copie este token e mantenha-o em algum lugar seguro.
   - **Você não terá outra chance de copiar este token.**

<a id="using-2"></a>

### 2. Obtendo o URL do seu arquivo

1. Em seu arquivo de design Figma, clique no **Share** botão na barra superior, em seguida, clique em **&#x1f517; Copy link**

<a id="using-cli"></a>

## Usando a CLI

Usar a CLI é tão simples quanto instalar o pacote e executar a ferramenta CLI.

### De PyPi

Você pode usar o comando abaixo como teste substituindo $FILE_URL & $FIGMA_TOKEN Se você não tiver o token e o link, consulte a [**Seção de Entradas Requeridas**](#using-1).

``` bash
pip install tkdesigner

tkdesigner $FILE_URL $FIGMA_TOKEN
```

### Da fonte

Para usar a CLI a partir do código-fonte, você precisa clonar o repositório e seguir as instruções abaixo.

Você pode usar o comando abaixo como teste substituindo $FILE_URL & $FIGMA_TOKEN por seus dados. Se você não tiver o token e o link, consulte a [**Seção de Entradas Requeridas**](#using-1).

```bash
$ python -m tkdesigner.cli $FILE_URL $FIGMA_TOKEN

# To learn more about how to use the cli, pass the --help flag
$ python -m tkdesigner --help
```

### Saída

Por padrão, o código GUI será escrito em build/gui.py. Você pode especificar o caminho de saída usando o sinalizador `-o` e fornecendo o caminho.

Para executar a GUI gerada, cd no diretório em que você a construiu (por exemplo, build/) e execute-a como faria com qualquer GUI do Tkinter.

```bash
cd build
python3 gui.py
```

<a id="using-gui"></a>

## Usando a GUI

### Abra o Tkinter Designer antes de executar as etapas a seguir

<br>

1. Abra a GUI do TKinter Designer por

```
cd Tkinter-Designer
cd gui
python3 gui.py
```

2. Cole seu *token de acesso pessoal* no formulário **Token ID** no Tkinter Designer
3. Cole o link no formulário **URL do arquivo** no Tkinter Designer
4. Clique no formulário **Output Path** para abrir um navegador de arquivos
5. Escolha um caminho de saída e clique em **Select Folder**
6. Pressione **Generate**

Os arquivos de saída do Tkinter Designer serão colocados no diretório escolhido, dentro de uma nova pasta chamada **build**. Parabéns, você agora criou sua GUI do Tkinter usando o Tkinter Designer!

<br><br>

<a id="Troubleshooting"></a>

# Solução de problemas <small>[[Top](#table-of-contents)]</small>

- Elementos não visíveis? Extraviado?
  - Certifique-se de que seu arquivo Figma tenha seus elementos nomeados corretamente. * Consulte [Formatando o design do Figma, &sect;1](#formatting-1)

- O botão tem um fundo cinza não intencional?
  - Certifique-se de ter adicionado um retângulo atrás do elemento do botão e que sua cor de preenchimento seja a mesma do plano de fundo

- Elementos incorretos?
  - Certifique-se de ter nomeado seus elementos corretamente no Figma
    - Consulte [Formatando o design do Figma, &sect;1](#formatting-1)

- A janela é maior que a tela?
  - Reduza o tamanho de seus elementos no Figma

- Arquivos não estão gerando?
  - Reinicie o Tkinter Designer
  - Verifique novamente o token e o URL
  - Certifique-se de que seu design tenha um quadro

- Algo mais?
  - [Relatar problemas não listados aqui no GitHub](https://github.com/ParthJadhav/Tkinter-Designer/issues/new)
