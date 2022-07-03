import tkinter as tk
from tkinter import *

root = tk.Tk()
root.title('XXII Roatan International Fishing Tournament')


HEIGHT = 250
WIDTH = 300

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()
btn_color = "#ffebcc"
register_font = "times 14"

def checkbutton():

        def isChecked_C7(): 

                if CheckVar7.get() == 1:
                    estado = TRUE
                else:
                    estado = FALSE
                
                print(estado)
                return(estado)

        font_text_ins = "times 12"

        CheckVar7 = tk.IntVar()
        C7 = tk.Checkbutton(canvas, text = "Clean Release", command=isChecked_C7, bg = "white",font=font_text_ins, variable = CheckVar7, onvalue = 1, offvalue = 0, height=2, width = 20, anchor='w')
        C7.place(relx=0.20, rely=0.68)  

button8 = tk.Button(canvas, text="Register Additional Catch", command=checkbutton, font=register_font, bg=btn_color)
button8.place(relx=0.35, rely=0.93)





root.resizable(False, False)
root.mainloop()