# Cách sử dụng Tkinter Designer

#### Các bản dịch

- [简体中文](/docs/instructions.zh-CN.md)
- [Français](/docs/instructions.fr-FR.md)
- [ગુજરાતી](docs/instructions.gu-GU.md)
- [عربية](/docs/instructions.ar-DZ.md)
- [Turkish](/docs/instructions.tr-TR.md)
- [Korean](/docs/instructions.kr-KR.md)
- [Tiếng Việt](/docs/instructions.vi-VN.md)
___

## Mục lục

1. [**Bắt đầu**](#getting-started-1)
   1. [Cài đặt Python](#getting-started-1)
   2. [Cài đặt Tkinter Designer](#getting-started-2)
   3. [Tạo tài khoản Figma](#getting-started-3)

2. [**Cách định dạng thiết kế ở Figma**](#formatting-1)
   1. [Tài liệu tham khảo](#formatting-1)
   2. [Hướng dẫn về các phần tử](#formatting-2)

3. [**Sử dụng Tkinter Designer**](#Using-Tkinter-Designer)
   1. [Mã truy cập cá nhân](#using-1)
   2. [Lấy địa chỉ của file](#using-2)
   3. [Sử dụng CLI (Command Line Interface)](#using-cli)
   4. [Sử dụng GUI (Giao diện người dùng đồ họa)](#using-gui)

4. [**Khắc phục sự cố**](#Troubleshooting)

<br><br>

# Bắt đầu <small>[[Top](#table-of-contents)]</small>

<a id="getting-started-1"></a>

## 1. Install Python

Trước khi sử dụng Tkinter Designer, bạn sẽ cần cài đặt Python.  
- [Bấm vào đây để đến trang tải xuống Python](https://www.python.org/downloads)  
- [Đây là hướng dẫn cho các hệ điều hành](https://wiki.python.org/moin/BeginnersGuide/Download)

*Trong hướng dẫn này, bạn sẽ sử dụng Trình cài đặt Gói cho Python (pip), điều này có thể đòi hỏi bạn phải thêm Python vào PATH của hệ thống.

___
<br>

<a id="getting-started-2"></a>

   ## 2. Cài đặt Tkinter Designer

   *3 Phương Pháp:*

   1. Sử dụng câu lệnh `pip install tkdesigner`

   2. Cài đặt [poetry](https:python-poetry.org) và sử dụng các câu lệnh:
      - `poetry new <gui_project_name> && cd <gui_project_name>`
      - `poetry add tkdesigner`
      - `poetry install`

   3. Chạy Tkinter Designer từ mã nguồn mở:

      1. Tải xuống các tệp nguồn cho Tkinter Designer bằng cách tải xuống thủ công hoặc sử dụng GIT.

         ` git clone https://github.com/ParthJadhav/Tkinter-Designer.git `

      2. Thay đổi thư mục làm việc của bạn thành Tkinter Designer.

         `cd Tkinter-Designer`

      3. Cài đặt các gói cần thiết.

         - `pip install -r requirements.txt`
            - Nếu pip không hoạt động, hãy thử các câu lệnh sau:
            - `pip3 install -r requirements.txt`
            - `python -m pip install -r requirements.txt`
            - `python3 -m pip install -r requirements.txt`
            - Nếu vẫn không hoạt động, hãy đảm bảo Python đã được thêm vào PATH.

      Điều này sẽ cài đặt tất cả các yêu cầu và Tkinter Designer. Trước khi sử dụng Tkinter Designer, bạn cần tạo một tệp Figma với các hướng dẫn dưới đây.

      Nếu bạn đã tạo một file, hãy đi tới phần [**Sử dụng Tkinter Designer**](#Using-Tkinter-Designer).

   ___
   <br>

   <a id="getting-started-3"></a>

   ## 3. Tạo tài khoản Figma

   1. Truy cập [figma.com](https://www.figma.com/) và đăng kí
   2. Nhập thông tin của bạn, sau đó xác minh email của bạnl
   3. Tạo một file thiết kế Figma
   4. Bắt đầu tạo GUI (Giao diện người dùng đồ họa)
      - Phần tiếp theo sẽ đề cập đến định dạng cần thiết cho đầu vào Tkinter Designer.
      - [Đây là loạt bài hướng dẫn chính thức của Figma dành cho người mới bắt đầu.](https://www.youtube.com/watch?v=Cx2dkpBxst8&list=PLXDU_eVOJTx7QHLShNqIXL1Cgbxj7HlN4)
      - [Đây là kênh YouTube chính thức của Figma.](https://www.youtube.com/c/Figmadesign/featured)
      - [Đây là Trung tâm Trợ giúp của Figma.](https://help.figma.com/hc/en-us)

   <br><br>

<a id="formatting-1"></a>

# Định dạng thiết kế ở Figma <small>[[Top](#table-of-contents)]</small>

## 1. Tham khảo

<br>

### Cách đặt tên là một yếu tố vô cùng quan trọng

| Tên phần tử trong Figma | Khi phần tử ở Tkinter |
| --- | --- |
| Button | Button |
| Line | Line |
| Text | Name it anything |
| Rectangle | Rectangle |
| TextArea | Text Area |
| TextBox | Entry |
| Image | Canvas.Image() |

<br>

Mã được tạo ra bởi Tkinter Designer dựa trên tên các phần tử trong thiết kế Figma của bạn, và do đó, bạn cần đặt tên cho các phần tử của mình một cách phù hợp. Trong Figma, đổi tên các phần tử bằng cách nhấp đúp vào chúng trong bảng Layers.


___
<br>

<a id="formatting-2"></a>

## 2. Hướng dẫn về các phần tử

<br>

1. **Trước tiên, tạo một khung chứa và đó sẽ là cửa sổ Tkinter của bạn.**
<br><br>

2. **Thêm ảnh**
   - IHình ảnh có thể được tạo bằng các hình dạng (shapes) và/hoặc hình ảnh (images)
   - Nếu bạn sử dụng nhiều hình dạng/ảnh, bạn phải nhóm chúng lại bằng cách chọn tất cả và nhấn <kbd>CTRL/⌘ + G</kbd>
   - Sau đó, đặt tên cho phần tử hoặc nhóm là "Image".
<br><br>

3. **Văn bản (Văn bản bình thường)**
   - Sử dụng phím <kbd>T</kbd> để kích hoạt công cụ văn bản, sau đó thêm văn bản theo ý muốn
   - Văn bản không cần được đổi tên để sử dụng trong Tkinter Designer
   - Nhấn rõ nút <kbd>Return</kbd> hoặc <kbd>Enter</kbd> để chuyển xuống dòng tiếp theo.
<br><br>

4. **Entry (Người dùng nhập trong 1 dòng)**
   - Kích hoạt công cụ Hình lập phương (rectangle) với <kbd>R</kbd>
   - Điều chỉnh Hình lập phương (rectangle) theo ý thích của bạn
   - Đảm bảo rằng Hình lập phương (rectangle) có tên là "TextBox"
<br><br>

5. **Vùng văn bản (Người dùng nhập nhiều dòng)**
   - Kích hoạt công cụ Hình lập phương (rectangle) với <kbd>R</kbd>
   - Điều chỉnh Hình lập phương (rectangle) theo ý thích của bạn
   - Đảm bảo rằng Hình lập phương (rectangle) có tên là "TextArea"

6. **Hình lập phương**
   - Kích hoạt công cụ Hình lập phương (rectangle) với <kbd>R</kbd>
   - Điều chỉnh Hình lập phương (rectangle) theo ý thích của bạn
   - Đảm bảo rằng Hình lập phương (rectangle) có tên là "Rectangle"
<br><br>

7. **Nút thông thường**
   - Thêm một Hình lập phương để làm nút trong Giao diện người dùng đồ họa của bạn.
      - Tùy chọn: Thêm văn bản cho nút.
   - Chọn nút (Hình lập phương vừa tạo) và văn bản, sau đó nhóm chúng với phím <kbd>CTRL/&#8984; + G</kbd>
   - Đặt tên cho nhóm là "Button"

#### Tham khảo [video này](https://youtu.be/Qd-jJjduWeQ) nếu bạn gặp phải vấn đề

<br><br>

8. **Nút bo tròn**
   - Add rectangle to serve as a button in your GUI
   - Thêm một Hình lập phương để làm nút trong Giao diện người dùng đồ họa của bạn.
      - Tùy chọn: Thêm văn bản cho nút.
   -Làm cho nút có hình dạng bo tròn bằng cách thêm bán kính góc bằng cách chọn Hình lập phương và thêm bán kính góc từ phía bên phải.[Đọc thêm](https://help.figma.com/hc/en-us/articles/360050986854-Adjust-corner-radius-and-smoothing)
   - Tạo một Hình lập phương có cùng kích thước với nút của bạn. Không làm cho nó bo tròn.
   - Thay đổi màu sắc của Hình lập phương để phù hợp với nền.
   - Tiếp theo, di chuyển Hình lập phương vừa tạo xuống phía dưới nút chính (Hình lập phương).
   - Chọn nút, Hình lập phương và văn bản tùy chọn (nếu có), sau đó nhóm chúng với phím <kbd>CTRL/⌘ + G</kbd>.
   - Đặt tên cho nhóm là "Button".

#### Tham khảo [video này](https://youtu.be/Qd-jJjduWeQ) nếu bạn gặp phải vấn đề

<br><br>

<a id="Using-Tkinter-Designer"></a>

# Sử dụng Tkinter Designer <small>[[Top](#table-of-contents)]</small>

## Các thông tin cần nhập

Có một số thông tin mà bạn sẽ cần thu thập để sử dụng Tkinter Designer.

<a id="using-1"></a>

### 1. Mã truy cập cá nhân

1. Đăng nhập vào tài khoản Figma của bạn.
2. Di chuyển đến Cài đặt.
3. Trong tab Tài khoản, cuộn xuống đến Mã truy cập cá nhân.
4. Nhập tên của mã truy cập cá nhân vào ô nhập và nhấn <kbd>Enter</kbd>.

5. Mã truy cập cá nhân của bạn sẽ được tạo.
   - Sao chép mã truy cập này và lưu nó ở một nơi an toàn.
   - **Mã này sẽ chỉ xuất hiện một lần và không thể sao chép lại**

<a id="using-2"></a>

### 2. Lấy địa chỉ của file

1. Trong tệp thiết kế Figma của bạn, nhấp vào nút **Share** ở thanh trên cùng, sau đó nhấp vào  **&#x1f517; Copy link**

<a id="using-cli"></a>

## Sử dụng CLI

Sử dụng CLI rất đơn giản, chỉ cần cài đặt gói và chạy công cụ CLI.

### Từ PyPi

Bạn có thể sử dụng lệnh dưới đây để kiểm tra bằng cách thay thế $FILE_URL và $FIGMA_TOKEN bằng dữ liệu của bạn. Nếu bạn chưa có mã thông báo và liên kết, vui lòng tham khảo phần [**Các thông tin cần nhập**](#using-1).

``` bash
pip install tkdesigner

tkdesigner $FILE_URL $FIGMA_TOKEN
```

### Từ mã nguồn

Để sử dụng CLI từ mã nguồn, bạn cần sao chép kho mã và sau đó làm theo các hướng dẫn dưới đây.

Bạn có thể sử dụng lệnh dưới đây để kiểm tra bằng cách thay thế $FILE_URL và $FIGMA_TOKEN bằng dữ liệu của bạn. Nếu bạn chưa có mã thông báo và liên kết, vui lòng tham khảo phần [**Các thông tin cần nhập**](#using-1).

```bash
$ python -m tkdesigner.cli $FILE_URL $FIGMA_TOKEN

# To learn more about how to use the cli, pass the --help flag
$ python -m tkdesigner --help
```

### Kết quả

Mặc định, mã GUI sẽ được ghi vào tệp build/gui.py. Bạn có thể chỉ định đường dẫn đầu ra bằng cách sử dụng cờ `-o` và cung cấp đường dẫn.

Để chạy GUI đã tạo, hãy di chuyển đến thư mục bạn đã xây dựng (ví dụ: build/) và chạy nó như bất kỳ GUI Tkinter nào khác.

```bash
cd build
python3 gui.py
```

<a id="using-gui"></a>

## Sử dụng giao diện người dùng đồ họa (GUI)

### Mở Tkinter Designer trước khi làm các bước sau

<br>

1. Mở giao diện người dùng Tkinter Designer bằng cách:

```
cd Tkinter-Designer
cd gui
python3 gui.py
```

2. Dán *mã truy cập cá nhân* của bạn vào ô **Token ID** trong Tkinter Designer.
3. Dán liên kết vào ô **File URL** trong Tkinter Designer.
4. Nhấp vào ô **Output Path** để mở trình duyệt tệp.
5. Chọn một đường dẫn đầu ra và nhấp vào **Select Folder**.
6. Nhấn **Generate**.

Các tệp kết quả từ Tkinter Designer sẽ được đặt trong thư mục đã chọn của bạn, trong một thư mục mới có tên là **build**. Chúc mừng bạn đã tạo thành công giao diện Tkinter của bạn bằng Tkinter Designer!

<br><br>

<a id="Troubleshooting"></a>

# Gỡ lỗi <small>[[Trở lại đầu trang](#table-of-contents)]</small>

- Các phần tử không hiển thị? Bị đặt sai vị trí?
  - Vui lòng đảm bảo rằng tệp Figma của bạn đã đặt tên các phần tử của nó đúng cách. * Xem [Định dạng thiết kế Figma của bạn, &sect;1](#formatting-1)

- Nút có màu nền xám không đúng ý?
  - Hãy đảm bảo bạn đã thêm một hình chữ nhật phía sau phần tử nút của bạn và màu sắc Fill của nó giống với màu nền.

- Các phần tử không chính xác?
  - Hãy đảm bảo bạn đã đặt tên các phần tử của mình đúng cách trong Figma.
    - Xem [Định dạng thiết kế Figma của bạn, &sect;1](#formatting-1)

- Cửa sổ lớn hơn màn hình?
  - Giảm kích thước các phần tử trong Figma.

- Không tạo ra các tệp?
  - Khởi động lại Tkinter Designer.
  - Kiểm tra lại mã thông báo và liên kết.
  - Đảm bảo thiết kế của bạn có một khung (Frame).

- Có vấn đề khác?
  - [Báo cáo vấn đề không được liệt kê tại đây trên GitHub](https://github.com/ParthJadhav/Tkinter-Designer/issues/new)