# Come usare Tkinter Designer

#### Traduzioni

- [简体中文](/docs/instructions.zh-CN.md)
- [Français](/docs/instructions.fr-FR.md)
- [ગુજરાતી](docs/instructions.gu-GU.md)
- [Italiano](instructions.it-IT.md)
- [عربية](/docs/instructions.ar-DZ.md)
- [Turkish](/docs/instructions.tr-TR.md)

___

## Indice dei contenuti

1. [**Introduzione**](#getting-started-1)
   1. [Installa Python](#getting-started-1)
   2. [Installa Tkinter Designer](#getting-started-2)
   3. [Crea un account Figma](#getting-started-3)

2. [**Formattare il Design di Figma**](#formatting-1)
   1. [Riferimento](#formatting-1)
   2. [Guida sugli elementi](#formatting-2)

3. [**Utilizza Tkinter Designer**](#Using-Tkinter-Designer)
   1. [Personal Access Token](#using-1)
   2. [Ottieni l'URL del file](#using-2)
   3. [Utilizzare la CLI](#using-cli)
   4. [Utilizzare la GUI](#using-gui)

4. [**Risoluzione dei problemi**](#Troubleshooting)

<br><br>

# Introduzione <small>[[Top](#indice-dei-contenuti)]</small>

<a id="getting-started-1"></a>

## 1. Installa Python

Prima di utilizzare Tkinter Designer, devi installare Python.
- [Questo è un collegamento alla pagina di download di Python.](https://www.python.org/downloads)  
- [Questa è una guida utile su come installare Python su vari sistemi operativi.](https://wiki.python.org/moin/BeginnersGuide/Download)

*In questa guida dovrai utilizzare il Package Installer for Python (pip), il quale potrebbe richiedere di essere aggiunto alla PATH di sistema.*
___
<br>

<a id="getting-started-2"></a>

## 2. Installa Tkinter Designer

*Tre opzioni:*

1. Utilizza il comando `pip install tkdesigner`;

2. Tramite [poetry](https:python-poetry.org)
   - `poetry new <gui_project_name> && cd <gui_project_name>`
   - `poetry add tkdesigner`
   - `poetry install`

   Per eseguire i comandi sopra riportati è necessario aver installato [poetry](https:python-poetry.org).

3. Per eseguire Tkinter Designer dal codice sorgente, segui le seguenti istruzioni.

   1. Scarica manualmente i file dal codice sorgente di Tkinter Designer by downloading o utilizza GIT.

      ` git clone https://github.com/ParthJadhav/Tkinter-Designer.git `

   2. Spostati nella directory di Tkinter Designer.

      `cd Tkinter-Designer`

   3. Installa le dipendenze necessarie tramite i seguenti comandi:

      - `pip install -r requirements.txt`
         - Se pip non dovesse funzionare, puoi provare ad utilizzare i seguenti comandi:
         - `pip3 install -r requirements.txt`
         - `python -m pip install -r requirements.txt`
         - `python3 -m pip install -r requirements.txt`
         - Se non dovesse comunque funzionare, assicurati di aver aggiunto Python alla PATH di sistema.

   Questo installerà Tkinter Designer e le sue dipendenze. Per poter utilizzare Tkinter Designer devi creare un file di Figma seguendo le istruzioni. 

   Qualora avessi già creato il file puoi recarti nella sezione [**Utilizza Tkinter Designer**](#Using-Tkinter-Designer).
___
<br>

<a id="getting-started-3"></a>

## 3. Crea un account Figma

1. In un web brwoser, vai su [figma.com](https://www.figma.com/) e clicca su 'Sign up';
2. Inserisci le tue informazioni, e verifica il tuo indirizzo mail;
3. Crea un nuovo File di Design Figma;
4. Inizia a disegnare la tua interfaccia.
   - Di seguito delle fonti utili:
     - [Questa è la serie di tutorial ufficiale di Figma.](https://www.youtube.com/watch?v=Cx2dkpBxst8&list=PLXDU_eVOJTx7QHLShNqIXL1Cgbxj7HlN4)
     - [Questo è il canale YouTube ufficiale di Figma.](https://www.youtube.com/c/Figmadesign/featured)
     - [Questo è il centro di assistenza ufficiale di Figma.](https://help.figma.com/hc/en-us)

<br><br>

<a id="formatting-1"></a>

# Formatta il tuo Design Figma <small>[[Top](#indice-dei-contenuti)]</small>

## 1. Riferimento

<br>

### La denominazione è importante

| Nome elemento Figma | Elemento Tkinter |
| --- | --- |
| Button | Button |
| Line | Line |
| Text | Testo a scelta |
| Rectangle | Rectangle |
| TextArea | Text Area |
| TextBox | Entry |
| Image | Canvas.Image() |

<br>

Il codice generato da Tkinter Designer è basato sui nomi degli elementi del Design Figma e, visto ciò, devi nominare gli elementi correttamente. In Figma, rinomina i elementi facendovi doppio click nel pannello Layers.

___
<br>

<a id="formatting-2"></a>

## 2. Guida sugli elementi

<br>

1. **Per prima cosa, crea un Frame che fungerà come finestra di Tkinter.**
<br><br>

2. **Aggiungi immagini**
   - Le immagini possono essere importate o create mediante forme
   - Se desideri utilizzare più forme/immagini, devi raggrupparle selezionandole e premendo i tasti <kbd>CTRL/&#8984; + G</kbd>
   - Dopodiché nomina l'elemento o il gruppo "Image"
<br><br>

3. **Testo (Testo normale)**
   - Usa il tasto <kbd>T</kbd> per attivare lo strumento testo, quindi aggiungi il testo desiderato
   - Il testo non deve essere rinominato per essere utilizzato in Tkinter Designer
   - Premi il tasto <kbd>Return</kbd>  o  <kbd>Enter</kbd> per muoverti alla riga successiva
<br><br>

4. **Input (Inserimento a linea singola)**
   - Attiva lo strumento rettangolo utilizzando il tasto <kbd>R</kbd>
   - Ridimensiona l'elemento rettangolo a tuo piacimento
   - Assicurati di rinominare l'elemento rettangolo "TextBox"
<br><br>

5. **Area di testo (Inserimento a linea multipla)**
   - Attiva lo strumento rettangolo utilizzando il tasto <kbd>R</kbd>
   - Ridimensiona l'elemento rettangolo a tuo piacimento
   - Assicurati di rinominare l'elemento rettangolo "TextArea"

6. **Rettangolo**
   - Attiva lo strumento rettangolo utilizzando il tasto <kbd>R</kbd>
   - Ridimensiona l'elemento rettangolo a tuo piacimento
   - Assicurati di rinominare l'elemento rettangolo "Rectangle"
<br><br>

7. **Pulsante normale**
   - Aggiungi un rettangolo per farlo funzionare come pulsante
     - Facoltativo: Aggiungi un testo al tuo pulsante
   - Seleziona il pulsante (Rettangolo), e l'eventuale testo, e raggruppali premendo i tasti <kbd>CTRL/&#8984; + G</kbd>
   - Rinomina il gruppo "Button"

#### Guarda [questo video](https://youtu.be/Qd-jJjduWeQ) se dovessi riscontrare problemi.

<br><br>

8. **Pulsante rotondo**
   - Aggiungi un rettangolo per farlo funzionare come pulsante
     - Facoltativo: Aggiungi un testo al tuo pulsante
   - Rendilo rotondo aggiungendo un raggio ai bordi. [Scopri di più qui.](https://help.figma.com/hc/en-us/articles/360050986854-Adjust-corner-radius-and-smoothing)
   - Crea un elemento Rettangolo dalle stesse dimensioni del tuo pulsante. Non seguire il punto precedente (dunque non renderlo rotondo)
   - Cambia il colore dell'elemento Rettangolo in modo da farlo combaciare con lo sfondo
   - Ora posizionati sull'ultimo elemento Rettangolo creato (quello sottostante)
   - Seleziona il pulsante (Rettangolo), e l'eventuale testo, e raggruppali premendo i tasti <kbd>CTRL/&#8984; + G</kbd>
   - Rinomina il gruppo "Button"

#### Guarda [questo video](https://youtu.be/Qd-jJjduWeQ) se dovessi riscontrare problemi.

<br><br>

<a id="Using-Tkinter-Designer"></a>

# Utilizza Tkinter Designer <small>[[Top](#indice-dei-contenuti)]</small>

## Requisiti minimi

Ci sono alcuni requisiti minimi che devi soddisfare per poter utilizzare TKinter Designer.

<a id="using-1"></a>

### 1. Personal Access Token

1. Accedi a Figma
2. Vai nelle impostazioni
3. Nella scheda **Account**, scrolla fino a **Personal access tokens**
4. Inserisci il nome del tuo access token nel campo e premi <kbd>Enter</kbd>
5. Ora il tuo Personal Access Token è stato creato.
   - Copia questo token e tienilo al sicuro.
   - **Non esiste alcuna procedura per recuperare questo codice.**

<a id="using-2"></a>

### 2. Ottieni l'URL del file

1. Nel tuo file di Design Figma, clicca sul pulsante **Share** nella barra in alto, quindi clicca su **&#x1f517; Copy link**

<a id="using-cli"></a>

## Utilizzare la CLI

Per utilizzare la CLI è sufficiente installare il pacchetto ed avviarlo da riga di comando. Per installarlo segui una delle due prossime opzioni.

### Tramite PyPi

Puoi usare il seguente comando sostituendo $FILE_URL & $FIGMA_TOKEN con i tuoi dati. Se non dovessi avere questi dati, segui la sezione [**Requisiti Minimi**](#using-1).

``` bash
pip install tkdesigner
tkdesigner $FILE_URL $FIGMA_TOKEN
```

### Tramite sorgente

Per usare CLI puoi decidere di clonare il codice sorgente dalla repository e seguire le istruzioni di seguito.

Puoi usare il seguente comando sostituendo $FILE_URL & $FIGMA_TOKEN by your data. e non dovessi avere questi dati, segui la sezione [**Requisiti Minimi**](#using-1).

```bash
$ python -m tkdesigner.cli $FILE_URL $FIGMA_TOKEN
# To learn more about how to use the cli, pass the --help flag
$ python -m tkdesigner --help
```

### Output

Di base, il codice dell'interfaccia grafica wiene scritto nella directory ``build/gui.py``. Puoi specificare un'altra directory utilizzando il flag `-o` seguito dalla path.

Per eseguire la GUI generata, spostarsi nella directory di output ed eseguire allo stesso modo in cui si esegue una GUI in Tkinter.

```bash
cd build
python3 gui.py
```

<a id="using-gui"></a>

## Utilizzare la GUI

### Apri Tkinter Designer prima di eseguire i seguenti passaggi

<br>

1. Apri TKinter Designer GUI eseguendo i seguenti comandi:

```
cd Tkinter-Designer
cd gui
python3 gui.py
```

2. Incolla il tuo *personal access token* nel form **Token ID** di Tkinter Designer
3. Incolla il tuo **File URL** nel form di Tkinter Designer
4. Clicca su **Output Path** per aprire il file browser
5. Scegli la cartella di destinazione e clicca su **Select Folder**
6. Clicca infine su **Generate**

I file di output di Tkinter Designer verranno salvati nella directory da te inserita, dentro una nuova cartella chiamata **build**. Congratulazioni, hai creato la tua GUI Tkinter grazie a Tkinter Designer!

<br><br>

<a id="Troubleshooting"></a>

# Risoluzione dei problemi <small>[[Top](#indice-dei-contenuti)]</small>

- Elementi non visibili? Fuori posto?
  - Assicurati di aver rinominato correttamente gli elementi nel tuo file di Figma.
  Leggi [Formatta il tuo Design Figma](#formatting-1).

- Il pulsante ha un indisiderato sfondo grigio?
  - Assicurati di aver aggiunto un Rettangolo dietro al tuo elemento pulsante, e che il suo colore sia identico a quello di sfondo.

- Elementi errati?
  - Assicurati di aver rinominato correttamente gli elementi nel tuo file di Figma.
  Leggi [Formatta il tuo Design Figma](#formatting-1).

- La finestra è più grande dello schermo?
  - Riduci la dimensione degli elementi Figma.

- Non si generano i file?
  - Riavvia Tkinter Designer
  - Controlla il tuo personal access token e l'URL del file
  - Assicurati di aver predisposto un frame al tuo file di Figma

- Qualcos'altro?
  - [Segnala i problemi non listati nella sezione Issues della repository](https://github.com/ParthJadhav/Tkinter-Designer/issues/new)