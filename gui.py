import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from main import classify

root = tk.Tk()
root.geometry(('400x400'))
label = tk.Label(root, text='Upload an image of an animal to see a fun fact!',
                 wraplength=300)
label.pack()
canvas = tk.Canvas(root)
photo = None

def upload():
    file_path = filedialog.askopenfile(initialdir = '.', filetypes=[('*.jpeg', '*.jpg')]).name
    # get fun fact
    if file_path:
        fun_fact = classify(file_path)
    else:
        fun_fact = ''

    label['text'] = fun_fact

    # display image
    im = Image.open(file_path)
    # im = im.resize((50,50))
    photo = ImageTk.PhotoImage(im)
    canvas.delete('all')
    canvas.create_image((0,0), image=photo, anchor="s")
    canvas.pack()

# add components
tk.Button(root, text='Upload', command=upload).pack()
root.mainloop()
