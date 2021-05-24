import requests
from colormap import rgb2hex
import os
from tkinter import messagebox

def generate_code(token,link,path_to_save):
    generated_dir = path_to_save + "/generated_code/"
    try:
        os.mkdir(generated_dir)
    except:
        pass

    lines = []
    lines.extend(['from tkinter import *', 'window = Tk()', 'def btn_clicked():', '    print("Button Clicked")\n'])

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

    token = token
    file_url = link

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

            lines.extend([
                f'\ncanvas.create_rectangle({x}, {y}, {x} + {width}, {y} + {height}, fill="{element_color}",outline="")\n'])

        elif element["name"] == 'Button':
            width, height = get_dimensions(element)
            x, y = get_coordinates(element)
            item_id = element["id"]

            response = requests.get(f"https://api.figma.com/v1/images/{fileId}?ids={item_id}",
                                    headers={"X-FIGMA-TOKEN": f"{token}"})
            image_link = requests.get(response.json()["images"][item_id])
            with open(f"{generated_dir}img{btn_count}.png", "wb") as file:
                file.write(image_link.content)

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

            lines.extend([f'canvas.create_text({x},{y},text="{text}",fill="{color}",font=("{font}",int({fontSize})))\n'])

        elif element["name"] == 'TextBox':
            width, height = get_dimensions(element)
            x, y = get_coordinates(element)
            x, y = x + (width / 2), y + (height / 2)
            bg = get_color(element)

            item_id = element["id"]
            response = requests.get(f"https://api.figma.com/v1/images/{fileId}?ids={item_id}",
                                    headers={"X-FIGMA-TOKEN": f"{token}"})

            image_link = requests.get(response.json()["images"][item_id])

            with open(f"{generated_dir}img_textBox{text_entry_count}.png", "wb") as file:
                file.write(image_link.content)

            lines.extend([f'entry{text_entry_count}_img = PhotoImage(file=f"img_textBox{text_entry_count}.png")',
                          f'entry{text_entry_count}_bg = canvas.create_image({x},{y},image=entry{text_entry_count}_img)\n'])

            corner_radius = element["cornerRadius"]
            if corner_radius > height / 2:
                corner_radius = height / 2

            reduced_width = width - (corner_radius * 2)
            reduced_height = height - 2
            x, y = get_coordinates(element)
            x = x + corner_radius

            lines.extend([f'entry{text_entry_count} = Entry(bd=0,bg="{bg}",highlightthickness=0)',
                          f'entry{text_entry_count}.place(x={x},y={y},width={reduced_width},height={reduced_height})\n'])

            text_entry_count += 1

        elif element["name"] == "Background":
            width, height = get_dimensions(element)
            x, y = get_coordinates(element)
            x, y = x + (width / 2), y + (height / 2)
            item_id = element["id"]

            response = requests.get(f"https://api.figma.com/v1/images/{fileId}?ids={item_id}&use_absolute_bounds=true",
                                    headers={"X-FIGMA-TOKEN": f"{token}"})
            image_link = requests.get(response.json()["images"][item_id])
            with open(f"{generated_dir}background.png", "wb") as file:
                file.write(image_link.content)

            lines.extend(['background_img = PhotoImage(file=f"background.png")',
                          f'background = canvas.create_image({x},{y},image=background_img)\n'])

    ####################### Adding the generated code to window.py #######################

    lines.extend(['window.resizable(False, False)','window.mainloop()'])
    final_code = [line + "\n" for line in lines]

    with open(f"{generated_dir}window.py", 'w') as py_file:
        py_file.writelines(final_code)

    messagebox.askokcancel("Success","The file were successfully Created")
