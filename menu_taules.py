from tkinter import *

def crear_taula_aliments(plat):
    pass

def menu_taula(taula):
    window = Toplevel()

    window.title("Menú taules")
    window.resizable(0,0)

    Label(window,text=f"Menú taula {taula}",font=("Gabriola",40)).grid(row=0,column=1)


    Button(window,text="Entrants",font=("Gabriola",20),command=lambda:crear_taula_aliments("entrant"),width=15).grid(row=1,column=0,padx=20,pady=20)
    Button(window,text="Primer Plat",font=("Gabriola",20),command=lambda:crear_taula_aliments("1rplat"),width=15).grid(row=1,column=1,padx=20,pady=20)
    Button(window,text="Segon Plat",font=("Gabriola",20),command=lambda:crear_taula_aliments("2nplat"),width=15).grid(row=1,column=2,padx=20,pady=20)

    Button(window,text="Acompanyaments",font=("Gabriola",20),command=lambda:crear_taula_aliments("acompanyaments"),width=15).grid(row=2,column=0,padx=20,pady=20)
    Button(window,text="Begudes",font=("Gabriola",20),command=lambda:crear_taula_aliments("beguda"),width=15).grid(row=2,column=1,padx=20,pady=20)
    Button(window,text="Postres",font=("Gabriola",20),command=lambda:crear_taula_aliments("postre"),width=15).grid(row=2,column=2,padx=20,pady=20)

    Button(window,text="Cafè i petit fours",font=("Gabriola",20),command=lambda:crear_taula_aliments("cafè i petit fours"),width=15).grid(row=3,column=0,padx=20,pady=20)
    Button(window,text="Fer el check",font=("Gabriola",20),width=15).grid(row=3,column=1,columnspan=2,padx=20,pady=20)

    window.mainloop()