# 如何使用 Tkinter Designer

#### 翻译:
- [English](/docs/instructions.md)
- [Français](/docs/instructions.fr-FR.md)
- [ગુજરાતી](docs/instructions.gu-GU.md)

___

## 目录:
1. [**入门**](#入门-top)
   1. [安装Python](#getting-started-1)
   2. [Install Tkinter Designer](#getting-started-2)
   3. [做一个 Figma Account](#getting-started-3)
   
2. [**格式化你的 Figma Design**](#格式化你的-figma-设计top)
   1. [参考](#formatting-1)
   2. [元素指南](#formatting-2)
   
3. [**使用 Tkinter Designer**](#使用-tkinter-designer-top)
   1. [Personal Access Token](#using-1)
   2. [File URL](#using-2)
   3. [测试您生成的代码](#using-3)
   
4. [**故障排除**](#故障排除-top)

<br><br>

# 入门 <small>[[Top](#目录)]</small>

<a id="getting-started-1"></a>
## 1.安装Python
在使用 Tkinter Designer 之前，您需要安装 Python。 
* [这是 Python 下载页面的链接。](https://www.python.org/downloads)  
* [这是在各种操作系统上安装 Python 的有用指南。](https://wiki.python.org/moin/BeginnersGuide/Download)

*在本指南的后面部分，您将使用 Python 包安装程序 (pip)，这可能需要您将 Python 添加到系统 PATH 中。*

___
<br>

<a id="getting-started-2"></a>
## 2. 安装 Tkinter 设计器
安装 Python 后，您可以从 [官方存储库](https://github.com/ParthJadhav/Tkinter-Designer) 下载 Tkinter Designer。

在右侧边栏上，单击最新版本，然后在 **Assets** 下，选择 `tkinter_designer.exe`。 下载完可执行文件后，您就可以运行程序了！

*要从源代码运行 Tkinter Designer，请按照以下说明进行操作。*

1. 下载Tkinter Designer的源文件

2. 将源文件解压到系统目录
   
3. 在此目录中打开终端/命令提示符
    * 您可以使用 `cd` 命令导航到此文件夹。
    * 您也可以使用带有内置终端的 IDE，例如 [Visual Studio Code](https://code.visualstudio.com/)。

4. 通过运行`pip install -r requirements.txt`安装必要的依赖项
    * 如果 pip 不起作用，还可以尝试以下命令：
      * `pip3 install -r requirements.txt`
      * `python -m pip install -r requirements.txt`
      * `python3 -m pip install -r requirements.txt`
    * 如果这仍然不起作用，请确保将 Python 添加到 PATH。
  
5. 你可以通过运行`python tkinter_designer.py`来运行Tkinter Designer

___
<br>

<a id="getting-started-3"></a>
## 3. 创建一个 Figma 帐户
1. 在网页浏览器中，导航至 [figma.com](https://www.figma.com/) 并点击“注册”
2. 输入您的信息并验证您的电子邮件
3. 创建一个新的 Figma Design 文件
4. 开始制作你的 GUI
    * 下一节介绍 Tkinter 设计器输入所需的格式。
      * [这是面向初学者的官方 Figma 教程系列。](https://www.youtube.com/watch?v=Cx2dkpBxst8&list=PLXDU_eVOJTx7QHLShNqIXL1Cgbxj7HlN4)
      * [这是 Figma 的官方 YouTube 频道。](https://www.youtube.com/c/Figmadesign/featured)
      * [这是 Figma 帮助中心。](https://help.figma.com/hc/en-us)

<br><br>

# 格式化你的 Figma 设计<small>[[Top](#目录)]</small>

<a id="formatting-1"></a>
## 1. 参考
<br>

### 命名很重要

| Figma 元素名称 | Tkinter 元素 |
| --- | --- |
| Button | Button |
| Rectangle | Rectangle |
| TextArea | Text Area |
| TextBox | Entry |
| Background | Canvas.Image() |

<br>

Tkinter Designer 生成的代码基于 Figma 设计中的元素名称，因此，您需要相应地命名元素。 在 Figma 中，通过在“图层”面板中双击元素来重命名元素。

___
<br>

<a id="formatting-2"></a>
## 2. 元素指南
<br>

1. **首先，创建一个框架作为您的 Tkinter 窗口。**
<br><br>

2. **创建背景**
   * 可以使用形状和/或图像创建背景
    * 如果您使用多个形状/图像，您必须通过选择它们并按下将它们组合在一起 <kbd>CTRL/&#8984; + G</kbd>
<br><br>

3. **文本（普通文本）**
   * 使用 <kbd>T</kbd> 键激活文本工具，然后根据需要添加文本
    * 在 Tkinter Designer 中使用时不必重命名文本
    * 明确按下 <kbd>Return</kbd> 或 <kbd>Enter</kbd> 键移动到下一行。
<br><br>

4. **输入（单行用户输入）**
    * 使用 <kbd>R</kbd> 激活矩形工具
    * 根据您的喜好调整矩形
    * 确保矩形命名为“TextBox”
<br><br>

5. **文本区域（多行用户输入）**
    * 使用 <kbd>R</kbd> 激活矩形工具
    * 根据您的喜好调整矩形
    * 确保矩形命名为“TextArea”
<br><br>

6. **矩形**
    * 使用 <kbd>R</kbd> 激活矩形工具
    * 根据您的喜好调整矩形
    * 确保矩形被命名为“矩形”
<br><br>

7. **按钮**
    * 添加一个元素作为 GUI 中的按钮
      * *可选：为按钮添加文本*
    * 在按钮下方的图层上创建一个矩形
    * 更改矩形的颜色以匹配背景
    * 选择按钮、矩形和任何可选文本，然后将它们与<kbd>CTRL/&#8984; + G</kbd>
   * 将组命名为“按钮”
<br><br>

# 使用 Tkinter Designer <small>[[Top](#目录)]</small>

### 在执行以下步骤之前打开 Tkinter Designer。
<br>

<a id="using-1"></a>
## 1. 个人访问令牌
1. 登录您的 Figma 帐户
2. 导航到设置
3. 在 **Account** 选项卡中，向下滚动到 **Personal access tokens**
4. 在条目表单中输入您的访问令牌的名称，然后按 <kbd>Enter</kbd>
5. 您的个人访问令牌将被创建。
    * 复制此令牌并将其保存在安全的地方。
    * **您将不会再有机会复制此令牌。**
6. 将您的个人访问令牌粘贴到 Tkinter Designer 中的 **Token ID** 表单中
___
<br>

<a id="using-2"></a>
## 2. 文件地址
1. 在您的 Figma 设计文件中，单击顶部栏中的 **Share** 按钮，然后单击 **&#x1f517; 复制链接**
2. 将链接粘贴到 Tkinter Designer 中的 **File URL** 表单中
___
<br>

<a id="using-3"></a>
## 3. 测试你生成的代码
1. 在 Tkinter Designer 中，单击 **Output Path** 表单打开文件浏览器
2. 选择一个输出路径并点击**Select Folder**
3. 按**生成**

Tkinter Designer 的输出文件将放置在您选择的目录中，位于名为 **generated_code** 的新文件夹中。 恭喜，您现在已经使用 Tkinter Designer 创建了您的 Tkinter GUI！

<br><br>

# 故障排除 <small>[[Top](#目录)]</small>

* 元素不可见？ 放错地方了？
   * 请确保您的顶级 Frame 的 X 和 Y 坐标位于 (0, 0)
     * 检查右侧栏，在 **Design** 下

* 按钮有意外的灰色背景？
   * 确保您在按钮元素后面添加了一个矩形，并且其填充颜色与背景的相同

* 不正确的元素？
   * 确保您在 Figma 中正确命名了元素
     * 请参阅 [格式化您的 Figma 设计，&sect;1](#formatting-1)

* 窗口比屏幕大？
   * 减少 Figma 中元素的大小

* 文件没有生成？
   * 重启 Tkinter 设计器
   * 仔细检查令牌和 URL
   * 确保你的设计有一个框架

* 还有什么？
   * [报告未在 GitHub 上列出的问题](https://github.com/ParthJadhav/Tkinter-Designer/issues/new)
