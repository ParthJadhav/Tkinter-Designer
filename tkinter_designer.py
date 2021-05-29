from tkinter import *
from tkinter import filedialog,messagebox
import backend
import webbrowser

window = Tk()
window.title("Tkinter Designer")
path_to_save = ""

def btnClicked():
    token = token_entry.get()
    URL = URL_entry.get()
    if token == "":
        messagebox.showerror(title="Empty Fields", message="Please enter Token")
    elif URL == "":
        messagebox.showerror(title="Empty Fields", message="Please enter URL")
    elif path_to_save == "":
        messagebox.showerror(title="invalid path", message="Enter a correct path")
    else:
        backend.generate_code(token,URL, path_to_save)

def select_path(event):
    global path_to_save
    # window.withdraw()
    path_to_save = filedialog.askdirectory()
    path_entry.insert(0, path_to_save)
    # window.deiconify()

def know_more_clicked(event):
    url = "https://github.com/ParthJadhav/Tkinter-Designer/blob/master/instructions.md"
    webbrowser.open_new(url)

def make_label(master, x, y, h, w, *args, **kwargs):
    f = Frame(master, height=h, width=w)
    f.pack_propagate(0) # don't shrink
    f.place(x=x, y=y)
    label = Label(f, *args, **kwargs)
    label.pack(fill=BOTH, expand=1)
    return label

window.geometry("862x519")
window.configure(bg="#3A7FF6")
canvas = Canvas(window,bg="#3A7FF6",height=519,width=862,bd=0, highlightthickness=0,relief="ridge")
canvas.place(x=0,y=0)
canvas.create_rectangle(431, 0, 431 + 431, 0 + 519, fill="#FCFCFC",outline="")
canvas.create_rectangle(40, 160, 40 + 60, 160 + 5, fill="#FCFCFC",outline="")

text_box_bg = PhotoImage(file=f"images/TextBox_Bg.png")
token_entry_img = canvas.create_image(650.5,167.5,image=text_box_bg)
URL_entry_img = canvas.create_image(650.5,248.5,image=text_box_bg)
filePath_entry_img = canvas.create_image(650.5,329.5,image=text_box_bg)

token_entry = Entry(bd=0,bg="#F6F7F9",highlightthickness=0)
token_entry.place(x=490.0,y=137+25,width=321.0,height=35)

URL_entry = Entry(bd=0,bg="#F6F7F9",highlightthickness=0)
URL_entry.place(x=490.0,y=218+25,width=321.0,height=35)

path_entry = Entry(bd=0,bg="#F6F7F9",highlightthickness=0)
path_entry.place(x=490.0,y=299+25,width=321.0,height=35)
path_entry.bind("<1>", select_path)


canvas.create_text(519.0,156.0,text="Token ID",fill="#515486",font=("Arial-BoldMT",int(13.0)))
canvas.create_text(518.5,234.5,text="File URL",fill="#515486",font=("Arial-BoldMT",int(13.0)))
canvas.create_text(529.5,315.5,text="Output Path",fill="#515486",font=("Arial-BoldMT",int(13.0)))
canvas.create_text(646.5,428.5,text="Generate",fill="#FFFFFF",font=("Arial-BoldMT",int(13.0)))
canvas.create_text(573.5,88.0,text="Enter the details.",fill="#515486",font=("Arial-BoldMT",int(22.0)))

title = Label(text="Welcome to Tkinter Designer", bg="#3A7FF6",fg="white",font=("Arial-BoldMT",int(20.0)))
title.place(x=27.0,y=120.0)

info_text = Label(text="Tkinter Designer uses the Figma API\n"
                   "to analyse a design file, then creates\n"
                   "the respective code and files needed\n"
                   "for your GUI.\n\n"
                   
                   "Even this GUI was created\n"
                   "using Tkinter Designer.",
              bg="#3A7FF6",fg="white",justify="left",font=("Georgia",int(16.0)))

info_text.place(x=27.0,y=200.0)

know_more = Label(text="How to use ?", bg="#3A7FF6",fg="white", cursor="hand2")
know_more.place(x=27,y=400)
know_more.bind('<Button-1>', know_more_clicked)

generate_btn_img = PhotoImage(file="./images/generate.png")
generate_btn = Button(image=generate_btn_img, borderwidth=0, highlightthickness=0, command=btnClicked, relief="flat")
generate_btn.place(x=557, y=401, width=180, height=55)


window.resizable(False, False)
window.mainloop()
