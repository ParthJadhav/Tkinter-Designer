# Tkinter Designer Nasıl Kullanılır

#### Translations:
- [简体中文](/docs/instructions.zh-CN.md)
- [English](/docs/instructions.md)
- [ગુજરાતી](docs/instructions.gu-GU.md)

___

## İçindekiler:
1. [**Başlarken**](#getting-started-1)
   1. [Python'u Kurun](#getting-started-1)
   2. [Tkinter Designer'ı Yükleyin](#getting-started-2)
   3. [Bir Figma Hesabı Oluşturun](#getting-started-3)
   
2. [**Figma Tasarımınızı Biçimlendirme**](#formatting-1)
   1. [Referans](#formatting-1)
   2. [Element Kılavuzu](#formatting-2)
   
3. [**Tkinter Designer'ı Kullanma**](#Using-Tkinter-Designer)
   1. [Kişisel Erişim Tokenı](#using-1)
   2. [Dosya URL'nizi Elde Etme](#using-2)
   3. [CLI'ı Kullanma](#using-cli)
   4. [GUI'yi Kullanma](#using-gui)
   
4. [**Sorun Giderme**](#Troubleshooting)

<br><br>

# Başlarken <small>[[Top](#table-of-contents)]</small>

<a id="getting-started-1"></a>
## 1. Python'u Kurun
Tkinter Designer'ı kullanmaya başlamadan önce Python'u kurmanız gerekmektedir.
* [Python'u burdan indirebilirsiniz.](https://www.python.org/downloads)  
* [Burda ise Python'u çeşitli işletim sistemlerine indirmeye yarayacak bir rehber var.](https://wiki.python.org/moin/BeginnersGuide/Download)

*Bu rehberden sonra Python'un paket yükleyicisi olan "pip"i kullanacaksınız, bu yüzden Python'u sistem yoluna eklemeniz gerekebilir.*

___
<br>

<a id="getting-started-2"></a>
## 2. Tkinter Designer'ı Yükleyin

*Üç yol*

1. `pip install tkdesigner`

2. Install [poetry](https:python-poetry.org)
   * `poetry new <gui_proje_ismi> && cd <gui_proje_ismi>`
   * `poetry add tkdesigner`
   * `poetry install`

3. Tkinter Designer'ı kaynak kodundan çalıştırmak için aşağıdaki adımları izleyin.

   1. Tkinter Designer'ın kaynak kodunu GIT kullanarak veya manuel olarak indirin.

      ` git clone https://github.com/ParthJadhav/Tkinter-Designer.git `

   2. Çalışma alanınızı Tkinter Designer olarak değiştirin.

      `cd tkinter-designer`
      
   3. Bunları çalıştırarak gerekenleri indirin.

      * `pip install -r requirements.txt`
         * O an "pip" çalışmıyorsa şu komutları deneyin:
         * `pip3 install -r requirements.txt`
         * `python -m pip install -r requirements.txt`
         * `python3 -m pip install -r requirements.txt`
         * Eğer halen çalışmıyorsa Python'un sistem yoluna eklendiğinden emin olun.
   
   Bu tüm gerekli şeyleri ve Tkinter Designer'ı kuracaktır. Tkinter Designer'ı kullanmadan önce aşağıdaki yönergeler ile bir Figma dosyası oluşturmanız gerekmektedir.

   Eğer zaten oluşturduysanız [**Tkinter Designer'ı Kullanma**](#Using-Tkinter-Designer) kısmına atlayabilirsiniz.

___
<br>

<a id="getting-started-3"></a>
## 3. Bir Figma Hesabı Oluşturma
1. Tarayıcınızdan [figma.com](https://www.figma.com/) adresine gidin ve "Üye Ol // Sign Up" tuşuna tıklayın.
2. Bilgilerinizi girin ardından email hesabınızı doğrulayın
3. Yeni bir Figma Tasarım Dosyası oluşturun
4. Arayüzünüzü yapmaya başlayın
   * Sonraki bölüm, Tkinter Designer girişi için gerekli biçimlendirmeyi kapsar.
     * [Burada yeni başlayanlar için Figma öğretici serisi var.](https://www.youtube.com/watch?v=Cx2dkpBxst8&list=PLXDU_eVOJTx7QHLShNqIXL1Cgbxj7HlN4)
     * [Figma'nın resmi YouTube kanalı.](https://www.youtube.com/c/Figmadesign/featured)
     * [Figma yardım servisi.](https://help.figma.com/hc/en-us)

<br><br>

<a id="formatting-1"></a>
# Figma Tasarımınızı Biçimlendirme <small>[[Top](#table-of-contents)]</small>

## 1. Referans
<br>

### İsimlendirme Önemlidir

| Figma Element İsmi | Tkinter Elementi |
| --- | --- |
| Button | Button |
| Rectangle | Rectangle |
| TextArea | Text Area |
| TextBox | Entry |
| Image | Canvas.Image() |

<br>

Tkinter Designer'ın oluşturduğu kodlar Figma tasarımınızdaki element isimlerden gelir, bu yüzden isimlendirmeyi doğru yapmanız gerekir. Figma'da elementleri kontrol panelindeki katmanlar paneli aracılığıyla çift tıklayarak isimlendirebilirsiniz.

___
<br>

<a id="formatting-2"></a>
## 2. Element Kılavuzu
<br>

1. **Öncelikle, Tkinter Penceresi olarak kullanacağınız bir "frame" oluşturun.**
<br><br>

2. **Resim Ekleme**
   * Resimler, şekiller ve resimler kullanılarak oluşturulabilir.
   * Eğer birden fazla şekil veya resim kullandıysanız, önce hepsini seçip ardından <kbd>CTRL/&#8984; + G</kbd> kısayolu ile gruplandırmanız gerekir.
   * Bundan sonra elementi veya grubu "Image" olarak isimlendirin.
<br><br>

3. **Yazı (Normal Yazı)**
   * <kbd>T</kbd> tuşunu kullanarak yazı aracını aktif edin. Ardından istediğiniz yazıyı girin
   * Tkinter Designer'da yazının kullanımı için yeniden isimlendirilmesine gerek yoktur
   * <kbd>Return</kbd>  ya da  <kbd>Enter</kbd> tuşuna basarak sonraki satıra ilerleyin.
<br><br>

4. **Giriş (Tek Satır Kullanıcı Input'u)**
   * <kbd>R</kbd> tuşu ile Rectangle(Dikdörtgen) aracını aktive edin
   * Diktörtgeni beğeninize göre ayarlayın
   * Dikdörtgenin "TextBox" olarak adlandırıldığından emin olun
<br><br>

5. **Yazı Alanı (Çoklu Kullanıcı Input)**
   * <kbd>R</kbd> tuşu ile Rectangle(Dikdörtgen) aracını aktive edin
   * Diktörtgeni beğeninize göre ayarlayın
   * Dikdörtgenin "TextArea" olarak adlandırıldığından emin olun

6. **Dikdörtgen**
   * <kbd>R</kbd> tuşu ile Rectangle(Dikdörtgen) aracını aktive edin
   * Diktörtgeni beğeninize göre ayarlayın
   * Dikdörtgenin "Rectangle" olarak adlandırıldığından emin olun
<br><br>

7. **Normal Buton**
   * Buton olarak kullanmak için bir rectangle(dikdörtgen) ekleyin
     * Opsiyonel: Buton için bir yazı ekleyin
   * Butonu(Rectangle), ve herhangi bir yazıyı seçin,  ardından onları <kbd>CTRL/&#8984; + G</kbd> ile guruplayın
   * Grubu "Button" olarak adlandırın

#### Herhangi bir problemde [bu videoyu](https://youtu.be/mFjE2-rbpm8?t=275) referans alın

<br><br>

8. **Köşeli Buton** 
   * Buton olarak kullanmak için bir rectangle(dikdörtgen) ekleyin
     * Opsiyonel: Buton için bir yazı ekleyin
   * Diktörtgene sağ taraftan kenar-yumuşatma ekleyerek kenarlarını yuvarlayın. [Daha fazlasına ulaşın](https://help.figma.com/hc/en-us/articles/360050986854-Adjust-corner-radius-and-smoothing)
   * Butonunuz ile aynı boyutta bir diktörtgen oluşturun. Onu yuvarlatmayın.
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
