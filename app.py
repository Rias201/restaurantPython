import random, datetime, threading, os
from tkinter import *
from tkinter import simpledialog, ttk, messagebox as msgbox
from database import *
from PIL import Image, ImageTk
from sendPDF import get_pdf, send_pdf

CHAMPAGNE_BG_COLOR = '#FFE4C4'
DARK_BLUE_BG_COLOR = '#38618C'
LIGHT_RED_BG_COLOR = '#FF5964'
BLUE_BG_COLOR = '#35A7FF'
RED_BG_COLOR = '#E3170A'
GRN_BG_COLOR = '#20BF55'
PINK_BG_COLOR = '#0A95FF'
BTN_ACTIVE_BG_COLOR = '#70C1FF'
BTN_DISABLED_GRN_COLOR = '#62E48D'
BTN_DISABLED_RED_COLOR = '#F85A4F'

def abs_path(relative_path):
    return os.path.join(os.path.dirname(__file__), relative_path)

def cancelar_comanda(n_taula, window):
    if delete_comanda(n_taula):
        list(taules_ocupades)[n_taula-1].config(bg=DARK_BLUE_BG_COLOR)
        taules_ocupades[list(taules_ocupades)[n_taula-1]] = 0
        window.destroy()
    else:
        msgbox.showerror("BD Error", "No s'ha pogut esborrar la comanda.",parent=window)

def check_if_done(t):
    print("Fent comprobació d'execució")
    # Si ha acabat l'execució del fil, activem el botó
    if not t.is_alive():
        fact_btn.config(state=NORMAL)
    else:
        # En cas negatiu, tornem a comprobar
        factura_thread_check(t)

def clear_check():
    # Habilitem el textarea
    check_txt.config(state=NORMAL)
    # Borrem el textarea
    check_txt.delete(1.0,END)
    # I el tornem a fer READONLY
    check_txt.config(state=DISABLED)
    fact_btn.config(state=DISABLED)

def crear_taula_aliments(n_taula,plat):
    menu_plats(n_taula,plat)

def enviar_factura():
    fact_btn.config(state=DISABLED)
    # Preguntem a quin mail s'envia
    email = simpledialog.askstring("Email", "A quin email s'envia la factura?")
    # Generem un fil d'execució per a la creació del PDF i per l'enviament
    t = threading.Thread(target=get_pdf(check_taula,check_num,check_comanda))
    t.start()
    factura_thread_check(t)

    t = threading.Thread(target=send_pdf(email))
    t.start()
    factura_thread_check(t)

    msgbox.showinfo("Factura enviada","La factura s'ha enviat correctament amb format PDF.")

def factura_thread_check(t):
    main.after(1000,check_if_done,t)

def fer_check(n_taula, window):
    global check_taula
    global check_num
    global check_comanda

    # Recollim la comanda
    productes = recollir_comanda(n_taula,'*')
    llista_articles = list()
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
            check += f"{f'{producte[3] * producte[2]:.2f}':>5} €\n"
            subtotal += producte[3] * producte[2]
            article = list()
            article.append(producte[2])
            article.append(producte[1])
            article.append(producte[3])
            llista_articles.append(tuple(article))
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
        list(taules_ocupades)[n_taula-1].config(bg=DARK_BLUE_BG_COLOR)
        taules_ocupades[list(taules_ocupades)[n_taula-1]] = 0
        window.destroy()

        # Activem l'opció de fer el PDF
        check_taula = n_taula
        check_num = productes[0][0]
        check_comanda = llista_articles
        fact_btn.config(state=NORMAL)
    else:
        msgbox.showinfo("Comanda no registrada", "No es pot fer check d'una comanda que no ha sigut registrada.",parent=window)

def generate_bg_image(image,width,height):
    # Agafem una imatge aleatoria del nostre lllistat
    foto = Image.open(abs_path(image))
    # Marquem la mida de l'imatge
    foto = foto.resize((width,height))
    f = ImageTk.PhotoImage(foto)
    return f

def historial_comandes():
    # Fer ttk.combobox
    # window = Toplevel()
    # window.title("Prova 1")
    # window.attributes("-fullscreen", True)
    # Label(window, text="Hola, sóc una prova").pack()
    historial = historic(datetime.date.today())
    for registre in historial:
        print(f"{registre[0]}. Taula n: {registre[1]}, Article: {registre[2].capitalize()}, Quantitat: {registre[3]}")
    # window.mainloop()

def menu_plats(n_taula,tipus):
    llista_plats = ["entrant","1r plat","2n plat","acompanyaments","beguda","postre","cafè i petit fours"]

    def clear_window():
        for widget in menu_aliments.winfo_children():
            # print(widget.cget("class"))
            widget.destroy()
    
    def enrere():
        menu_aliments.destroy()
        cont = 0
        for i in llista_plats:
            if i == tipus:
                menu_plats(n_taula, llista_plats[cont-1])
            cont+=1

    def endavant():
        menu_aliments.destroy()
        cont = 0
        for i in llista_plats:
            if i == tipus:
                menu_plats(n_taula, llista_plats[cont+1])
            cont+=1
    
    def guardar_comanda():
        dict_comanda = {}
        
        for i in range(len(llista_int_vars)):
            if llista_int_vars[i].get() != 0:
                dict_comanda[llista_productes[i]] = llista_int_vars[i].get()
        if not afegir_comanda(n_taula, dict_comanda):
            msgbox.showerror("BD Error", "No s'ha pogut guardar la comanda.",parent=menu_aliments)
        # else:
            # msgbox.showinfo("Comanda guardada","S'ha guardat la comanda",parent=menu_aliments)
        
    
    def restar(index):
        if llista_int_vars[(index)-(7*(page-1))].get() > 0: 
            num_actual = llista_int_vars[(index)-(7*(page-1))].get()
            llista_int_vars[(index)-(7*(page-1))].set(num_actual-1)
            
    def sumar(index):
        num_actual = int(llista_int_vars[(index)-(7*(page-1))].get())
        llista_int_vars[(index)-(7*(page-1))].set(num_actual+1)

    def crea_pag(page):
        # Pag title
        Label(menu_aliments, text=f"{tipus.capitalize()}", font=("Impact", 40),bg=CHAMPAGNE_BG_COLOR).grid(row=0,column=0, columnspan=5, ipady=30)
        try:
            # Col·locació elements a la pàgina
            for i in range(7*page-7, 7*page):
                # imatge
                foto = generate_bg_image(llista_product_completa[i][3],75,75)
                lbl = Label(menu_aliments,compound=LEFT, font=("Gabriola",20),image=foto,bg="#722F37")
                lbl.image = foto
                lbl.grid(row=(i+1)-(7*(page-1)), column=1, padx=20, pady=5)
                # Nom del producte
                Label(menu_aliments,compound=LEFT, text=llista_productes[i].capitalize(), font=("Gabriola",20),bg=CHAMPAGNE_BG_COLOR).grid(row=(i+1)-(7*(page-1)), column=2, padx=20, pady=5)
                # Suma, resta d'stock
                Button(menu_aliments, text="➕",font=("Gabriola",10),bg=BLUE_BG_COLOR,activebackground=BTN_ACTIVE_BG_COLOR,width=4, command=lambda plat=i : sumar(plat)).grid(row=(i+1)-(7*(page-1)), column=5, padx=20,pady=10)
                Button(menu_aliments, text="➖",font=("Gabriola",10),bg=BLUE_BG_COLOR,activebackground=BTN_ACTIVE_BG_COLOR,width=4, command=lambda plat=i : restar(plat)).grid(row=(i+1)-(7*(page-1)), column=3, padx=20,pady=10)
                # Entry d'stock
                Entry(menu_aliments, font=("Kameron", 20), width=3, justify=CENTER, textvariable=llista_int_vars[i]).grid(row=(i+1)-(7*(page-1)), column=4)
        except IndexError:
            pass   
        # canviar de pagina amb limitadors
        if page == 1:
            Button(menu_aliments, text="<",font=("Gabriola",10),width=4, command=lambda:canviar_pag_ant(page), state=DISABLED, relief=RIDGE,bg=BTN_DISABLED_GRN_COLOR).grid(row=8,column=5,padx=20,pady=5,sticky="nse")
        else:
             Button(menu_aliments, text="<",font=("Gabriola",10),width=4, command=lambda:canviar_pag_ant(page), bg=GRN_BG_COLOR,activebackground=BTN_DISABLED_GRN_COLOR).grid(row=8,column=5,padx=20,pady=5,sticky="nse")

        if len(llista_productes) <= page*7:
            Button(menu_aliments, text=">",font=("Gabriola",10),width=4, command=lambda:canviar_pag_seg(page), state=DISABLED, relief=RIDGE, bg=BTN_DISABLED_GRN_COLOR).grid(row=8,column=6,padx=20,pady=5,sticky="nsw")
        else:
            Button(menu_aliments, text=">",font=("Gabriola",10),width=4, command=lambda:canviar_pag_seg(page), bg=GRN_BG_COLOR, activebackground=BTN_DISABLED_GRN_COLOR).grid(row=8,column=6,padx=20,pady=5,sticky="nsw")

        # Botó enrere
        Button(menu_aliments,text="Enrere",font=("Gabriola",10),width=20,bg=LIGHT_RED_BG_COLOR, activebackground="#FFC2C6",command=menu_aliments.destroy).grid(row=8,column=3,columnspan=2,sticky="nsw")  
        # Botó guardar comanda
        Button(menu_aliments,text="Guardar comanda",font=("Gabriola",10),width=30, bg=GRN_BG_COLOR, activebackground="#FFC2C6",command=guardar_comanda).grid(row=8,column=1,columnspan=2,sticky="nse", padx=30)
        # Botó enrere menu
        if tipus!="entrant":
            Button(menu_aliments,text="👈",font=("Gabriola",20),bg=PINK_BG_COLOR,activebackground="#FEEBFB",command=enrere).grid(row=1,column=0,rowspan=7,sticky="nsw")
        else:
            Button(menu_aliments,text="👈",font=("Gabriola",20),bg=PINK_BG_COLOR,activebackground="#FEEBFB",command=enrere,relief=RIDGE,state=DISABLED).grid(row=1,column=0,rowspan=7,sticky="nsw")
        # Botó següent menu
        if tipus != "cafè i petit fours":
            Button(menu_aliments,text="👉",font=("Gabriola",20),bg=PINK_BG_COLOR,activebackground="#FEEBFB",command=endavant).grid(row=1,column=6,rowspan=7,sticky="nse")
        else:
            Button(menu_aliments,text="👉",font=("Gabriola",20),bg=PINK_BG_COLOR,activebackground="#FEEBFB",command=enrere,relief=RIDGE,state=DISABLED).grid(row=1,column=6,rowspan=7,sticky="nse")

        resize(None,menu_aliments)
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

    # Inicialització de variables per a la finestra
    llista_productes= list()
    llista_int_vars = list()
    llista_product_completa = recollir_productes(tipus)
    llista_comanda = recollir_comanda(n_taula,tipus)
    
    # Creació finestra menú aliments
    menu_aliments = Toplevel()
    # Configuració finestra menu aliments
    menu_aliments.title(f"{tipus}")
    menu_aliments.config(bg=CHAMPAGNE_BG_COLOR)
    menu_aliments.attributes("-fullscreen", True)
    menu_aliments.grid_rowconfigure((0,1,2,3,4,5,6,7,8),weight=1)
    menu_aliments.grid_columnconfigure((0,1,2,3,4,5,6),weight=1)
    menu_aliments.iconbitmap(abs_path("./img/icon.ico"))

    for i in range (len(llista_product_completa)):
        llista_productes.append(llista_product_completa[i][0])
        llista_int_vars.append(IntVar(value=0))
    
    # Agafa els valors inicials de la comanda
    for i in range(len(llista_comanda)):
        if llista_comanda[i][1] in llista_productes:
            index = llista_productes.index(llista_comanda[i][1])
            llista_int_vars[index].set(llista_comanda[i][2])

    # Crea la pàgina de productes
    page = crea_pag(1)

    menu_aliments.bind('<Configure>', resize)
    menu_aliments.mainloop()

def menu_taula(n_taula):
    if taules_ocupades[list(taules_ocupades)[n_taula-1]] == 0:
        if create_comanda(n_taula):
            list(taules_ocupades)[n_taula-1].config(bg=LIGHT_RED_BG_COLOR)
            taules_ocupades[list(taules_ocupades)[n_taula-1]] = 1
        else:
            msgbox.showerror("BD Error", "No s'ha pogut crear la comanda.",parent=window)
        

    # Creació de la finestra de menú
    window = Toplevel()
    # Configuració finestra de menú
    window.title("Menú taules")
    window.config(bg=CHAMPAGNE_BG_COLOR)
    window.attributes('-fullscreen',True)
    window.iconbitmap(abs_path("./img/icon.ico"))

    window.grid_rowconfigure(0,weight=1)
    window.grid_rowconfigure(1,weight=10)
    window.grid_columnconfigure(0,weight=1)
    
    # Elements de la finestra principal
    Label(window,text=f"Menú taula {n_taula}",font=("Gabriola",40),bg=CHAMPAGNE_BG_COLOR).grid(row=0)
    main_frame = Frame(window,bg=CHAMPAGNE_BG_COLOR)

    # Col·locació elements finestra principal
    main_frame.grid(row=1,sticky="nsew")
    
    # Responsive main_frame
    n_rows = 4
    n_cols = 3
    for i in range(0,n_rows):
        main_frame.grid_rowconfigure(i, weight=1)
    for i in range(0,n_cols):
        main_frame.grid_columnconfigure(i, weight=1)
        
    # Elements main_frame
    ## Primera filera
    Button(main_frame,text="Entrants",font=("Gabriola",20),bg=BLUE_BG_COLOR,width=15,command=lambda:crear_taula_aliments(n_taula,"entrant")).grid(row=0,column=0,padx=20,pady=20,sticky="nsew")
    Button(main_frame,text="Primer Plat",font=("Gabriola",20),bg=BLUE_BG_COLOR,width=15,command=lambda:crear_taula_aliments(n_taula,"1r plat")).grid(row=0,column=1,padx=20,pady=20,sticky="nsew")
    Button(main_frame,text="Segon Plat",font=("Gabriola",20),bg=BLUE_BG_COLOR,width=15,command=lambda:crear_taula_aliments(n_taula,"2n plat")).grid(row=0,column=2,padx=20,pady=20,sticky="nsew")
    ## Segona filera
    Button(main_frame,text="Acompanyaments",font=("Gabriola",20),bg=BLUE_BG_COLOR,width=15,command=lambda:crear_taula_aliments(n_taula,"acompanyaments")).grid(row=1,column=0,padx=20,pady=20,sticky="nsew")
    Button(main_frame,text="Begudes",font=("Gabriola",20),bg=BLUE_BG_COLOR,width=15,command=lambda:crear_taula_aliments(n_taula,"beguda")).grid(row=1,column=1,padx=20,pady=20,sticky="nsew")
    Button(main_frame,text="Postres",font=("Gabriola",20),bg=BLUE_BG_COLOR,width=15,command=lambda:crear_taula_aliments(n_taula,"postre")).grid(row=1,column=2,padx=20,pady=20,sticky="nsew")
    ## Tercera filera
    Button(main_frame,text="Fer el check",font=("Gabriola",20),bg=GRN_BG_COLOR,width=15,command=lambda:fer_check(n_taula, window)).grid(row=2,column=0,padx=20,pady=20,sticky="nsew")
    Button(main_frame,text="Cafè i petit fours",font=("Gabriola",20),bg=BLUE_BG_COLOR,width=15,command=lambda:crear_taula_aliments(n_taula,"cafè i petit fours")).grid(row=2,column=1,padx=20,pady=20,sticky="nsew")
    Button(main_frame,text="Cancelar comanda",font=("Gabriola",20),bg=RED_BG_COLOR,width=15,command=lambda:cancelar_comanda(n_taula, window)).grid(row=2,column=2,padx=20,pady=20,sticky="nsew")
    ## Quarta filera
    Button(main_frame,text="Enrere",font=("Gabriola",20),bg=LIGHT_RED_BG_COLOR,width=15,command=window.destroy).grid(row=3,column=1,padx=20,pady=20,sticky="nsew")

    window.mainloop()

# resize button text size
def resize(e=None,window=None):
    if e != None:
        # print(e.widget.master.winfo_class())
        # get window width 
        lbl_font_size = e.width//40
        btn_font_size = e.width//65
        inp_font_size = e.width//45
        window = e.widget
    else:
        lbl_font_size = window.winfo_screenwidth()//40
        btn_font_size = window.winfo_screenwidth()//65
        inp_font_size = window.winfo_screenwidth()//45

    # define text size on different condition
    for widget in window.winfo_children():
        if widget.master.winfo_class() == 'Tk':
            if widget.winfo_class() == 'Label':
                widget['font'] = widget['font'].split(' ')[0] + ' ' + str(lbl_font_size)
            elif widget.winfo_class() == 'Frame':
                for widget2 in widget.winfo_children():
                    if widget2.winfo_class() == 'Button':
                        widget2['font'] = widget2['font'].split(' ')[0] + ' ' + str(btn_font_size)
        elif widget.master.winfo_class() == 'Toplevel':
            if widget.winfo_class() == 'Label':
                widget['font'] = widget['font'].split(' ')[0] + ' ' + str(lbl_font_size)
            elif widget.winfo_class() == 'Button':
                widget['font'] = widget['font'].split(' ')[0] + ' ' + str(btn_font_size)
            elif widget.winfo_class() == 'Entry':
                widget['font'] = widget['font'].split(' ')[0] + ' ' + str(inp_font_size)

# Comença programa
# Inicialització de variables
imatges_taules = ["./img/taula_1.png","./img/taula_2.png","./img/taula_3.png"]
taules_ocupades = dict()
check_taula = 0
check_num = 0
check_comanda = []

# Creació de la finestra principal
main = Tk()
# Configuració finestra principal
main.title("QwikOrder")
main.attributes('-fullscreen',True)
main.config(bg=CHAMPAGNE_BG_COLOR)
main.iconbitmap(abs_path("./img/icon.ico"))

# Fer responsive finestra principal
main.grid_rowconfigure(0,weight=1)
main.grid_rowconfigure(1,weight=3)
main.grid_columnconfigure(0,weight=2)
main.grid_columnconfigure(1,weight=1)

# Elements de la finestra principal
title_lbl = Label(main,text="La Cuina dels Sentits",font=("Gabriola",25),bg=CHAMPAGNE_BG_COLOR)
left_frame = Frame(main,bg=CHAMPAGNE_BG_COLOR)
right_frame = Frame(main,bg=CHAMPAGNE_BG_COLOR)

# Col·locació dels elements de la finestra principal
title_lbl.grid(row=0,column=0,columnspan=2)
left_frame.grid(row=1,column=0,sticky="nsew")
right_frame.grid(row=1,column=1,sticky="nsew")

# Fer responsive frame esquerre
n_rows, n_cols = 5, 5
for i in range(n_rows):
    left_frame.grid_rowconfigure(i, weight=1)
    left_frame.grid_columnconfigure(i, weight=1)

# Elements del frame esquerre
for i in range(0,25):
    foto = generate_bg_image(random.choice(imatges_taules),100,100)
    btn = Button(left_frame,text=str(i+1),bg=DARK_BLUE_BG_COLOR,fg="White",font=("Impact",18),image=foto,compound=CENTER,command=lambda i=i+1:menu_taula(i))
    btn.image = foto
    taules_ocupades[btn] = 0
    btn.grid(row=i//5,column=i-5*(i//5),sticky="nsew")

# Fer responsive frame dret
right_frame.grid_rowconfigure((0,1,2),weight=1)
right_frame.grid_columnconfigure((0,1),weight=1)

# Elements del frame dret
check_txt = Text(right_frame,font=("Courier New",12),state=DISABLED,width=50,height=30)
fact_btn = Button(right_frame,text="PDF",font=("Impact",18),bg=BLUE_BG_COLOR,state=DISABLED,command=enviar_factura)
clear_btn = Button(right_frame,text="C",font=("Impact",18),bg=BLUE_BG_COLOR,command=clear_check)
hist_btn = Button(right_frame,text="HIST",font=("Impact",18),bg=BLUE_BG_COLOR,command=historial_comandes)
quit_btn = Button(right_frame,text="X",font=("Impact",18),bg="red",command=main.destroy)

# Col·locació dels elements del frame dret
check_txt.grid(row=0,column=0,columnspan=2,sticky=NS)
fact_btn.grid(row=1,column=0,sticky="nsew")
clear_btn.grid(row=1,column=1,sticky="nsew")
hist_btn.grid(row=2,column=0,sticky="nsew")
quit_btn.grid(row=2,column=1,sticky="nsew")

# it will call resize function
# when window size will change
main.bind('<Configure>', resize)
main.mainloop()