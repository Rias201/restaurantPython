from tkinter import *

taula = 1

def crear_taula_aliments(plat):
    pass


main = Toplevel()

main.title("Menú")
main.resizable(0,0)

title_lbl = Label(main, text="Menú taules", font=("Gabriola",40)).grid(row=0, column=1)


Button(main, text="Entrants", font=("Gabriola",20),command=lambda : crear_taula_aliments("entrant"), width=15).grid(row=1, column=0, padx=20, pady=20)
Button(main, text="Primer Plat", font=("Gabriola",20),command=lambda : crear_taula_aliments("1rplat"), width=15).grid(row=1, column=1, padx=20, pady=20)
Button(main, text="Segon Plat", font=("Gabriola",20),command=lambda : crear_taula_aliments("2nplat"), width=15).grid(row=1, column=2, padx=20, pady=20)

Button(main, text="Acompanyaments", font=("Gabriola",20),command=lambda : crear_taula_aliments("acompanyaments"), width=15).grid(row=2, column=0, padx=20, pady=20)
Button(main, text="Begudes", font=("Gabriola",20),command=lambda : crear_taula_aliments("beguda"), width=15).grid(row=2, column=1, padx=20, pady=20)
Button(main, text="Postres", font=("Gabriola",20),command=lambda : crear_taula_aliments("postre"), width=15).grid(row=2, column=2, padx=20, pady=20)

Button(main, text="Cafè i petit fours", font=("Gabriola",20),command=lambda : crear_taula_aliments("cafè i petit fours"), width=15).grid(row=3, column=0, padx=20, pady=20)
Label(main, text=f"Taula {taula}", font=("Gabriola",40), width=15).grid(row=3, column=1,columnspan=2, padx=20, pady=20)

main.mainloop()