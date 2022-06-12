from tkinter import *
from tkinter.filedialog import askopenfile
from PIL import Image
import os
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.spatial import KDTree
from webcolors import (
    CSS3_HEX_TO_NAMES,
    hex_to_rgb,
)

root = Tk()
root.title("Color Detection Application")
root.geometry('968x720')

frm = Frame(root,width=300,height=300)
frm.grid(sticky="NW")

lb = Label(root,text = "Please click the button to upload the input image",font='Arial 17 bold')
lb.place(relx=0.5,rely=0.1,anchor=CENTER)   

input1 = Label(root,text = "Please enter the number of pixels needed in a row")
input1.place(relx=0.5,rely=0.5,anchor=E)
cnum = IntVar()
e1 = Entry(root,textvariable=cnum).place(relx=0.5,rely=0.5,anchor=W)

input2 = Label(root,text = "Please enter the number of rows needed in the output")
input2.place(relx=0.5,rely=0.6,anchor=E)
rnum = IntVar()
e2 = Entry(root,textvariable =rnum).place(relx=0.5,rely=0.6,anchor=W)


def getAvgRGB(pixarr,co,ro,w,h):
    num=0
    mr,mg,mb=0,0,0
    for i in range(ro,h+ro):
        for j in range(co,w+co):
            # print("i = ",i, "j = ",j)
            r,g,b=pixarr[i][j]
            mr+=r
            mg+=g
            mb+=b
            num+=1
    return (mr/num,mg/num,mb/num)
     
  
def mapping(pixval,width,height,w,h):
    k = 0
    pix2D = [[0 for i in range(width)] for j in range(height)]
    for i in range(height):
        for j in range(width):
            pix2D[i][j] = pixval[k]
            k+=1
    col = math.floor(width/w)
    row = math.floor(height/h)
    resarr = [[0 for i in range(col)] for j in range(row)]
    for i in range(row):
        for j in range(col):
            resarr[i][j] = getAvgRGB(pix2D,j*w,i*h,w,h)
    
    for i in range(len(resarr)):
            for j in range(len(resarr[i])):
                print("(",i,",",j,"): ",convert_rgb_to_names(resarr[i][j]))

    plt.imshow(np.array(resarr).astype('uint8'))
    plt.axis('off')
    plt.show()


def open_file():
    file_path = askopenfile(mode='r', filetypes=[('Image Files', '*jpg')])
    if file_path:
        flpth = os.path.abspath(file_path.name)
        fp = Label(root,text=flpth+" Upload Successful")
        fp.place(relx=0.5,rely=0.9,anchor=CENTER)
        im = Image.open(flpth,'r')
        width, height = im.size
        w = math.floor(width/cnum.get())
        h = math.floor(height/rnum.get())
        pixval = list(im.getdata())
        mapping(pixval,width,height,w,h)


def convert_rgb_to_names(rgb_tuple):
    
    # a dictionary of all the hex and their respective names in css3
    css3_db = CSS3_HEX_TO_NAMES
    names = []
    rgb_values = []    
    
    for color_hex, color_name in css3_db.items():
        names.append(color_name)
        rgb_values.append(hex_to_rgb(color_hex))
    
    kdt_db = KDTree(rgb_values)    
    distance, index = kdt_db.query(rgb_tuple)
    return f'closest match: {names[index]}'


btn = Button(root, text = "Upload image",fg = "red", font=('Arial 12 bold'), command=open_file)
btn.place(relx=0.5,rely=0.8,anchor=CENTER)
root.mainloop()