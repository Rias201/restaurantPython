import random
from tkinter import *

imatges_taules = ["./img/taula1.png","./img/taula3.png","./img/taula3.png"]

# Creació de la finestra principal
main = Tk()
# Configuració finestra principal
main.title("Gestió del restaurant")
main.resizable(0,0)

# Elements de la finestra principal
title_lbl = Label(main, text="La Cuina dels Sentits", font=("Gabriola",20))
left_frame = Frame(main)

# Col·locació dels elements de la finestra principal
title_lbl.pack(side=TOP)
left_frame.pack(side=LEFT)

# Elements del frame esquerra
for i in range(0,25):
    btn = Button(left_frame,text=str(i+1),bg="Tomato",fg="Black",font=("Impact", 16),image=random.choice(imatges_taules))
    btn.grid(row=i//5,column=i-5*(i//5),sticky=N+S+E+W)

main.mainloop()