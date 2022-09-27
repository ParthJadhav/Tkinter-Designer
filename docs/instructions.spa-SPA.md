# ¿Cómo usar Tkinter Designer?

#### Traducciones

- [简体中文](/docs/instructions.zh-CN.md)
- [Français](/docs/instructions.fr-FR.md)
- [ગુજરાતી](docs/instructions.gu-GU.md)
- [عربية](/docs/instructions.ar-DZ.md)
- [Turkish](/docs/instructions.tr-TR.md)

___

## Tabla de contenidos

1. [**Comience por aquí**](#getting-started-1)
   1. [Instalar Python](#getting-started-1)
   2. [Instalar Tkinter Designer](#getting-started-2)
   3. [Crear una cuenta en Figma](#getting-started-3)

2. [**Dando formato a tu diseño de Figma**](#formatting-1)
   1. [Referencia](#formatting-1)
   2. [Guía de Elementos](#formatting-2)

3. [**Usar Tkinter Designer**](#Using-Tkinter-Designer)
   1. [Token de Acceso Personal](#using-1)
   2. [Obteniendo URL de tu archivo](#using-2)
   3. [Usando el CLI](#using-cli)
   4. [Usando el GUI](#using-gui)

4. [**Solución de Problemas**](#Troubleshooting)

<br><br>

# Comenzando <small>[[Top](#table-of-contents)]</small>

<a id="getting-started-1"></a>

## 1. Instalar Python

Antes de usar Tkinter Desinger, deberás instalar Python.  
- [Aquí hay un link a la página de descargas de Python.](https://www.python.org/downloads)  
- [Aquí hay una guía útil de cómo instalar Python en diferentes Sistemas Operativos.](https://wiki.python.org/moin/BeginnersGuide/Download)

*Más tarde en éste curso, usarás el Package Installer de Python (pip), el cual requiere que agregues Python al PATH de tu sistema*

___
<br>

<a id="getting-started-2"></a>

## 2. Instalar Tkinter Designer

*Tres opciones:*

1. `pip install tkdesigner`

2. Instalar [poetry](https:python-poetry.org)
   - `poetry new <gui_project_name> && cd <gui_project_name>`
   - `poetry add tkdesigner`
   - `poetry install`

3. Para ejecutar Tkinter Designer desde el archivo fuente, sigue las siguientes instrucciones.

   1. Descarga el archivo fuente, descargandolo manualmente o usando GIT.

      ` git clone https://github.com/ParthJadhav/Tkinter-Designer.git `

   2. Cambia tu directorio de trabajo a Tkinter Designer.

      `cd Tkinter-Designer`

   3. Instala las dependencias necesarias ejecutando

      - `pip install -r requirements.txt`
         - En el caso que pip no funcione, también prueba con los siguientes comandos:
         - `pip3 install -r requirements.txt`
         - `python -m pip install -r requirements.txt`
         - `python3 -m pip install -r requirements.txt`
         - Si esto no funciona, asegurate de que Python está agregado al PATH.

   Ésto instalará todos los requisitos y Tkinter Designer. Antes de usar Tkinter Designer, deberás crear un archivo de Figma siguiendo las siguientes instrucciones.

   Si ya creaste un archivo Figma, puedes saltar a la sección [**Usar Tkinter Designer**](#Using-Tkinter-Designer).

___
<br>

<a id="getting-started-3"></a>

## 3. Crear una cuenta en Figma

1. En un navegador web, navega a [figma.com](https://www.figma.com/) y da click en 'Sign up'
2. Ingresa tu informacion y luego verifica tu email
3. Crea un nuevo archivo de diseño en Figma
4. Comienza a crear tu GUI
   - Las siguientes secciones abarcan el formato necesario para el resultado en Tkinter Designer.
     - [Aqúi está el tutorial oficial de Figma para principiantes.](https://www.youtube.com/watch?v=Cx2dkpBxst8&list=PLXDU_eVOJTx7QHLShNqIXL1Cgbxj7HlN4)
     - [Aquí está el canal oficial de YouTube de Figma.](https://www.youtube.com/c/Figmadesign/featured)
     - [Aquí está el Centro de Ayuda de Figma.](https://help.figma.com/hc/en-us)

<br><br>

<a id="formatting-1"></a>

# Dando formato a tu diseño de Figma <small>[[Top](#table-of-contents)]</small>

## 1. Referencias

<br>

### El nombre es importante

| Nombre de Elemento en Figma | Elemento en Tkinter |
| --- | --- |
| Button | Button |
| Line | Line |
| Text | Nómbralo como quieras |
| Rectangle | Rectangle |
| TextArea | Text Area |
| TextBox | Entry |
| Image | Canvas.Image() |

<br>

El código generado por Tkinter Designer está basado en los nombres de los elementos de tu diseño en Figma, y como tal, necesitas nombrar tus elementos de acuerdo a lo establecido. En Figma, puedes renombrar tus elementos al dar doble click en ellos en el panel de Layers.

___
<br>

<a id="formatting-2"></a>

## 2. Guía de Elementos

<br>

1. **Primero, crea un Frame que te servirá como tu ventana de Tkinter.**
<br><br>

2. **Añadir Imágenes**
   - Las imágenes pueden ser creadas usando formas y/o imágenes.
   - Si usas multiples formas/imágenes, necesitarás agruparlos todos juntos, seleccionandolos y presionando <kbd>CTRL/&#8984; + G</kbd>
   - Después de eso, nombra el elemento o grupo como "Image".
<br><br>

3. **Texto (Texto Normal)**
   - Usa la tecla <kbd>T</kbd> para activar la herramienta de texto, después añade texto que desees.
   - El texto no tiene que ser renombrado para usar en Tkinter Designer.
   - Explicitamente presiona las teclas <kbd>Return</kbd>  o  <kbd>Enter</kbd> para saltar a la siguiente línea.
<br><br>

4. **Entry (Input de Usuario en una sóla línea)**
   - Activa la herramienta de Rectángulo con la letra <kbd>R</kbd>
   - Ajusta el rectangulo a tu gusto
   - Asegurate que el Rectángulo sea llamado "TextBox"
<br><br>

5. **Area de Texto (Input de Usuario en múltiples líneas)**
   - Activa la herramienta de Rectángulo con la letra <kbd>R</kbd>
   - Ajusta el rectangulo a tu gusto
   - Asegurate que el Rectángulo sea llamado "TextArea"

6. **Rectángulo**
   - Activa la herramienta de Rectángulo con la letra <kbd>R</kbd>
   - Ajusta el rectangulo a tu gusto
   - Asegurate que el Rectángulo sea llamado "Rectangle"
<br><br>

7. **Botón Normal**
   - Añade un rectangulo para que funcione como un botón en tu GUI
     - Opcional: Añade texto para el botón.
   - Selecciona el botón(Rectangle), y cualquier texto opcional, luego agrupalos con <kbd>CTRL/&#8984; + G</kbd>
   - Nombra el grupo "Button"

#### Dirigete a [Éste video](https://youtu.be/mFjE2-rbpm8?t=275) si te encuentras con cualquier problema

<br><br>

8. **Botón circular**
   - Añade un rectangulo para que funcione como un botón en tu GUI
     - Opcional: Añade texto para el botón.
   - Hazlo redondo al añadir un radio de esquinas, seleccionado el rectángulo y añadiendo un radio de esquinas desde el lado derecho. [Lee más en](https://help.figma.com/hc/en-us/articles/360050986854-Adjust-corner-radius-and-smoothing)
   - Crea un rectángulo con el mismo tamaño que tu botón. No lo hagas redondeado.
   - Cambia el color del rectángulo para combinarlo con el fondo
   - Ahora, mueve el rectángulo más nuevo debajo del botón principal(Rectangle).
   - Selecciona el botón, el rectángulo y cualquier texto adicional, luego agrupalos con <kbd>CTRL/&#8984; + G</kbd>
   - Nombra al grupo "Button"

#### Dirigete a [Éste video](https://youtu.be/mFjE2-rbpm8?t=275) si te encuentras con cualquier problema

<br><br>

<a id="Using-Tkinter-Designer"></a>

# Usar Tkinter Designer <small>[[Top](#table-of-contents)]</small>

## Datos Requeridos

Hay algunos datos que necesitarás coleccionar para usar Tkinter Designer.

<a id="using-1"></a>

### 1. Token de Acceso Personal

1. Inicia sesión en tu cuenta de Figma
2. Dirígete a Configuración
3. En la pestaña de **Account**, deslíza hacía abajo hasta **Personal Access Tokens**
4. Ingresa el nombre de tu Token de Acceso Personal en el campo y presiona <kbd>Enter</kbd>
5. Tu Token de Acceso Personal será creada.
   - Copia ésta Token y guárdala en algún lugar seguro.
   - **No tendrás otra chance de copiar ésta Token.**

<a id="using-2"></a>

### 2. Obteniendo URL de tu archivo

1. En tu archivo de diseño de Figma, da click en el botón de **Share** en la barra superior, luego da click en **&#x1f517; Copy Link**

<a id="using-cli"></a>

## Usando el CLI

Usar el CLI es tan simple como instalar un pacquete y ejecutar la herramienta de CLI.

### Desde PyPi

Puedes usar el siguiente comando como una prueba, reemplazando $FILE_URL & $FIGMA_TOKEN por tu información. Si todavía no haz conseguido el Token, dirígete a [**Datos Requeridos**](#using-1).

``` bash
pip install tkdesigner

tkdesigner $FILE_URL $FIGMA_TOKEN
```

### Desde Archivo Fuente

Para usar CLI desde el archivo fuente, necesitas clonar el repositorio y luego seguir las siguientes instrucciones.

Puedes usar el siguiente comando como una prueba, reemplazando $FILE_URL & $FIGMA_TOKEN por tu información. Si todavía no haz conseguido el Token, dirígete a [**Datos Requeridos**](#using-1).

```bash
$ python -m tkdesigner.cli $FILE_URL $FIGMA_TOKEN

# Para aprender más sobre cómo usar el CLI, pasa el Flag --help
$ python -m tkdesigner --help
```

### Resultado

Por defecto, el código GUI será almacenado en build/gui.py. Puedes especificar la ruta al presionar la Flag `-o` y escribiendo la ruta.

Para ejecutar el GUI generado, haz un cd hasta el directorio que haz creado (en general: build/) y ejecutalo tal como lo hicieras con cualquier GUI de Tkinter.

```bash
cd build
python3 gui.py
```

<a id="using-gui"></a>

## Usando el GUI

### Abre Tkinter Desinger antes de realizar los siguientes pasos

<br>

1. Abre Tkinter Designer GUI de la siguiente forma

```
cd Tkinter-Designer
cd gui
python3 gui.py
```

2. Pega tu *Token de Acceso Personal* en el campo de **Token ID** en Tkinter Designer
3. Pega el link en el campo de **File URL** en Tkinter Designer
4. Da click en el campo de **Output Path** para abrir el buscador de archivos
5. Elige una ruta de destino y da click **Select Folder**
6. Presiona **Generate**

Los archivos generados por Tkinter Designer serán puestos en tu directorio de destino, dentro de una nueva carpeta llamada **build**. Felicitaciones, ahora has cread tu GUI de Tkinter usando Tkinter Designer!

<br><br>

<a id="Troubleshooting"></a>

# Solución de Problemas <small>[[Top](#table-of-contents)]</small>

- ¿Los elementos no son visibles? ¿Están en un lugar equivocado?
  - Por favor, asegurate que tu archivo Figma tiene los elementos nombrados correctamente. * Ve [Dando formato a tu diseño de Figma, &sect;1](#formatting-1)

- ¿El botón tiene un fondo gris no deseado?
  - Asegurate que has añadido un rectángulo detras de tu elemento botón, y que éste sea del mismo color que el fondo

- ¿Elementos incorrectos?
  - Asegurate que has nombrado tus elementos correctamente en Figma
    - Ve [Dando formato a tu diseño de Figma, &sect;1](#formatting-1)

- ¿La ventana es más grande que la pantalla?
  - Reduce el tamaño de tus elementos en Figma

- ¿Los archivos no se generan?
  - Reinicia Tkinter Designer
  - Vuelve a checkear el URL y el Token Access
  - Asegurate que tu diselo tiene un Frame

- ¿Algo más?
  - [Reportar problemas no mencionados aquí en GitHub](https://github.com/ParthJadhav/Tkinter-Designer/issues/new)
