from tkinter import *
from tkinter import filedialog
import backend

window = Tk()
window.title("Tkinter Designer")
path_to_save = ""

def btnClicked():
    backend.generate_code(entry0.get(), entry1.get(), path_to_save)

def select_path(event):
    global path_to_save
    window.withdraw()
    path_to_save = filedialog.askdirectory()
    entry2.insert(0, path_to_save)
    window.deiconify()

window.geometry("749x737")
window.configure(bg="#FFFFFF")
canvas = Canvas(window,bg="#FFFFFF",height=737,width=749,bd=0, highlightthickness=0,relief="ridge")
canvas.place(x=0,y=0)

background_img = PhotoImage(file=f"background.png")
background = canvas.create_image(374.5,368.5,image=background_img)

img0 = PhotoImage(file=f"img0.png")
b0 = Button(image=img0, borderwidth=0, highlightthickness=0, command=select_path, relief="flat")
b0.place(x=512, y=481, width=18, height=18)

entry0 = Entry(bd=0,bg="#F6F7F9",highlightthickness=0)
entry0.place(x=219,y=328,width=284,height=27)

entry1 = Entry(bd=0,bg="#F6F7F9",highlightthickness=0)
entry1.place(x=219,y=409,width=284,height=27)

entry2 = Entry(bd=0,bg="#F6F7F9",highlightthickness=0)
entry2.place(x=219,y=490,width=284,height=27)
entry2.bind("<1>", select_path)

canvas.create_text(378.0,165.0,text="Tkinter Designer",fill="#373C8A",font=("Arial-BoldMT",int(64.0)))

canvas.create_text(367.0,229.0,text="Enter the following details",fill="#515486",font=("ArialMT",int(24.0)))

canvas.create_text(243.0,316.5,text="Token ID",fill="#515486",font=("Arial-BoldMT",int(13.0)))

canvas.create_text(242.5,397.5,text="File URL",fill="#515486",font=("Arial-BoldMT",int(13.0)))

canvas.create_text(253.5,478.5,text="Output Path",fill="#515486",font=("Arial-BoldMT",int(13.0)))

img1 = PhotoImage(file=f"img1.png")
b1 = Button(image=img1, borderwidth=0, highlightthickness=0, command=btnClicked, relief="flat")
b1.place(x=294, y=575, width=180, height=56)

window.resizable(False, False)
window.mainloop()
