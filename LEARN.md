# Creation Of Tkinter-Designer

## Introduction

 Hello everyone, I'm Parth Jadhav. I am a 17 year old student. And I would like to share how I created this repository.

## How does it work?

 Tkinter Designer uses Figma to generate the GUI. Users design the desired user interface in Figma. Then paste the URL into Tkinter Designer. TkinterDesigner uses the Figma API to get information about the file. Use that data to generate Tkinter-based GUI code in Python, using templates and more.

## How it all started

So, about a year ago, I took this [online course](https://www.udemy.com/course/100-days-of-code) for Python on Udemy. I was new to Python. I was having fun with Python until it came to creating GUIs.

I didn't find it interesting or easy enough to create GUIs in Python. They were mostly dull and boring. And it took a lot of effort to make it look good. So I decided to make something which will make GUIs beautiful and easy.

## Discovery & Search

If you have a problem, first search to see if anyone has solved it. Often times the problem you are trying to solve is already solved by someone. In that case you could either use that solution or build up on that solution or create a solution of your own. I chose to create my own solution to the problem.

I went on to search for any libraries or softwares which can solve this problem. And I found a repository -> [PySimpleGUI](https://github.com/PySimpleGUI/PySimpleGUI). I tried it and it was amazing. But I wanted to Automate stuff and do something fun. I didn't have an concrete idea on what and how to build. But wanted to create something which would make creating GUIs easier in Python.

One day I was just surfing on Youtube and found this guy working with [Figma API](https://www.figma.com/developers/api). Figma is a web based graphic design software. And it's API was able to provide the data about the design file the user is working on.

That gave me the idea to use Figma as the external tool for this project.

## First steps

Starting a project can sometimes be overwhelming. Sometimes we don't know where to start. Sometimes we are afraid of failures.Sometimes we don't know what to do next. It happens with everyone of us. The key is to just take that first step and start. It's not always easy to start. But it's always worth it.

I went on to create `main.py` file. First thing I did was to write code to get Data from [FigmaAPI](https://www.figma.com/developers/api) and Print it. I now had a code which would get the data from Figma about a file that User designed.

## Creating elements

So the next step was to create something simple from that data. It's always a good idea to start with something simple. Break your goal into small steps. My goal was to create a functional & beautiful GUI with Tkinter-Designer. So I broke it down to small steps like :-

- Add Frame Feature
- Add Label Feature
- Add Button Feature
- Add Entry Feature

I started by writing code to add Frame Feature. Figma has an element called Frame. It's a container which can contain other elements. You can create a Frame by pressing `F` and drawing a rectangle on the canvas.

_Psuedocode ahead_

```python
response = requests.get(
    "https://www.figma.com/developers/api#files-endpoints + {FileID}"
    )
```

The above code would store the response from Figma API in `response` variable. It would have all the data about the file.

```
{
  "document": {
    "id": "0:0",
    "name": "Document",
    "type": "DOCUMENT",
    "children": [
      {
        "id": "0:1",
        "name": "Page 1",
        "type": "CANVAS",
        "children": [
          {
            "id": "0:2",
            "name": "Frame 1",
            "type": "FRAME",
            "blendMode": "PASS_THROUGH",
            "children": [],
            "absoluteBoundingBox": {
              "x": 2,
              "y": -881,
              "width": 219,
              "height": 219
              },
            },
            ],
          ]
        }
}
```

Here's a simplified version of data returned from the API. It would have everything including the Color, type, position, text etc. Using that data I used template literals to create a Tkinter canvas with the dimensions of the Frame.

I did the same with every element Tkinter-Designer currently support. It was an easy process once I started. I just needed to repeat the process for each element.

Process :-

1. Write Python code to create the desired element in Tkinter.

Example :-

This is a code to create a Tkinter canvas, I've added some values to it..

```python
canvas = Canvas(
    window,
    bg = "Blue",
    height = 200,
    width = 400,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
```

2. Replace the values of that element with the values from Figma.

Example :-

Here we take that same code and replace the values of the element with the values from Figma.

`bg` -> figma.window.bg_color (Background color of a frame)

`height` -> figma.window.height (Height of a frame)

`width` -> figma.window.width (Width of a frame)

```python
canvas = Canvas(
    window,
    bg = "{{ figma.window.bg_color }}",
    height = {{ figma.window.height }},
    width = {{ figma.window.width }},
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
```

3. Write the output code to a Python file.

And once we convert all the elements to Tkinter, we can write the code to a Python file.

```python
def write_text(self, data, encoding=None, errors=None, newline=None):
        encoding = io.text_encoding(encoding)
        with self.open(mode='w', encoding=encoding, errors=errors, newline=newline) as f:
            return f.write(data)

def design(self):
        code = self.to_code() #Code is the converted Tkinter code. 
        self.output_path.joinpath(CODE_FILE_NAME).write_text(code)
```

### Element Identification

In order to create different elements like buttons, rectangles etc. I used the `name` property of the element. Figma didn't provide a way to identify the element. So I used the name of the element to identify it.

You can create a rectangle in Figma and name it 'Button' and it would be identified as a button. And Tkinter-Designer would create a button with the same properties.

## Finishing up

Once I had the basic elements working I uploaded the code to Github. It started to gain attention and popularity. More and more people were using it and it was fun to see it happen. I learned a lot on the way. The most fascinating part was the community. I was able to connect with people who were using it. I learned a lot from them.

[piccoloser](https://github.com/piccoloser) was one of the first contributor to this project. He refined and improved the documentation.

[Jason Chin](https://github.com/jrobchin) helped me in refactoring the code. The original code was a single big python file which was hard to read and build up on. Jason created a pull request which was really amazing. You can have a look at it here -> [PR 67](https://github.com/ParthJadhav/Tkinter-Designer/pull/67)

[Jakob Vendegna](https://github.com/jvendegna) helped a lot in CI/CD stuff. He also helped me publish code on PyPi.

That's the beauty of open source. We meet people who are more smarter than us; We learn from them. We meet people who we can teach something to. We exchange knowledge and ideas. And at the end of the day it's all about learning and making a difference.
