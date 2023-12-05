import random
from tkinter import *
from tkinter import messagebox as msgbox
from database import *
from PIL import Image, ImageTk

TABLE_DEFAULT_BG_COLOR = 'SlateGray'
TABLE_OCUPPIED_BG_COLOR = 'DarkSlateGray'

def clear_check():
    # Habilitem el textarea
    check_txt.config(state="normal")
    # Borrem el textarea
    check_txt.delete(1.0,END)
    # I el tornem a fer READONLY
    check_txt.config(state="disabled")

def crear_taula_aliments(n_taula,plat):
    menu_plats(n_taula,plat)

# Evita que es pugui tancar la finestra amb la X
def disable_event():
    pass

def fer_check(n_taula, finestra):
    # Recollim la comanda
    productes = recollir_comanda(n_taula)
    if len(productes) != 0:
        # Fem el check
        subtotal = 0.0
        check = f"{'======================================':^50}"
        check += f"{'La Cuina dels Sentits':^50}"
        check += f"{f'Check: {productes[0][0]}':^25}{f'Taula: {n_taula}':^25}"
        check += f"{'======================================':^50}\n\n"
        # Fem una fila per a cada producte indicant quantitat, nom i preu total
        for producte in productes:
            check += f"{f'{producte[2]}':>5} "
            check += f"{f'{producte[1][:32].capitalize()}':<32} "
            check += f"{f'{producte[3] * producte[2]}':>5} €\n"
            subtotal += producte[3] * producte[2]
        check += f"\n{'----------------------':^50}"
        check += f"{'Subtotal':>25} "
        check += f"{f'{subtotal:.2f}':>7} €\n"
        check += f"{'Impostos':>25} "
        check += f"{f'{subtotal*21/100:.2f}':>7} €\n"
        check += f"{'Total':>25} "
        check += f"{f'{subtotal + subtotal*21/100:.2f}':>7} €\n\n"
        check += f"{'**************************************':^50}"
        check += f"{'****************************':^50}"

        # Habilitem escriptura al check
        check_txt.config(state="normal")
        # Borrem (per si algún cas) el check
        check_txt.delete(1.0, END)
        # Escrivim el check
        check_txt.insert(END, check)
        # Habilitem READ-ONLY al check
        check_txt.config(state="disabled")
        list(taules_ocupades)[n_taula-1].config(bg=TABLE_DEFAULT_BG_COLOR)
        taules_ocupades[list(taules_ocupades)[n_taula-1]] = 0
        finestra.destroy()
    else:
        msgbox.showerror("Error BD", "No hi ha ninguna comanda registrada")

def generate_bg_image():
    # Agafem una imatge aleatoria del nostre lllistat
    foto = Image.open(random.choice(imatges_taules))
    # Marquem la mida de l'imatge
    foto = foto.resize((100,100))
    f = ImageTk.PhotoImage(foto)
    return f

def menu_plats(n_taula,tipus):
    print(recollir_comanda(n_taula))
    def clear_window():
        for widget in menu_aliments.winfo_children():
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
        # Pag title
        Label(menu_aliments, text=f"{tipus.capitalize()}", font=("Impact",30)).grid(row=0,column=0)
        try:
            # Col·locació elements a la pàgina
            for i in range(7*page-7, 7*page):
                # Nom del producte
                Label(menu_aliments, text=llista_productes[i].capitalize(), font=("Gabriola",20), width=52).grid(row=(i+1)-(7*(page-1)), column=0, padx=20, pady=5)
                # Suma, resta d'stock
                Button(menu_aliments, text="➕",font=("Gabriola",10),width=4, command=lambda plat=i : sumar(plat)).grid(row=(i+1)-(7*(page-1)), column=3, padx=20,pady=10)
                Button(menu_aliments, text="➖",font=("Gabriola",10),width=4, command=lambda plat=i : restar(plat)).grid(row=(i+1)-(7*(page-1)), column=1, padx=20,pady=10)
                # Entry d'stock
                Entry(menu_aliments, font=("Kameron", 20), width=3, justify=CENTER, textvariable=llista_int_vars[i]).grid(row=(i+1)-(7*(page-1)), column=2)
        except IndexError:
            pass   
        # canviar de pagina amb limitadors
        if page == 1:
            Button(menu_aliments, text="<",font=("Gabriola",10),width=4, command=lambda:canviar_pag_ant(page), state=DISABLED, relief=RIDGE).grid(row=8,column=1, padx=20,pady=5)
        else:
             Button(menu_aliments, text="<",font=("Gabriola",10),width=4, command=lambda:canviar_pag_ant(page)).grid(row=8,column=1, padx=20,pady=5)

        if len(llista_productes) <= page*7:
            Button(menu_aliments, text=">",font=("Gabriola",10),width=4, command=lambda:canviar_pag_seg(page), state=DISABLED, relief=RIDGE).grid(row=8,column=3, padx=20,pady=5)
        else:
            Button(menu_aliments, text=">",font=("Gabriola",10),width=4, command=lambda:canviar_pag_seg(page)).grid(row=8,column=3, padx=20,pady=5)
                  
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
    
    menu_aliments = Toplevel()

    menu_aliments.title(f"{tipus}")
    menu_aliments.resizable(0,0)

    for i in range (len(llista_product_completa)):
        llista_productes.append(llista_product_completa[i][0])
        llista_int_vars.append(IntVar(value=0))

    page = crea_pag(1)

    menu_aliments.mainloop()

def menu_taula(taula):
    # Creació de la finestra de menú
    window = Toplevel()
    # Configuració finestra de menú
    window.title("Menú taules")
    window.resizable(0,0)
    window.protocol("WM_DELETE_WINDOW", disable_event)

    # Capçalera de la finestra
    Label(window,text=f"Menú taula {taula}",font=("Gabriola",40)).grid(row=0,column=1)
    # Botons del menú
    ## Primera filera
    Button(window,text="Entrants",font=("Gabriola",20),command=lambda:crear_taula_aliments(taula,"entrant"),width=15).grid(row=1,column=0,padx=20,pady=20)
    Button(window,text="Primer Plat",font=("Gabriola",20),command=lambda:crear_taula_aliments(taula,"1r plat"),width=15).grid(row=1,column=1,padx=20,pady=20)
    Button(window,text="Segon Plat",font=("Gabriola",20),command=lambda:crear_taula_aliments(taula,"2n plat"),width=15).grid(row=1,column=2,padx=20,pady=20)
    ## Segona filera
    Button(window,text="Acompanyaments",font=("Gabriola",20),command=lambda:crear_taula_aliments(taula,"acompanyaments"),width=15).grid(row=2,column=0,padx=20,pady=20)
    Button(window,text="Begudes",font=("Gabriola",20),command=lambda:crear_taula_aliments(taula,"beguda"),width=15).grid(row=2,column=1,padx=20,pady=20)
    Button(window,text="Postres",font=("Gabriola",20),command=lambda:crear_taula_aliments(taula,"postre"),width=15).grid(row=2,column=2,padx=20,pady=20)
    ## Tercera filera
    Button(window,text="Cafè i petit fours",font=("Gabriola",20),command=lambda:crear_taula_aliments(taula,"cafè i petit fours"),width=15).grid(row=3,column=0,padx=20,pady=20)
    Button(window,text="Fer el check",font=("Gabriola",20),width=15,command=lambda:fer_check(taula, window)).grid(row=3,column=1,padx=20,pady=20)
    Button(window,text="Sortir de la taula",font=("Gabriola",20),width=15,bg="coral",command=lambda:tancar_finestra(taula, window)).grid(row=3,column=2,padx=20,pady=20)

    window.mainloop()

def tancar_finestra(n_taula, finestra):
    if len(recollir_comanda(n_taula)) != 0:
        list(taules_ocupades)[n_taula-1].config(bg=TABLE_OCUPPIED_BG_COLOR)
        taules_ocupades[list(taules_ocupades)[n_taula-1]] = 1
    finestra.destroy()

# Comença programa
# Inicialització de variables
imatges_taules = ["./img/taula_1.png","./img/taula_2.png","./img/taula_3.png"]
taules_ocupades = dict()

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
left_frame.pack(side=LEFT,anchor=N)
right_frame.pack(side=RIGHT)

# Elements del frame esquerre
for i in range(0,25):
    foto = generate_bg_image()
    btn = Button(left_frame,text=str(i+1),bg=TABLE_DEFAULT_BG_COLOR,fg="White",font=("Impact",18),image=foto,compound=CENTER,command=lambda i=i+1:menu_taula(i))
    btn.image = foto
    taules_ocupades[btn] = 0
    btn.grid(row=i//5,column=i-5*(i//5),sticky=N+S+E+W)

# Elements del frame dret
check_txt = Text(right_frame,font=("Courier New",12),state="disabled",width=50,height=30)
clear_btn = Button(right_frame,text="C",font=("Impact",18),command=clear_check,bg="HotPink")

# Col·locació dels elements del frame dret
check_txt.grid(row=0,column=0,columnspan=2)
clear_btn.grid(row=1,column=0,columnspan=2,sticky=N+S+W+E)

main.mainloop()