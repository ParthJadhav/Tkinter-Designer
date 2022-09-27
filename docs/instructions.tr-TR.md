# Tkinter Designer Nasıl Kullanılır
___

## İçindekiler

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
- [Python'u burdan indirebilirsiniz.](https://www.python.org/downloads)  
- [Burda ise Python'u çeşitli işletim sistemlerine indirmeye yarayacak bir rehber var.](https://wiki.python.org/moin/BeginnersGuide/Download)

*Bu rehberden sonra Python'un paket yükleyicisi olan "pip"i kullanacaksınız, bu yüzden Python'u sistem yoluna eklemeniz gerekebilir.*

___
<br>

<a id="getting-started-2"></a>

## 2. Tkinter Designer'ı Yükleyin

*Üç yol*

1. `pip install tkdesigner`

2. Install [poetry](https:python-poetry.org)
   - `poetry new <gui_proje_ismi> && cd <gui_proje_ismi>`
   - `poetry add tkdesigner`
   - `poetry install`

3. Tkinter Designer'ı kaynak kodundan çalıştırmak için aşağıdaki adımları izleyin.

   1. Tkinter Designer'ın kaynak kodunu GIT kullanarak veya manuel olarak indirin.

      ` git clone https://github.com/ParthJadhav/Tkinter-Designer.git `

   2. Çalışma alanınızı Tkinter Designer olarak değiştirin.

      `cd tkinter-designer`

   3. Bunları çalıştırarak gerekenleri indirin.

      - `pip install -r requirements.txt`
         - O an "pip" çalışmıyorsa şu komutları deneyin:
         - `pip3 install -r requirements.txt`
         - `python -m pip install -r requirements.txt`
         - `python3 -m pip install -r requirements.txt`
         - Eğer halen çalışmıyorsa Python'un sistem yoluna eklendiğinden emin olun.

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
   - Sonraki bölüm, Tkinter Designer girişi için gerekli biçimlendirmeyi kapsar.
     - [Burada yeni başlayanlar için Figma öğretici serisi var.](https://www.youtube.com/watch?v=Cx2dkpBxst8&list=PLXDU_eVOJTx7QHLShNqIXL1Cgbxj7HlN4)
     - [Figma'nın resmi YouTube kanalı.](https://www.youtube.com/c/Figmadesign/featured)
     - [Figma yardım servisi.](https://help.figma.com/hc/en-us)

<br><br>

<a id="formatting-1"></a>

# Figma Tasarımınızı Biçimlendirme <small>[[Top](#table-of-contents)]</small>

## 1. Referans

<br>

### İsimlendirme Önemlidir

| Figma Element İsmi | Tkinter Elementi |
| --- | --- |
| Button | Button |
| Line | Line |
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
   - Resimler, şekiller ve resimler kullanılarak oluşturulabilir.
   - Eğer birden fazla şekil veya resim kullandıysanız, önce hepsini seçip ardından <kbd>CTRL/&#8984; + G</kbd> kısayolu ile gruplandırmanız gerekir.
   - Bundan sonra elementi veya grubu "Image" olarak isimlendirin.
<br><br>

3. **Yazı (Normal Yazı)**
   - <kbd>T</kbd> tuşunu kullanarak yazı aracını aktif edin. Ardından istediğiniz yazıyı girin
   - Tkinter Designer'da yazının kullanımı için yeniden isimlendirilmesine gerek yoktur
   - <kbd>Return</kbd>  ya da  <kbd>Enter</kbd> tuşuna basarak sonraki satıra ilerleyin.
<br><br>

4. **Giriş (Tek Satır Kullanıcı Input'u)**
   - <kbd>R</kbd> tuşu ile Rectangle(Dikdörtgen) aracını aktive edin
   - Diktörtgeni beğeninize göre ayarlayın
   - Dikdörtgenin "TextBox" olarak adlandırıldığından emin olun
<br><br>

5. **Yazı Alanı (Çoklu Kullanıcı Input)**
   - <kbd>R</kbd> tuşu ile Rectangle(Dikdörtgen) aracını aktive edin
   - Diktörtgeni beğeninize göre ayarlayın
   - Dikdörtgenin "TextArea" olarak adlandırıldığından emin olun

6. **Dikdörtgen**
   - <kbd>R</kbd> tuşu ile Rectangle(Dikdörtgen) aracını aktive edin
   - Diktörtgeni beğeninize göre ayarlayın
   - Dikdörtgenin "Rectangle" olarak adlandırıldığından emin olun
<br><br>

7. **Normal Buton**
   - Buton olarak kullanmak için bir rectangle(dikdörtgen) ekleyin
     - Opsiyonel: Buton için bir yazı ekleyin
   - Butonu(Rectangle), ve herhangi bir yazıyı seçin,  ardından onları <kbd>CTRL/&#8984; + G</kbd> ile guruplayın
   - Grubu "Button" olarak adlandırın

#### Herhangi bir problemde [bu videoyu](https://youtu.be/Qd-jJjduWeQ) referans alın

<br><br>

8. **Köşeli Buton**
   - Buton olarak kullanmak için bir rectangle(dikdörtgen) ekleyin
     - Opsiyonel: Buton için bir yazı ekleyin
   - Diktörtgene sağ taraftan kenar-yumuşatma ekleyerek kenarlarını yuvarlayın. [Daha fazlasına ulaşın](https://help.figma.com/hc/en-us/articles/360050986854-Adjust-corner-radius-and-smoothing)
   - Butonunuz ile aynı boyutta bir diktörtgen oluşturun. Onu yuvarlatmayın.
   - Dikdörtgeninizin rengini arkaplan ile eşleşmesi için değiştirin
   - Şimdi yeni oluşturulan dikdörtgeni ana düğmenin(dikdörtgenin) altına taşıyın.
   - Butonu, dikdörtgeni ve herhangi opsiyonel yazıyı seçin ve onları <kbd>CTRL/&#8984; + G</kbd> ile gruplandırın
   - Grubu "Button" olarak adlandırın.

#### Herhangi bir problemde [bu videoyu](https://youtu.be/Qd-jJjduWeQ) referans alın

<br><br>

<a id="Using-Tkinter-Designer"></a>

# Tkinter Designer'ı Kullanma <small>[[Top](#table-of-contents)]</small>

## Gerekli Girdiler

TKinter Designer'ı kullanabilmek için bazı girdileri toplamanız gerekmektedir.

<a id="using-1"></a>

### 1. Kişisel Erişim Tokenı

1. Figma hesabınıza girin
2. Ayarlara gidin
3. **Account** sekmesinde, **Personal access tokens** kısmına kadar kaydırın
4. Giriş formu için erişim tokeninizin ismini girin ve <kbd>Enter</kbd> tuşuna basın
5. Kişisel erişim tokeniniz oluşturalacak.
   - Bu tokeni kopyalayın ve güvenli bir yerde saklayın.
   - **Bu tokenı kopyalamak için başka şansınız olmayacak.**

<a id="using-2"></a>

### 2. Dosya URL'nizi Elde Etme

1. Figma tasarım dosyanızda üst menüden **Share** butonuna, ardından **&#x1f517; Copy link**'e tıklayın

<a id="using-cli"></a>

## CLI'ı Kullanma

CLI'yı kullanmak paketi yüklemek ve CLI aracını çalıştırmak kadar kolaydır.

### PyPi'den

Verilerinizle $FILE_URL & $FIGMA_TOKEN değiştirerek aşağıdaki komutu test olarak kullanabilirsiniz. Eğer linke ve tokena ulaşamadıysanız [**Gerekli Girdiler**](#using-1) kısmına bakın.

``` bash
pip install tkdesigner

tkdesigner $FILE_URL $FIGMA_TOKEN
```

### Kaynaktan

CLI'ı kaynak kodundan kullanmak için depoyu klonlamanız ve ardından aşağıdaki talimatları izlemeniz gerekir.

Verilerinizle $FILE_URL & $FIGMA_TOKEN değiştirerek aşağıdaki komutu test olarak kullanabilirsiniz. Eğer linke ve tokena ulaşamadıysanız [**Gerekli Girdiler**](#using-1) kısmına bakın.

```bash
$ python -m tkdesigner.cli $FILE_URL $FIGMA_TOKEN

# To learn more about how to use the cli, pass the --help flag
$ python -m tkdesigner --help
```

### Çıktı

Varsayılan olarak GUI kodu build/gui.py dosyasına yazılacak. Çıktı yolunu `-o` ile değiştirebilirsiniz.

Oluşturulan GUI'yi çalıştırmak için GUI'yi oluşturduğunuz konuma gidin ve herhangi normal bir Tkinter GUI'si çalıştırır gibi çalıştırın.

```bash
cd build
python3 gui.py
```

<a id="using-gui"></a>

## GUI'yi Kullanma

### Sıradaki adımları yapmadan önce Tkinter Designer'ı açın

<br>

1. TKinter Designer GUI'sini aşağıdaki kod yardımıyla açın

```
cd Tkinter-Designer
cd gui
python3 gui.py
```

2. *kişisel erişim tokenı*'nı Tkinter Designer'daki **Token ID** kısmına yapıştırın.
3. Tkinter Designer'da linki **File URL** kısmına yapıştırın
4. Dosya gezgininden bir dosya açmak için **Output Path**'a tıklayın
5. Bir çıktı yolu seçin ve **Select Folder**'a basın
6. **Generate**'e tıklayın

Tkinter Designer'ın çıktı dosyaları, seçtiğiniz dizine, **build** adlı yeni bir klasöre yerleştirilecektir. Tebrikler, şimdi Tkinter GUI'nizi Tkinter Designer kullanarak oluşturdunuz!

<br><br>

<a id="Troubleshooting"></a>

# Sorun Giderme <small>[[Top](#table-of-contents)]</small>

- Elementler görünmüyor mu? Yanlış mı yerleştirilmiş?
  - Lütfen Figma dosyasındaki elementlerin doğru isimlendirildiğinden emin olun. * See [Formatting Your Figma Design, &sect;1](#formatting-1)

- Butonun istenmeyen bir gri arka planı mı var?
  - Buton elementinizin arkasına dikdörtgen eklediğinizden ve dolgu renginin arka plan rengiyle aynı olduğundan emin olun.

- Yanlış elementler?
  - Figmada elementinizi doğru isimlendirdiğinizden emin olun
    - Şu kısma bakın: [Figma Tasarımınızı Biçimlendirme, &sect;1](#formatting-1)

- Pencere ekranınızdan daha mı büyük?
  - Figma'da elementlerinizin boyutunu düşürün

- Dosya oluşturulmuyor mu?
  - Tkinter Designer'ı yeniden başlatın
  - Token'ı ve URL'yi iki kez kontrol edin
  - Tasarımınızın bir Frame'e(çerçeve) sahip olduğundan emin olun

- Başka bir şey?
  - [GitHub'da burda listelenmeyen sorunları bildirin](https://github.com/ParthJadhav/Tkinter-Designer/issues/new)
