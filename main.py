import requests
from colormap import rgb2hex
import os

os.mkdir("./generated_code/")

lines = []
lines.extend(['from tkinter import *', 'window = Tk()', 'def btnClicked():\n', '    print("Button Clicked")\n'])


def get_color(element):
    """ Get's the element as input and checks for it's RGB color and converts and returns it's HEX COLOR. (STRING)"""
    el_r = element["fills"][0]["color"]['r'] * 255
    el_g = element["fills"][0]["color"]['g'] * 255
    el_b = element["fills"][0]["color"]['b'] * 255
    hex_code = rgb2hex(round(el_r), round(el_g), round(el_b))
    return hex_code


def get_coordinates(element):
    """ Get's the element as input and returns it's coordinates in X, Y. (INT)"""
    x = int(element["absoluteBoundingBox"]["x"])
    y = int(element["absoluteBoundingBox"]["y"])
    return x, y


def get_dimensions(element):
    """ Get's the element as input and returns it's dimensions in width, height. (INT)"""
    height = int(element["absoluteBoundingBox"]["height"])
    width = int(element["absoluteBoundingBox"]["width"])
    return width, height


def get_text_properties(element):
    """ Get's the element as input and returns it's font and fontSize in String."""
    font = element["style"]["fontPostScriptName"]
    fontSize = element["style"]["fontSize"]
    return font, fontSize


###################### Getting File Data #######################
# token = "189541-e5791cc9-4619-411e-b4b1-6b6f7d285d68"

token = input("Enter the token :\n")
file_url = input("Enter the URL to the file :\n")


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


fileId = find_between(file_url, "file/", "/")

response = requests.get(f"https://api.figma.com/v1/files/{fileId}", headers={"X-FIGMA-TOKEN": token})

data = response.json()
print(data)

####################### Getting Window Properties #######################

fig_window = data["document"]["children"][0]['children'][0]

window_width, window_height = get_dimensions(fig_window)

try:
    window_bg_hex = get_color(fig_window)
except:
    window_bg_hex = "#FFFFFF"

####################### Creating Window #######################

lines.extend([f'\nwindow.geometry("{window_width}x{window_height}")', f'window.configure(bg="{window_bg_hex}")',
              f'canvas = Canvas(window,bg="{window_bg_hex}",height={window_height},width={window_width},bd=0, highlightthickness=0,relief="ridge")',
              'canvas.place(x=0,y=0)\n'])

####################### Getting Elements inside Window #######################
window_elements = fig_window["children"]

btn_count = 0
text_entry_count = 0

for element in window_elements:

    if element["name"] == 'Rectangle':
        width, height = get_dimensions(element)
        x, y = get_coordinates(element)
        element_color = get_color(element)
        # canvas.create_rectangle(x, y, x + width, y + height, fill=element_color)
        lines.extend([
            f'\ncanvas.create_rectangle({x}, {y}, {x} + {width}, {y} + {height}, fill="{element_color}",outline="")\n'])

    elif element["name"] == 'Button':
        width, height = get_dimensions(element)
        x, y = get_coordinates(element)
        item_id = element["id"]

        response = requests.get(f"https://api.figma.com/v1/images/{fileId}?ids={item_id}",
                                headers={"X-FIGMA-TOKEN": "189543-60e9c4f6-7b8c-4fc1-b682-586c2fb8a0e7"})
        res = requests.get(response.json()["images"][item_id])
        with open(f"./generated_code/img{btn_count}.png", "wb") as file:
            file.write(res.content)

        lines.extend([f'img{btn_count} = PhotoImage(file=f"img{btn_count}.png")',
                      f'b{btn_count} = Button(image=img{btn_count}, borderwidth=0, highlightthickness=0, command=btnClicked, relief="flat")',
                      f'b{btn_count}.place(x={x}, y={y}, width={width}, height={height})\n'])
        btn_count += 1

    elif element["type"] == 'TEXT':
        text = element["characters"]
        x, y = get_coordinates(element)
        width, height = get_dimensions(element)
        color = get_color(element)
        font, fontSize = get_text_properties(element)
        x, y = x + (width / 2), y + (height / 2)
        # canvas.create_text(x,y,text=text,fill=color,font=(font,int(fontSize)))
        lines.extend([f'canvas.create_text({x},{y},text="{text}",fill="{color}",font=("{font}",int({fontSize})))\n'])

    elif element["name"] == 'TextBox':
        width, height = get_dimensions(element)
        x, y = get_coordinates(element)
        bg = get_color(element)
        # entry = Entry(bd=0,bg=bg,highlightthickness=0)
        # entry.place(x=x,y=y,width=width,height=height)
        lines.extend([f'entry{text_entry_count} = Entry(bd=0,bg="{bg}",highlightthickness=0)',
                      f'entry{text_entry_count}.place(x={x},y={y},width={width},height={height})\n'])

    elif element["name"] == "Background":
        width, height = get_dimensions(element)
        x, y = get_coordinates(element)
        x, y = x + (width / 2), y + (height / 2)
        item_id = element["id"]

        response = requests.get(f"https://api.figma.com/v1/images/{fileId}?ids={item_id}&use_absolute_bounds=true",
                                headers={"X-FIGMA-TOKEN": "189543-60e9c4f6-7b8c-4fc1-b682-586c2fb8a0e7"})
        res = requests.get(response.json()["images"][item_id])
        with open(f"./generated_code/background.png", "wb") as file:
            file.write(res.content)

        # img = PhotoImage(file=f"background.png")
        # background = canvas.create_image(x,y,image=img)
        lines.extend(['background_img = PhotoImage(file=f"background.png")',
                      f'background = canvas.create_image({x},{y},image=background_img)\n'])

####################### Adding the generated code to window.py #######################
lines.extend(['window.mainloop()'])
final_code = [line + "\n" for line in lines]

with open("./generated_code/window.py", 'w') as py_file:
    py_file.writelines(final_code)
