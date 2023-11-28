import random, database
from tkinter import *
from PIL import Image, ImageTk
from menu_taules import menu_taula

def generate_bg_image():
    foto = Image.open(random.choice(imatges_taules))
    foto = foto.resize((100,100))
    f = ImageTk.PhotoImage(foto)
    return f

imatges_taules = ["./img/taula_1.png","./img/taula_2.png","./img/taula_3.png"]

# Creació de la finestra principal
main = Tk()
# Configuració finestra principal
main.title("Gestió del restaurant")
main.resizable(0,0)

# Elements de la finestra principal
title_lbl = Label(main, text="La Cuina dels Sentits", font=("Gabriola",25))
left_frame = Frame(main)
right_frame = Frame(main)

# Col·locació dels elements de la finestra principal
title_lbl.pack(side=TOP)
left_frame.pack(side=LEFT)
right_frame.pack(side=RIGHT)

# Elements del frame esquerre
for i in range(0,25):
    foto = generate_bg_image()
    btn = Button(left_frame,text=str(i+1),bg="SlateGray",fg="White",font=("Impact", 18),image=foto, compound=CENTER,command=lambda i=i+1:menu_taula(i))
    btn.image = foto
    btn.grid(row=i//5,column=i-5*(i//5),sticky=N+S+E+W)

# Elements del frame dret
check_txt = Text(right_frame,font=("Courier New",12),state="normal",width=40,height=30)

# Col·locació dels elements del frame dret
check_txt.grid(row=0,column=0,columnspan=2)

main.mainloop()