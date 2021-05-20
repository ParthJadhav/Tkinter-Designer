from tkinter import *
window = Tk()

def btnClicked():
    print("hey")

window.geometry("944x639")
window.configure(bg="#4FA1DC")
canvas = Canvas(window,bg="#4FA1DC",height=639,width=944,bd=0, highlightthickness=0,relief="ridge")
canvas.pack()

img0 = PhotoImage(file=f"img0.png")
b0 = Button(image=img0, borderwidth=0, highlightthickness=0, command=btnClicked, relief="flat")
b0.place(x=248, y=480, width=184, height=64)


img1 = PhotoImage(file=f"img1.png")
b1 = Button(image=img1, borderwidth=0, highlightthickness=0, command=btnClicked, relief="flat")
b1.place(x=487, y=480, width=184, height=64)

canvas.create_text(471.0,134.5,text="Hello",fill="#FFFFFF",font=("UniSansHeavyItalic",int(96.0)))
canvas.create_text(458.5,237.0,text="This Is Good",fill="#FFFFFF",font=("UniSansThinCAPS",int(48.0)))

window.mainloop()