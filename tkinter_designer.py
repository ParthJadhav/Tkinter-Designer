from tkinter import *
from tkinter import filedialog,messagebox
import backend

window = Tk()
window.title("Tkinter Designer")
path_to_save = ""

def btnClicked():
    token = token_entry.get()
    URL = URL_entry.get()
    print(f"'{type(URL)}','{type(token)}'")
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
    window.withdraw()
    path_to_save = filedialog.askdirectory()
    path_entry.insert(0, path_to_save)
    window.deiconify()

window.geometry("749x737")
window.configure(bg="#FFFFFF")
canvas = Canvas(window,bg="#FFFFFF",height=737,width=749,bd=0, highlightthickness=0,relief="ridge")
canvas.place(x=0,y=0)

background_img = PhotoImage(file="./images/background.png")
background = canvas.create_image(374.5,368.5,image=background_img)

folder_btn_img = PhotoImage(file="./images/folder.png")
folder_btn = Button(image=folder_btn_img, borderwidth=0, highlightthickness=0, command=select_path, relief="flat")
folder_btn["state"] = "disabled"
folder_btn.place(x=512, y=481, width=18, height=18)

token_entry = Entry(bd=0, bg="#F6F7F9", highlightthickness=0)
token_entry.place(x=219, y=328, width=284, height=27)

URL_entry = Entry(bd=0, bg="#F6F7F9", highlightthickness=0)
URL_entry.place(x=219, y=409, width=284, height=27)

path_entry = Entry(bd=0, bg="#F6F7F9", highlightthickness=0)
path_entry.place(x=219, y=490, width=284, height=27)
path_entry.bind("<1>", select_path)

canvas.create_text(378.0,165.0,text="Tkinter Designer",fill="#373C8A",font=("Arial-BoldMT",int(64.0)))
canvas.create_text(367.0,229.0,text="Enter the following details",fill="#515486",font=("ArialMT",int(24.0)))
canvas.create_text(243.0,316.5,text="Token ID",fill="#515486",font=("Arial-BoldMT",int(13.0)))
canvas.create_text(242.5,397.5,text="File URL",fill="#515486",font=("Arial-BoldMT",int(13.0)))
canvas.create_text(253.5,478.5,text="Output Path",fill="#515486",font=("Arial-BoldMT",int(13.0)))

generate_btn_img = PhotoImage(file="./images/generate.png")
generate_btn = Button(image=generate_btn_img, borderwidth=0, highlightthickness=0, command=btnClicked, relief="flat")
generate_btn.place(x=294, y=575, width=180, height=56)

window.resizable(False, False)
window.mainloop()
