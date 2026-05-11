import webbrowser
import sys
import os
import tkinter as tk
import tkinter.messagebox as tk1
import tkinter.filedialog
from pathlib import Path

from PIL import Image, ImageTk

# Add tkdesigner to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
try:
    from tkdesigner.designer import Designer
    from tkdesigner.utils import parse_figma_url
except ModuleNotFoundError:
    raise RuntimeError("Couldn't add tkdesigner to the PATH.")


# Path to asset files for this GUI window.
ASSETS_PATH = Path(__file__).resolve().parent / "assets"

# Required in order to add data files to Windows executable
path = getattr(sys, '_MEIPASS', os.getcwd())
os.chdir(path)

output_path = ""
image_refs = []


def load_photo_image(path):
    try:
        image = tk.PhotoImage(file=path)
    except tk.TclError:
        image = ImageTk.PhotoImage(Image.open(path))
    image_refs.append(image)
    return image


def btn_clicked():
    token = token_entry.get()
    URL = URL_entry.get()
    output_path = path_entry.get()
    output_path = output_path.strip()

    if not token:
        tk.messagebox.showerror(
            title="Empty Fields!", message="Please enter Token.")
        return
    if not URL:
        tk.messagebox.showerror(
            title="Empty Fields!", message="Please enter URL.")
        return
    if not output_path:
        tk.messagebox.showerror(
            title="Invalid Path!", message="Enter a valid output path.")
        return

    try:
        figma_reference = parse_figma_url(URL)
    except ValueError:
        tk.messagebox.showerror(
            "Invalid URL!", "Please enter a valid file URL.")
        return

    token = token.strip()
    output = Path(f"{output_path}/build").expanduser().resolve()
    clean_output = False

    if output.exists() and not output.is_dir():
        tk1.showerror(
            "Exists!",
            f"{output} already exists and is not a directory.\n"
            "Enter a valid output directory.")
    elif output.exists() and output.is_dir() and tuple(output.glob('*')):
        response = tk1.askyesno(
            "Continue?",
            f"Directory {output} is not empty.\n"
            "Do you want to continue and overwrite?")
        if not response:
            return
        clean_output = True

    try:
        designer = Designer(
            token,
            figma_reference.file_key,
            output,
            node_id=figma_reference.node_id,
        )
        designer.design(clean=clean_output)
    except Exception as exc:
        tk.messagebox.showerror("Generation failed", str(exc))
        return

    tk.messagebox.showinfo(
        "Success!", f"Project successfully generated at {output}.")


def select_path():
    global output_path

    output_path = tk.filedialog.askdirectory()
    path_entry.delete(0, tk.END)
    path_entry.insert(0, output_path)


def know_more_clicked(event):
    instructions = (
        "https://github.com/ParthJadhav/Tkinter-Designer/"
        "blob/master/docs/instructions.md")
    webbrowser.open_new_tab(instructions)


def make_label(master, x, y, h, w, *args, **kwargs):
    f = tk.Frame(master, height=h, width=w)
    f.pack_propagate(0)  # don't shrink
    f.place(x=x, y=y)

    label = tk.Label(f, *args, **kwargs)
    label.pack(fill=tk.BOTH, expand=1)

    return label


window = tk.Tk()
logo = load_photo_image(ASSETS_PATH / "iconbitmap.gif")
window.call('wm', 'iconphoto', window._w, logo)
window.title("Tkinter Designer")

window.geometry("862x519")
window.configure(bg="#3A7FF6")
canvas = tk.Canvas(
    window, bg="#3A7FF6", height=519, width=862,
    bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)
canvas.create_rectangle(431, 0, 431 + 431, 0 + 519, fill="#FCFCFC", outline="")

text_box_bg = load_photo_image(ASSETS_PATH / "TextBox_Bg.png")
token_entry_img = canvas.create_image(650.5, 167.5, image=text_box_bg)
URL_entry_img = canvas.create_image(650.5, 248.5, image=text_box_bg)
filePath_entry_img = canvas.create_image(650.5, 329.5, image=text_box_bg)

token_entry = tk.Entry(
    bd=0, bg="#F6F7F9", fg="#000716", insertbackground="#000716",
    highlightthickness=0)
token_entry.place(x=490.0, y=137+25, width=321.0, height=35)
token_entry.focus()

URL_entry = tk.Entry(
    bd=0, bg="#F6F7F9", fg="#000716", insertbackground="#000716",
    highlightthickness=0)
URL_entry.place(x=490.0, y=218+25, width=321.0, height=35)

path_entry = tk.Entry(
    bd=0, bg="#F6F7F9", fg="#000716", insertbackground="#000716",
    highlightthickness=0)
path_entry.place(x=490.0, y=299+25, width=321.0, height=35)

path_picker_img = load_photo_image(ASSETS_PATH / "path_picker.png")
path_picker_button = tk.Button(
    image = path_picker_img,
    text = '',
    compound = 'center',
    fg = 'white',
    borderwidth = 0,
    highlightthickness = 0,
    command = select_path,
    relief = 'flat')

path_picker_button.place(
    x = 783, y = 319,
    width = 24,
    height = 22)

canvas.create_text(
    490.0, 156.0, text="Token ID", fill="#515486",
    font=("Arial-BoldMT", int(13.0)), anchor="w")
canvas.create_text(
    490.0, 234.5, text="File URL", fill="#515486",
    font=("Arial-BoldMT", int(13.0)), anchor="w")
canvas.create_text(
    490.0, 315.5, text="Output Path",
    fill="#515486", font=("Arial-BoldMT", int(13.0)), anchor="w")
canvas.create_text(
    646.5, 428.5, text="Generate",
    fill="#FFFFFF", font=("Arial-BoldMT", int(13.0)))
canvas.create_text(
    573.5, 88.0, text="Enter the details.",
    fill="#515486", font=("Arial-BoldMT", int(22.0)))

title = tk.Label(
    text="Welcome to Tkinter Designer", bg="#3A7FF6",
    fg="white", justify="left", font=("Arial-BoldMT", int(20.0)))
title.place(x=20.0, y=120.0)
canvas.create_rectangle(25, 160, 33 + 60, 160 + 5, fill="#FCFCFC", outline="")

info_text = tk.Label(
    text="Tkinter Designer uses the Figma API\n"
    "to analyse a design file, then creates\n"
    "the respective code and files needed\n"
    "for your GUI.\n\n"

    "Even this GUI was created\n"
    "using Tkinter Designer.",
    bg="#3A7FF6", fg="white", justify="left",
    font=("Georgia", int(16.0)))

info_text.place(x=20.0, y=200.0)

know_more = tk.Label(
    text="Click here for instructions",
    bg="#3A7FF6", fg="white", justify="left", cursor="hand2")
know_more.place(x=20, y=400)
know_more.bind('<Button-1>', know_more_clicked)

generate_btn_img = load_photo_image(ASSETS_PATH / "generate.png")
generate_btn = tk.Button(
    image=generate_btn_img, borderwidth=0, highlightthickness=0,
    command=btn_clicked, relief="flat")
generate_btn.place(x=557, y=401, width=180, height=55)

window.resizable(False, False)
window.mainloop()
