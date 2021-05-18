import requests
import pandas as pd
from colormap import rgb2hex
import PySimpleGUI as sg
from window import Figma_window

# window = Tk()


token = "189541-e5791cc9-4619-411e-b4b1-6b6f7d285d68"
fileId = "8K2eByUz9tLasBT5sOFSzJ"
response = requests.get("https://api.figma.com/v1/files/8K2eByUz9tLasBT5sOFSzJ", headers={"X-FIGMA-TOKEN": "189543-60e9c4f6-7b8c-4fc1-b682-586c2fb8a0e7"})
print(response.text)

with open("js.json",'w') as js:
    js.write(response.text)

data = pd.read_json("js.json")

fig_window = data["document"]["children"][0]['children'][0]
window_cordinates = fig_window["absoluteBoundingBox"]

window_width = window_cordinates["width"]
window_height = window_cordinates["height"]

window_color = fig_window["fills"][0]["color"]
window_color_r = window_color['r'] * 255
window_color_g = window_color['g'] * 255
window_color_b = window_color['b'] * 255

window_elements = fig_window["children"]

layout = [[sg.Button("And this is Created using PySimpleGUI Automatically")]]

hex = rgb2hex(round(window_color_r),round(window_color_g),round(window_color_b))

created_window = Figma_window.createWindow(Figma_window(),layout,window_width,window_height,hex)
