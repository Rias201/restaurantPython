import random
from tkinter import *
from tkinter import messagebox as msgbox
from database import *
from PIL import Image, ImageTk

# Color bisque
BG_DEFAULT_COLOR = '#ffe4c4'
# Color dark cream
TABLE_DEFAULT_BG_COLOR = '#fff39a'
# Color verd maragda
TABLE_OCUPPIED_BG_COLOR = '#287233'

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
    llista_comanda = recollir_comanda(n_taula)

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
    window.attributes('-fullscreen',True)
    window.protocol("WM_DELETE_WINDOW", disable_event)

    n_rows = 4
    n_cols = 3
    for i in range(0,n_rows):
        window.grid_rowconfigure(i, weight=1)
    for i in range(0,n_cols):
        window.grid_columnconfigure(i, weight=1)
    
    # Capçalera de la finestra
    Label(window,text=f"Menú taula {taula}",font=("Gabriola",40)).grid(row=0,column=1)
    # Botons del menú
    ## Primera filera
    Button(window,text="Entrants",font=("Gabriola",20),bg="Aquamarine",width=15,command=lambda:crear_taula_aliments(taula,"entrant")).grid(row=1,column=0,padx=20,pady=20,sticky="nsew")
    Button(window,text="Primer Plat",font=("Gabriola",20),bg="Aquamarine",width=15,command=lambda:crear_taula_aliments(taula,"1r plat")).grid(row=1,column=1,padx=20,pady=20,sticky="nsew")
    Button(window,text="Segon Plat",font=("Gabriola",20),bg="Aquamarine",width=15,command=lambda:crear_taula_aliments(taula,"2n plat")).grid(row=1,column=2,padx=20,pady=20,sticky="nsew")
    ## Segona filera
    Button(window,text="Acompanyaments",font=("Gabriola",20),bg="Aquamarine",width=15,command=lambda:crear_taula_aliments(taula,"acompanyaments")).grid(row=2,column=0,padx=20,pady=20,sticky="nsew")
    Button(window,text="Begudes",font=("Gabriola",20),bg="Aquamarine",width=15,command=lambda:crear_taula_aliments(taula,"beguda")).grid(row=2,column=1,padx=20,pady=20,sticky="nsew")
    Button(window,text="Postres",font=("Gabriola",20),bg="Aquamarine",width=15,command=lambda:crear_taula_aliments(taula,"postre")).grid(row=2,column=2,padx=20,pady=20,sticky="nsew")
    ## Tercera filera
    Button(window,text="Cafè i petit fours",font=("Gabriola",20),bg="Aquamarine",width=15,command=lambda:crear_taula_aliments(taula,"cafè i petit fours")).grid(row=3,column=0,padx=20,pady=20,sticky="nsew")
    Button(window,text="Fer el check",font=("Gabriola",20),bg="Chartreuse",width=15,command=lambda:fer_check(taula, window)).grid(row=3,column=1,padx=20,pady=20,sticky="nsew")
    Button(window,text="Sortir de la taula",font=("Gabriola",20),bg="coral",width=15,command=lambda:tancar_finestra(taula, window)).grid(row=3,column=2,padx=20,pady=20,sticky="nsew")

    window.mainloop()

# resize button text size
def resize(e):
    # print(e.widget)
    # get window width 
    lbl_font_size = e.width//40
    btn_font_size = e.width//60

    # define text size on different condition
    for widget in e.widget.winfo_children():
        if widget.master.winfo_class() == 'Tk':
            if widget.winfo_class() == 'Label':
                widget['font'] = widget['font'].split(' ')[0] + ' ' + str(lbl_font_size)
            elif widget.winfo_class() == 'Button':
                widget['font'] = widget['font'].split(' ')[0] + ' ' + str(btn_font_size)

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
main.title("QwikOrder")
main.attributes('-fullscreen',True)
main.config(bg=BG_DEFAULT_COLOR)
# main.resizable(0,0)

# Fer responsive finestra principal
main.grid_rowconfigure(0,weight=1)
main.grid_rowconfigure(1,weight=3,uniform=1)
# main.grid_rowconfigure(2,weight=1)
main.grid_columnconfigure((0,1),weight=1)

# Elements de la finestra principal
title_lbl = Label(main,text="La Cuina dels Sentits",font=("Gabriola",25),bg=BG_DEFAULT_COLOR)
left_frame = Frame(main,bg=BG_DEFAULT_COLOR)
right_frame = Frame(main,bg=BG_DEFAULT_COLOR)
kill_btn = Button(main,text="Kill",font=('Monaco',20),bg="#ae2535",command=main.destroy)

# Col·locació dels elements de la finestra principal
title_lbl.grid(row=0,column=0,columnspan=2)
left_frame.grid(row=1,column=0,sticky="nsew")
right_frame.grid(row=1,column=1,sticky="nsew")
# kill_btn.grid(row=2,column=0,columnspan=2,sticky="nsew")

# Fer responsive frame esquerre
n_rows, n_cols = 5, 5
for i in range(n_rows):
    left_frame.grid_rowconfigure(i, weight=1)
    left_frame.grid_columnconfigure(i, weight=1)

# Elements del frame esquerre
for i in range(0,25):
    foto = generate_bg_image()
    btn = Button(left_frame,text=str(i+1),bg=TABLE_DEFAULT_BG_COLOR,fg="White",font=("Impact",18),image=foto,compound=CENTER,command=lambda i=i+1:menu_taula(i))
    btn.image = foto
    taules_ocupades[btn] = 0
    btn.grid(row=i//5,column=i-5*(i//5),sticky="nsew")

# Fer responsive frame dret
right_frame.grid_rowconfigure((0,1),weight=1)
right_frame.grid_columnconfigure(0,weight=1)

# Elements del frame dret
check_txt = Text(right_frame,font=("Courier New",12),state="disabled",width=50,height=30)
clear_btn = Button(right_frame,text="C",font=("Impact",18),command=clear_check,bg="HotPink")

# Col·locació dels elements del frame dret
check_txt.grid(row=0,column=0,columnspan=2,sticky=NS)
clear_btn.grid(row=1,column=0,columnspan=2,sticky="nsew")

# it will call resize function 
# when window size will change
main.bind('<Configure>', resize)
main.mainloop()































# llista = ['cafè amb llet','gin tonic amb gerds i llimona','picapoll negre','tallat']

# dicc = {
# 'cafè amb llet':1,
# 'gin tonic amb gerds i llimona':3,
# 'picapoll negre':5,
# 'tallat':1,
# 'trufes de xocolata':2,
# 'patates braves':4,
# }

# for i in len(list(dicc.keys())):
#   if list(dicc.keys())[i] in llista:
#     index = llista.index(list(dicc.keys())[i])
#     "UPDATE comandes SET quantitat = %s WHERE producte = %s",(dicc[llista[index]],llista[index])
#   else:
#     n_comanda = "SELECT MAX(id) FROM registres WHERE id_taula = %s",(n_taula,)
#     "INSERT INTO comandes VALUES (%s,%s,%s)",(n_comanda,dicc[llista[index]],llista[index])