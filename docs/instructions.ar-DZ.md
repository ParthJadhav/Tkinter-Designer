<div dir="rtl">

# كيفية استعمال Tkinter Designer

___

## Table of Contents

1. [**البدء**](#getting-started-1)
   1. [تثبيت Python](#getting-started-1)
   2. [تثبيت Tkinter Designer](#getting-started-2)
   3. [إنشاء حساب Figma](#getting-started-3)

2. [**تنسيق تصميم Figma**](#formatting-1)
   1. [المرجع](#formatting-1)
   2. [دليل العناصر](#formatting-2)

3. [**إستعمال Tkinter Designer**](#Using-Tkinter-Designer)
   1. [Access Token الشخصي](#using-1)
   2. [الحصول على URL الملف](#using-2)
   3. [استعمال CLI](#using-cli)
   4. [استعمال GUI](#using-gui)

4. [**Troubleshooting**](#Troubleshooting)

<br><br>

# البدء <small>[[الأعلى](#table-of-contents)]</small>

<a id="getting-started-1"></a>

## 1. تثبيت Python

قبل استعمال Tkinter Designer, ستحتاج إلى تثبيت Python.

- [رابط تثبيت Python](https://www.python.org/downloads)
- [رابط مفيد لثبيت Python على أنظمة تشغيل مختلفة](https://wiki.python.org/moin/BeginnersGuide/Download)

*لاحقا في هذا الدليل، ستستعمل Package Installer for Python (pip), والذي قد يتطلب منك إضافة Python إلى نظام PATH*

___
<br>

<a id="getting-started-2"></a>

## 2. تثبيت Tkinter Designer

*ثلاث خيارات:*

1. `pip install tkdesigner`

2. تثبيت [poetry](https:python-poetry.org)
    - `poetry new gui_project_name && cd gui_project_name`
    - `poetry add tkdesigner`
    - `poetry install`

3. لتشغيل Tkinter Designer من source code, اتبع الخطوات أدناه.

    1. تحميل كود Tkinter Designer إما يدويًا أو بواسطة git.

      `git clone https://github.com/ParthJadhav/Tkinter-Designer.git`

    2. فتح مجلد Tkinter Designer (تغيير المجلد الحالي)

      `cd tkinter-designer`

    3. تثبيت الملحقات الضرورية

      - `pip install -r requirements.txt`
         - في حالة عطب في pip جرب الأوامر التالية:
         - `pip3 install -r requirements.txt`
         - `python -m pip install -r requirements.txt`
         - `python3 -m pip install -r requirements.txt`
         - وإن كان هذا لا يزال يعمل، تأكد من أن Python مُضاف إلى PATH.

   . هذا سيقوم بتثبيت كل العناصر الضرورية لعمل Tkinter Designer. قبل استعمال Tkinter Designer ستحتاج إلى إنشاء ملف Figma بالإرشادات التالية.

   If you already have created a file then skip to [**Using Tkinter Designer**](#Using-Tkinter-Designer) Section.

   إذا أنشأت الملف بالفعل، فانتقل إلى قسم [**استعمال Tkinter Designer**](#Using-Tkinter-Designer)

___
<br>

<a id="getting-started-3"></a>

## 3. إنشاء حساب Figma

1. باستعمال متصفح ويب إذهب إلى [figma.com](https://www.figma.com/) وانقر على 'Sign up'
2. أدخل معلوماتك وتحقق من بريدك الإلكتروني
3. قم بإنشاء ملف تصميم Figma جديد
4. إبدأ بإنشاء الواجهة
    - القسم الموالي يغطي التنسيق المطلوب لإدخال Tkinter Designer
    - [هنا الدورة التعليمية الرسمية للبرنامج Figma](https://www.youtube.com/watch?v=Cx2dkpBxst8&list=PLXDU_eVOJTx7QHLShNqIXL1Cgbxj7HlN4)
    - [هنا القناة الرسمية في اليوتوب Figma](https://www.youtube.com/c/Figmadesign/featured)
    - [هنا مقر المساعدة Figma](https://help.figma.com/hc/en-us)

<br><br>

<a id="formatting-1"></a>

# تنسيق تصميم Figma <small>[[الأعلى](#table-of-contents)]</small>

## 1. المرجع

<br>

### التسمية مهمة

| اسم العنصر في Figma | عنصر Tkinter |
| --- | --- |
| Button | Button |
| Line | Line |
| Rectangle | Rectangle |
| TextArea | Text Area |
| TextBox | Entry |
| Image | Canvas.Image() |

<br>

يعتمد الكود الذي تم إنشاؤه بواسطة Tkinter Designer على أسماء العناصر من تصميم Figma الخاص بك، وعلى هذا النحو، تحتاج إلى تسمية العناصر الخاصة بك وفقًا لذلك. في Figma ، أعد تسمية عناصرك بالنقر عليها في لوحة Layers.
___
<br>

<a id="formatting-2"></a>

## 2. دليل العناصر

<br>

1. **أولاً، قم بإنشاء Frame والتي ستكون بمثابة نافذة Tkinter**
<br><br>

2. **إضافة صور**
   - يمكن إنشاء الصور باستخدام الأشكال و / أو الصور
   - إذا كنت تستخدم أشكالًا / صورًا متعددة ، فيجب عليك تجميعها معًا عن طريق تحديدها جميعًا والضغط عليها <kbd>CTRL/&#8984; + G</kbd>
   - وبعد ذلك، قم بتسمية العنصر أو المجموعة ب "Image".
<br><br>

3. **نص (نص عادي)**
   - استخدم مفتاح <kbd> T </kbd> لتنشيط أداة Text ، ثم أضف النص حسب الرغبة
   - لا يلزم إعادة تسمية النص لاستخدامه في Tkinter Designer
   - اضغط على مفتاح <kbd> Return </kbd> أو <kbd> Enter </kbd> للانتقال إلى السطر التالي.
<br><br>

4. **الإدخال (إدخال مستخدم أحادي السطر)**
   - قم بتنشيط أداة Rectangle باستخدام <kbd> R </kbd>
   - اضبط المستطيل حسب رغبتك
   - تأكد من تسمية المستطيل "TextBox"
<br><br>

5. **منطقة النص (إدخال مستخدم متعدد الأسطر)**
   - قم بتنشيط أداة Rectangle باستخدام <kbd> R </kbd>
   - اضبط المستطيل حسب رغبتك
   - تأكد من تسمية المستطيل "TextArea"

6. **Rectangle**
   - قم بتنشيط أداة Rectangle باستخدام <kbd> R </kbd>
   - اضبط المستطيل حسب رغبتك
   - تأكد من تسمية المستطيل "Rectangle".
<br><br>

7. **زر عادي**
    - أضف مستطيلاً ليكون بمثابة زر في واجهة المستخدم
    - اختياري: أضف نصًا للزر
    - حدد الزر (مستطيل) ، وأي نص اختياري ، ثم قم بتجميعها باستخدام <kbd> CTRL / & # 8984؛ + G </kbd>
    - قم بتسمية المجموعة "Button"

<br><br> إلجأ إلى هذا [الفيديو](https://youtu.be/Qd-jJjduWeQ) إذا واجهت أي مشاكل

8. **زر مدور**
    - أضف مستطيلًا ليكون بمثابة زر في واجهة المستخدم
    - اختياري: أضف نصًا للزر
    - إجعلها مدورة بإضافة corner radius عن طريق تحديد المستطيل وإضافة corner radius من الجهة اليمنى. [إقرأ المزيد عنها](https://help.figma.com/hc/en-us/articles/360050986854-Adjust-corner-radius-and-smoothing)
    - قم بإنشاء مستطيل بنفس حجم الزر الخاص بك. لا تجعلها مدورة
    - قم بتغيير لون المستطيل ليطابق الخلفية
    - الآن قم بتحريك المستطيل الذي تم إنشاؤه حديثًا أسفل الزر الرئيسي (مستطيل)
    - حدد الزر والمستطيل وأي نص اختياري ، ثم قم بتجميعها باستخدام <kbd> CTRL / & # 8984؛ + G </kbd>
    - قم بتسمية المجموعة "Button"

#### إلجأ إلى هذا [الفيديو](https://youtu.be/Qd-jJjduWeQ) إذا واجهت أي مشاكل

<br><br>

<a id="Using-Tkinter-Designer"></a>

# استعمال Tkinter Designer <small>[[الأعلى](#table-of-contents)]</small>

## المدخلات المطلوبة

هناك بعض المدخلات التي ستحتاج إلى جمعها لتتمكن من استخدام Tkinter Designer.

<a id="using-1"></a>

### 1. Access Token الشخصي

1. قم بتسجيل الدخول إلى حساب Figma الخاص بك
2. انتقل إلى الإعدادات
3. في علامة التبويب **الحساب** ، قم بالتمرير لأسفل إلى **Personal Access tokens**
4. أدخل اسم access token الخاص بك في نموذج الإدخال واضغط على <kbd> Enter </kbd>
5. سيتم إنشاء access token الخاص بك.
   - انسخ هذا access token واحتفظ به في مكان آمن.
   - **لن تحصل على فرصة أخرى لنسخ هذا token.**

### 2. الحصول على URL الملف

1. في ملف تصميمك Figma، إضغط على زر **Share** في القسم العلوي، ثم على **&#x1f517; Copy link**

<a id="using-cli"></a>

## باستعمال CLI

يعد استخدام CLI أمرًا بسيطًا مثل تثبيت الحزمة وتشغيل أداة CLI.

### من PyPi

يمكنك استخدام الأوامر أدناه كاختبار باستبدال $FILE_URL و $FIGMA_TOKEN ببياناتك. إذا لم يكن لديك token والرابط فارجع إلى [**المدخلات المطلوبة**](#using-1).

``` bash
pip install tkdesigner
tkdesigner $FILE_URL $FIGMA_TOKEN
```

### من Source

لاستخدام CLI من الكود المصدري ، تحتاج إلى clone repository ثم اتباع الإرشادات أدناه.

يمكنك استخدام الأوامر أدناه كاختبار باستبدال $FILE_URL و $FIGMA_TOKEN ببياناتك. إذا لم يكن لديك token والرابط فارجع إلى [**المدخلات المطلوبة**](#using-1).

```bash
$ python -m tkdesigner.cli $FILE_URL $FIGMA_TOKEN
# To learn more about how to use the cli, pass the --help flag
$ python -m tkdesigner --help
```

### المخرجات

بشكل تلقائي، كود واجهة المستخدم سيكتب إلى build/gui.py. تستطيع تحديد path المخرج باستعمال flag `-o` مع path.

لتشغيل واجهة المستخدم المنتجة، قم بcd إلى path الذي ستكتب إليه (build/ مثلاً) وقم بتشغيله مثل أي واجهة مستخدم Tkinter.

```bash
cd build
python3 gui.py
```

<a id="using-gui"></a>

## استعمال واجهة المستخدم

### افتح Tkinter Designer قبل تنفيذ الخطوات التالية

<br>

1. افتح Tkinter Designer GUI عن طريق

```
cd Tkinter-Designer
cd gui
python3 gui.py
```

2. إنسخ *access token الشخصي إلى* **Token ID** في Tkinter Designer
3. إنسخ الرابط إلى **File URL** في Tkinter Designer
4. إضغط على **Output Path** لفتح متصفح الملفات
5. إختر path مخرجات وإضغط على **Select Folder**
6. إضغط على **Generate**

سيتم وضع ملفات الإخراج من Tkinter Designer في path الذي اخترته ، داخل مجلد جديد يسمى **build**. تهانينا ، لقد قمت الآن بإنشاء Tkinter GUI باستخدام Tkinter Designer!

<br><br>

<a id="Troubleshooting"></a>

# Troubleshooting <small>[[الأعلى](#table-of-contents)]</small>

- العناصر غير مرئية؟ في غير محلها؟
  - يرجى التأكد من أن ملف Figma الخاص بك يحتوي على عناصره المسماة بشكل صحيح. * أنظر إلى [تنسيق تصميم Figma, &sect;1](#formatting-1)

- الزر له خلفية رمادية من غير قصد؟
  - تأكد من إضافة مستطيل خلف عنصر الزر الخاص بك ، وأن لون التعبئة الخاص به هو نفسه لون الخلفية

- عناصر غير صحيحة؟
  - تأكد من تسمية العناصر الخاصة بك بشكل صحيح في Figma
    - أنظر إلى [تنسيق تصميم Figma, &sect;1](#formatting-1)

- النافذة أكبر من الشاشة؟
  - قم بتصغير العناصر الخاصة بك في Figma

- الملفات لم تُولّد؟
  - أعد تشغيل Tkinter Designer
  - تحقق مرة أخرى access token  وعنوان URL
  - تأكد من أن التصميم الخاص بك يحتوي على Frame

- شيء آخر؟
  - [الإبلاغ عن المشكلات غير المدرجة هنا على GitHub](https://github.com/ParthJadhav/Tkinter-Designer/issues/new)

</div>
