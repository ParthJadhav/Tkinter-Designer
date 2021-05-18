from PySimpleGUI import Window
from colormap import rgb2hex


class Figma_window():

    def createWindow(self, layout, window_width, window_height, hex_code):
        window = Window("Figma Window", layout, size=(int(window_width), int(window_height)), background_color=hex_code)
        event, values = window.read()
