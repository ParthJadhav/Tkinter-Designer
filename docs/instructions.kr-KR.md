# Tkinter Designer 사용법

___

## 목차

1. [**시작하기**](#getting-started-1)
    1. [Python 설치하기](#getting-started-1)
    2. [Tkinter Designer 설치하기](#getting-started-2)
    3. [Figma 계정 생성하기](#getting-started-3)

2. [**Figma 가이드**](#formatting-1)
    1. [레퍼런스](#formatting-1)
    2. [속성 가이드](#formatting-2)

3. [**Tkinter Designer 사용하기**](#Using-Tkinter-Designer)
    1. [Access Token](#using-1)
    2. [File URL 가져오기](#using-2)
    3. [CLI 사용하기](#using-cli)
    4. [GUI 사용하기](#using-gui)

4. [**문제해결**](#Troubleshooting)

<br><br>

# 시작하기 <small>[[Top](#)]</small>

<a id="getting-started-1"></a>

## 1. Python 설치하기

Tkinter Designer를 사용하기 전에 Python을 설치해야 합니다.
- [여기에서 Python을 설치할 수 있습니다.](https://www.python.org/downloads)
- [다음은 다양한 운영 체제에 Python을 설치하는 데 유용한 가이드입니다.](https://wiki.python.org/moin/BeginnersGuide/Download)

*이 가이드의 뒷부분에서 Python용 Package Installer(pip)를 사용할 것이며, 이 경우 시스템 환경변수에 Python을 추가해야 할 수도 있습니다.*

___
<br>

<a id="getting-started-2"></a>

## 2. Tkinter Designer 설치하기

*세 가지 옵션:*

1. `pip install tkdesigner`

2. [poetry](https:python-poetry.org) 설치
    - `poetry new <gui_project_name> && cd <gui_project_name>`
    - `poetry add tkdesigner`
    - `poetry install`

3. 소스 코드에서 Tkinter Designer를 실행하려면 아래 지침을 따르십시오.

    1. Tkinter Designer의 원본 파일을 수동으로 다운로드하거나 GIT를 사용하여 다운로드합니다.

       ` git clone https://github.com/ParthJadhav/Tkinter-Designer.git `

    2. 작업 디렉토리를 Tkinter Designer로 변경합니다.

       `cd Tkinter-Designer`

    3. 다음을 실행하여 필요한 종속성을 설치합니다.

        - `pip install -r requirements.txt`
            - pip이 작동하지 않는 경우 다음 명령도 사용해 보십시오:
            - `pip3 install -r requirements.txt`
            - `python -m pip install -r requirements.txt`
            - `python3 -m pip install -r requirements.txt`
            - 그래도 작동하지 않으면 환경변수에 Python이 추가되었는지 확인합니다.

   그러면 모든 요구 사항과 Tkinter Designer가 설치됩니다. Tkinter Designer를 사용하기 전에 아래 지침을 사용하여 Figma 파일을 만들어야 합니다.

   파일을 이미 만든 경우 [**Tkinter Designer 사용하기**](#Using-Tkinter-Designer) 섹션으로 건너뜁니다.

___
<br>

<a id="getting-started-3"></a>

## 3. Figma 계정 생성하기

1. 웹 브라우저에서 [figma.com ](https://www.figma.com/)로 이동하여 '가입'을 클릭합니다.
2. 정보를 입력한 다음 이메일 인증을 합니다.
3. 새로운 Figma 파일을 만듭니다.
4. GUI 제작 시작
    - 다음 섹션에서는 Tkinter Designer 입력에 필요한 형식에 대해 설명합니다.
        - [초보자를 위한 공식 피그마 튜토리얼 시리즈입니다.](https://www.youtube.com/watch?v=Cx2dkpBxst8&list=PLXDU_eVOJTx7QHLShNqIXL1Cgbxj7HlN4)
        - [피그마 공식 유튜브 채널입니다.](https://www.youtube.com/c/Figmadesign/featured)
        - [여기가 피그마 도움말입니다.](https://help.figma.com/hc/en-us)

<br><br>

<a id="formatting-1"></a>

# Figma 가이드 <small>[[Top](#목차)]</small>

## 1. 레퍼런스

<br>

### Naming이 중요합니다

| Figma Element Name | Tkinter Element |
| --- | --- |
| Button | Button |
| Line | Line |
| Text | Name it anything |
| Rectangle | Rectangle |
| TextArea | Text Area |
| TextBox | Entry |
| Image | Canvas.Image() |

<br>

Tkinter Designer에서 생성된 코드는 Figma 설계의 요소 이름을 기반으로 하므로 요소 이름을 적절하게 지정해야 합니다. Figma의 레이어 패널에서 요소를 두 번 클릭하여 이름을 바꿉니다.

___
<br>

<a id="formatting-2"></a>

## 2. 속성 가이드

<br>

1. **먼저 Tkinter 창 역할을 할 프레임을 만듭니다.**
   <br><br>

2. **Image**
    - 도형 및/또는 이미지를 사용하여 이미지를 생성할 수 있습니다.
    - 여러 도형/이미지를 사용하는 경우 '모두 선택'을 눌러 그룹화해야 합니다 <kbd>CTRL/&#8984; + G</kbd>
    - 그런 다음 요소 또는 그룹의 이름을 "이미지"로 지정합니다.
      <br><br>

3. **Text (일반 텍스트)**
    - <kbd>T</kbd> 키를 눌러 텍스트 도구를 활성화한 다음 원하는 대로 텍스트 추가합니다.
    - Tkinter Designer에서 사용하기 위해 텍스트 이름을 변경할 필요가 없습니다.
    - 명시적으로 <kbd>Return</kbd> 또는 <kbd>Enter</kbd> 키를 눌러 다음 줄로 이동합니다.
      <br><br>

4. **Entry (사용자의 한 줄 입력)**
    - <kbd>R</kbd>을 사용하여 Rectangle 도구 활성화
    - 원하는 대로 Rectangle 조정
    - Rectangle의 이름이 "TextBox"인지 확인합니다
      <br><br>

5. **Text Area (사용자의 여러줄 입력)**
    - <kbd>R</kbd>을 사용하여 Rectangle 도구 활성화
    - 원하는 대로 Rectangle 조정
    - Rectangle의 이름이 "TextArea"인지 확인합니다

6. **Rectangle**
    - <kbd>R</kbd>을 사용하여 Rectangle 도구 활성화
    - 원하는 대로 Rectangle 조정
    - Rectangle의 이름이 "Rectangle"인지 확인합니다
      <br><br>

7. **Normal Button**
    - GUI에서 button으로 사용할 rectangle 추가
        - 선택 사항: button에 대한 text  추가
    - button(Rectangle)과 옵션으로 text를 선택한 다음 <kbd>CTRL/&#8984; + G</kbd>로 그룹화합니다
    - 그룹 이름을 "Button"으로 지정합니다
      <br><br>

8. **둥근 Button**
    - GUI에서 button으로 사용할 rectangle 추가
        - 선택 사항: button에 text 추가
    - rectangle을 선택하고 오른쪽에서 모서리 반지름을 추가하여 모서리 반지름을 반올림합니다. [자세히 읽어보기](https://help.figma.com/hc/en-us/articles/360050986854-Adjust-corner-radius-and-smoothing)
    - button과 크기가 같은 Rectangle을 만듭니다. 동그랗게 만들지 마세요.
    - 배경과 일치하도록 Rectangle 색상 변경
    - 이제 새로 만든 Rectangle을 기본 button(Rectangle) 아래로 이동합니다.
    - button, Rectangle및 optional text를 선택한 다음 <kbd>CTRL/&#8984; + G</kbd>로 그룹화합니다
    - 그룹 이름을 "Button"으로 지정합니다

#### 문제가 발생하면 [유튜브](https://youtu.be/Qd-jJjduWeQ) 를 참조하십시오

<br><br>

<a id="Using-Tkinter-Designer"></a>

# Tkinter Designer 사용하기 <small>[[Top](#목차)]</small>

## 필수 입력 정보

TKinter Designer를 사용하려면 몇 가지 입력 정보를 수집해야 합니다.

<a id="using-1"></a>

### 1. 개인 액세스 토큰

1. Figma 계정에 로그인합니다
2. 설정으로 이동
3. **Account** 탭에서 **Personal access tokens**으로 스크롤합니다
4. 입력 양식에 액세스 토큰 이름을 입력하고 <kbd>Enter</kbd> 키를 누릅니다
5. 개인 액세스 토큰이 생성됩니다.
    - 이 토큰을 복사하여 안전한 곳에 보관하십시오.
    - **이 토큰을 다시 복사할 수 없습니다.**

<a id="using-2"></a>

### 2. File URL 얻기

1. Figma 디자인 파일에서 상단 바의 **Share** 버튼을 클릭한 다음 **&#x1f517; Copy link**를 클릭합니다.
   <a id="using-cli"></a>

## CLI로 실행하기

CLI를 사용하는 것은 패키지를 설치하고 CLI 도구를 실행하는 것만큼 간단합니다.

### PyPi로 실행하기

$FILE_URL & $FIGMA_TOKEN을 데이터로 대체하여 아래 명령을 테스트로 사용할 수 있습니다. 토큰과 링크가 없으면 [**필수 입력 정보 Section**](#Using-Tkinter-Designer)을 참조하십시오.

``` bash
pip install tkdesigner

tkdesigner $FILE_URL $FIGMA_TOKEN
```

### 소스로 실행하기

소스 코드에서 CLI를 사용하려면 리포지토리를 복제한 다음 아래 지침을 따라야 합니다.

$FILE_URL & $FIGMA_TOKEN을 데이터로 대체하여 아래 명령을 테스트로 사용할 수 있습니다. 토큰과 링크가 없으면 [**필수 입력 정보 Section**](#Using-Tkinter-Designer)을 참조하십시오.

```bash
$ python -m tkdesigner.cli $FILE_URL $FIGMA_TOKEN

# To learn more about how to use the cli, pass the --help flag
$ python -m tkdesigner --help
```

### 결과물

기본적으로 GUI 코드는 build/gui.py 에 기록됩니다. '-o' 플래그를 사용하고 경로를 제공하여 출력 경로를 지정할 수 있습니다.

생성된 GUI를 실행하려면 빌드한 디렉토리(예: build/)에 들어가 Tkinter GUI와 마찬가지로 실행합니다.

```bash
cd build
python3 gui.py
```

<a id="using-gui"></a>

## GUI로 실행하기

### 다음 단계를 수행하기 전에 Tkinter Designer 실행시키기

<br>

1. 다음 명령어를 통해 TKinter Designer GUI를 실행합니다.

```
cd Tkinter-Designer
cd gui
python3 gui.py
```

2. Tkinter Designer의 **Token ID**에 *personal access token*를 추가합니다.
3. Tkinter Designer의 **File URL**에 Figma링크를 추가합니다.
4. **Output Path** 를 통해 저장될 위치를 누릅니다.
5. 생성 경로를 선택하고 다음을 누릅니다. **Select Folder**
6. **Generate**를 누릅니다.

Tkinter Designer의 출력 파일은 선택한 디렉토리의 **build**라는 새 폴더 안에 배치됩니다. 축하합니다. 이제 Tkinter Designer를 사용하여 Tkinter GUI를 만들었습니다!

<br><br>

<a id="Troubleshooting"></a>

# 문제해결 <small>[[Top](#목차)]</small>

- 요소가 보이지 않습니까?
    - Figma 파일의 요소 이름이 올바른지 확인하십시오 * See [Figma 가이드, &sect;1](#formatting-1)

- 버튼에 의도하지 않은 회색 배경이 있습니까?
    - 버튼 요소 뒤에 직사각형을 추가했는지 확인하고 채우기 색이 배경의 색과 동일한지 확인합니다.

- 잘못된 요소?
    - Figma에서 요소의 이름을 올바르게 지정했는지 확인합니다.
        - See [Figma 가이드, &sect;1](#formatting-1)

- 창이 화면보다 큽니까?
    - Figma에서 요소의 크기를 줄이세요.

- 파일이 생성되지 않습니까?
    - Tkinter Designer 다시 시작합니다.
    - 토큰과 URL을 더블체크합니다.
    - 디자인에 프레임이 있는지 확인합니다.

- 다른 문제가 있습니까?
    - [Report issues not listed here on GitHub](https://github.com/ParthJadhav/Tkinter-Designer/issues/new)
