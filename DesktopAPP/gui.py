# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer



from pathlib import Path
import requests
#then you can use the font as you would normally
# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import *
from tkinter import BOTH, W, NW, SUNKEN, TOP, X, FLAT, LEFT
from PIL import Image, ImageTk
from tkinter import filedialog as fd
from io import BytesIO
from PIL import ImageTk, Image


URL = 'http://localhost:8000/api/'

window = Tk()

window.geometry("1200x700")
window.configure(bg="#6E8EE0", highlightthickness=0, relief="ridge")


canvas = Canvas(
    window,
    bg = "#FFF",
    height = 700,
    width = 1200,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)

  
# Add image file
bg = PhotoImage(file = "a.png")

canvas.create_image(
    600,
    0,
    image=bg,
    anchor='ne'
) 
ans = []

def my_command(event):
    filename = fd.askopenfilename()
    respose = requests.post(
        URL,
        files={
            'imagee': open(filename, 'rb')
        }
    )
    canvas.create_rectangle(
        600, 0,
        1200,555,
        fill='#fff',
        outline='#fff'
    )
    if respose.status_code == 200:
        data = respose.json()
        # print(data)
        canvas.create_text(
           (860.0, 540.0),
            anchor="nw",
            text=data["l"],
            fill="#000000",
            font='TkHeadingFont',
        ) 
        canvas.create_text(
           (860.0, 500.0),
            anchor="nw",
            text=data["text"],
            fill="#000000",
            font='TkHeadingFont',
        ) 
        import base64
        import io
        # print(data["l"] + data["data_url"] )
        image_data = base64.b64decode(data['data_url'])
        image_stream = io.BytesIO(image_data)
        
        image_ = Image.open(image_stream)

        image_.save('.brain.png')

        # image = ImageTk.PhotoImage(Image.open('.brain.png'))
        helina = PhotoImage(file = '.brain.png')
        ans.insert(0, helina)
    
        canvas.create_image(
            (900.0, 300.0),
            image=ans[0]
        )
        
        
        


   

# Load image
image = ImageTk.PhotoImage(Image.open('./b.png'))
#
# Add image to canvas
verify_icon = canvas.create_image(
   (900.0, 600.0),
   image=image
)
#



canvas.tag_bind(
   verify_icon,
   "<Button-1>",
   my_command
)
#
#
# Create OptionMenu
#options = ['Select', 'Option 1', 'Option 2', 'Option 3', 'Option 4']
#variable = StringVar(window)
#variable.set(options[0])
#
#option_menu = OptionMenu(window, variable, *options)
#
# Create Combobox
#
window.resizable(False, False)

window.mainloop()
