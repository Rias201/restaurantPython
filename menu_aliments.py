from tkinter import *
from database import *




# variable per a saber quin tipues de plat es, s'ha d'agafar de la pantalla anterior.
def menu_plats(tipus):
    
    def clear_window():
        for widget in main.winfo_children():
            # print(widget.cget("class"))
            widget.destroy()
    
    def restar(index):
        if llista_int_vars[(index)-(7*(page-1))].get() > 0: 
            num_actual = llista_int_vars[(index)-(7*(page-1))].get()
            llista_int_vars[(index)-(7*(page-1))].set(num_actual-1)
            
    def sumar(index):
        num_actual = int(llista_int_vars[(index)-(7*(page-1))].get())
        llista_int_vars[(index)-(7*(page-1))].set(num_actual+1)

    def crea_pag(page):
        print("pag creada")
        # Pag title
        Label(main, text=f"{tipus}", font=("Gabriola",30)).grid(row=0,column=0)
        try:
            # Col·locació elements a la pàgina
            for i in range(7*page-7, 7*page):
                # Nom del producte
                Label(main, text=llista_productes[i], font=("Gabriola",20), width=52).grid(row=(i+1)-(7*(page-1)), column=0, padx=20, pady=5)
                # Suma, resta d'stock
                Button(main, text="➕",font=("Gabriola",10),width=4, command=lambda plat=i : sumar(plat)).grid(row=(i+1)-(7*(page-1)), column=3, padx=20,pady=10)
                Button(main, text="➖",font=("Gabriola",10),width=4, command=lambda plat=i : restar(plat)).grid(row=(i+1)-(7*(page-1)), column=1, padx=20,pady=10)
                # Entry d'stock
                Entry(main, font=("Kameron", 20), width=3, justify=CENTER, textvariable=llista_int_vars[i]).grid(row=(i+1)-(7*(page-1)), column=2)
        except IndexError:
            pass   
        # canviar de pagina amb limitadors
        if page == 1:
            Button(main, text="<",font=("Gabriola",10),width=4, command=lambda:canviar_pag_ant(page), state=DISABLED, relief=RIDGE).grid(row=8,column=1, padx=20,pady=5)
        else:
             Button(main, text="<",font=("Gabriola",10),width=4, command=lambda:canviar_pag_ant(page)).grid(row=8,column=1, padx=20,pady=5)

        if len(llista_productes) <= page*7:
            Button(main, text=">",font=("Gabriola",10),width=4, command=lambda:canviar_pag_seg(page), state=DISABLED, relief=RIDGE).grid(row=8,column=3, padx=20,pady=5)
        else:
            Button(main, text=">",font=("Gabriola",10),width=4, command=lambda:canviar_pag_seg(page)).grid(row=8,column=3, padx=20,pady=5)
                  
        return page
    # funcions canviar pàgina
    def canviar_pag_seg(pag):
        global page
        clear_window()
        page = crea_pag(pag+1)

    def canviar_pag_ant(pag):
        global page
        clear_window()
        page = crea_pag(pag-1)

    
    llista_productes= list()
    llista_int_vars = list()
    llista_product_completa = recollir_productes(tipus)
    
    main = Toplevel()

    main.title(f"{tipus}")
    main.resizable(0,0)

    for i in range (len(llista_product_completa)):
        llista_productes.append(llista_product_completa[i][0])
        llista_int_vars.append(IntVar(value=0))

    page = crea_pag(1)

    main.mainloop()

menu_plats("beguda")
