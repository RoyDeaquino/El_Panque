import tkinter as tk
from tkinter import ttk, Menu, Toplevel, Image, Text, scrolledtext
from Language import I18N
from Callbacks import Callbacks
from threading import Thread


class Gui:
    """Clase que despliega la GUI"""
    def __init__(self, language='es'):
        self.win = tk.Tk()
        self.i18n = I18N(language)
        self.win.title(self.i18n.title)
        self.win.resizable(1, 1)
        self.win.geometry("1000x600")
        self.pcb = Image("photo", file="Resources/pinguinoChefPanbien.png")
        self.pnv = Image("photo", file="Resources/PinguinoNoVe.png")
        self.pcq = Image("photo", file="Resources/pinguinoChefPanQuemado.png")
        self.img = Image("photo", file="Resources/panque.png")
        self.lpz = Image("photo", file="Resources/lapiz.png")
        self.ojo = Image("photo", file="Resources/ojo.png")
        self.win.tk.call('wm', 'iconphoto', self.win._w, self.img)
        self.call_backs = Callbacks(self)
        # Se llaman metodos que crean los widgets
        self.create_tabs()
        self.create_menubar()
        self.create_tab1()
        self.create_tab2()
        self.create_logo()
        self.total.set("300")
        self.tab_control.select(1)

    def create_tabs(self):
        """Crea las pestañas (notebook) del frame"""
        self.tab_control = ttk.Notebook(self.win)
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab1, text=self.i18n.tab1Text)
        self.tab_control.pack(expand=1, fill="both")

        self.tab2 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab2, text=self.i18n.pedidos)
        self.tab_control.pack(expand=1, fill="both")

        self.tab3 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab3, text=self.i18n.store)
        self.tab_control.pack(expand=1, fill="both")

    def del_tabs(self):
        self.tab_control.destroy()

    def change_language(self, language):
        self.i18n.__init__(language)
        self.del_tabs()
        self.create_tabs()
        self.create_menubar()
        self.create_logo()
        self.create_tab1()
        self.create_tab2()

    def create_menubar(self):
        """Crea el MenuBar del frame"""
        menu_bar = Menu(self.win)
        self.win.config(menu=menu_bar)
        pedidos_menu = Menu(menu_bar, tearoff=0)
        pedidos_menu.add_command(label=self.i18n.new)
        pedidos_menu.add_command(label=self.i18n.list)
        pedidos_menu.add_command(label=self.i18n.search)
        pedidos_menu.add_separator()
        pedidos_menu.add_command(label=self.i18n.exit, command=self.call_backs._quit)
        menu_bar.add_cascade(label=self.i18n.pedidos, menu=pedidos_menu)

        store_menu = Menu(menu_bar, tearoff=0)
        store_menu.add_command(label=self.i18n.new_product)
        menu_bar.add_cascade(label=self.i18n.store, menu=store_menu)

        inv_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label=self.i18n.inv, menu=inv_menu)

        lang_menu = Menu(menu_bar, tearoff=0)
        lang_menu.add_command(label=self.i18n.es, command=lambda: self.change_language("es"))
        lang_menu.add_command(label=self.i18n.en, command=lambda: self.change_language("en"))
        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label=self.i18n.about)
        help_menu.add_cascade(label=self.i18n.lang, menu=lang_menu)
        menu_bar.add_cascade(label=self.i18n.help, menu=help_menu)

    def create_logo(self):
        """Coloca el nombre  y logo de la empresa en todas las pestañas que aparecen en la lista"""
        for tab in [self.tab1, self.tab2, self.tab3]:
            setlogo = ttk.LabelFrame(tab, borderwidth=0)
            setlogo.grid(column=0, row=0, columnspan=8)
            ttk.Label(setlogo, text=self.i18n.title, font=("Z003", 50)).grid(column=0, row=0)
            el_panque = ttk.Label(setlogo, image=self.img)
            el_panque.image = self.img
            el_panque.grid(column=4, row=0, sticky=tk.W)

    def create_tab1(self):
        """Crea el form principal de la caja"""
        ttk.Label(self.tab1, text=self.i18n.total,
                  font=("Source Code Pro Black", 30)).grid(column=7, row=1,
                                                           columnspan=2, padx=4, pady=6)
        self.art = ttk.Treeview(self.tab1, columns=(self.i18n.product, self.i18n.amount, self.i18n.cost))
        self.art.grid(column=0,  row=1, columnspan=6, rowspan=6, padx=5, pady=8, sticky=tk.W+tk.E+tk.N+tk.S)
        self.art.heading("#0", text="N.")
        self.art.column("#0", minwidth=0, width=25, anchor=tk.W, stretch=tk.NO)
        self.art.heading(self.i18n.product, text=self.i18n.product)
        self.art.column(self.i18n.product, minwidth=200, width=350, anchor=tk.CENTER, stretch=tk.NO)
        self.art.heading(self.i18n.amount, text=self.i18n.amount)
        self.art.column(self.i18n.amount, minwidth=50, width=90, anchor=tk.W, stretch=tk.NO)
        self.art.heading(self.i18n.cost, text=self.i18n.cost)
        self.art.column(self.i18n.cost, minwidth=50, width=90, anchor=tk.W, stretch=tk.NO)

        self.total = tk.StringVar()
        self.total_entry = ttk.Entry(self.tab1, width=10, textvariable=self.total, justify=tk.CENTER,
                                     font=("HELVETICA", 35), state=tk.DISABLED)
        self.total_entry.grid(column=7, row=2, columnspan=2, padx=5, pady=5)

        ttk.Label(self.tab1, text=self.i18n.cash,
                  font=("Source Code Pro Black", 30)).grid(column=7, row=3, columnspan=2, padx=4, pady=6)
        self.cash = tk.StringVar()
        self.cash_entry = ttk.Entry(self.tab1, width=10, textvariable=self.cash, justify=tk.CENTER,
                                    font=("HELVETICA", 35)).grid(column=7, row=4, columnspan=2, padx =5, pady=5)

        ttk.Label(self.tab1, text=self.i18n.change,
                  font=("Source Code Pro Black", 30)).grid(column=7, row=5, columnspan=2, padx=4, pady=6)

        self.change = tk.StringVar()
        self.change_entry = ttk.Entry(self.tab1, width=10, textvariable=self.change, justify=tk.CENTER,
                                      font=("HELVETICA", 35), state=tk.DISABLED)
        self.change_entry.grid(column=7, row=6, columnspan=2, padx=5, pady=5)

    def inert_info(self):
        """Inserta la informacion de los productos"""
        descrip = "Delciciosa rebanada de pastel\nde tres leches sabor cajeta\ncon trozos de nuez."
        cost = "\nCosto: 120"
        size = "\nTamaño: Rebanada para 1 persona"
        stock= "\n\nAGOTADO"
        scrol_w = 30;
        scrol_h = 8
        info_text = scrolledtext.ScrolledText(self.tab2, wrap='word', background='aliceBlue', width=scrol_w, height=scrol_h)
        info_text.insert(tk.INSERT,descrip)
        info_text.insert(tk.END, cost)
        info_text.insert(tk.END,size)
        info_text.insert(tk.END,stock)
        info_text.grid(column=5, row=2)
        info_text.tag_add("stock", "7.0", "7.7")
        info_text.tag_config("stock", foreground="red")
        info_text.config(state='disabled')
        self.lbl_name = Text(self.tab2, wrap='word', background='aliceBlue', height=scrol_h, width=scrol_w)
        self.lbl_name.insert(tk.INSERT, 'Pastel de cajeta rebanado')
        self.lbl_name.image_create("current", image=self.pnv)
        self.lbl_name.grid(column=0, row=2, sticky='W')
        self.lbl_name.config(state='disabled')

    def create_tab2(self):
        """Crea el form del tab2"""
        # Head
        ttk.Label(self.tab2, text=self.i18n.products,
                  font=("HELVETICA", 20), relief=tk.SUNKEN).grid(column=0, row=1, columnspan=1, pady=5)
        ttk.Label(self.tab2, text=self.i18n.stock,
                  font=("HELVETICA", 20), width=10, relief=tk.SUNKEN).grid(column=1, row=1, sticky=tk.W,
                                                                           columnspan=2, pady=5)
        ttk.Label(self.tab2, text=self.i18n.edit, font=("HELVETICA", 20), width=6,
                  relief=tk.SUNKEN).grid(column=3, row=1, pady=5)
        ttk.Label(self.tab2, text=self.i18n.details, font=("HELVETICA", 20), width=10,
                  relief=tk.SUNKEN).grid(column=4, row=1, pady=5)
        ttk.Label(self.tab2, text=self.i18n.info, font=("HELVETICA", 20), width=20,
                  relief=tk.SUNKEN).grid(column=5, row=1, pady=5)

        # body cells
        # lbl = ttk.Label(self.tab2, justify='left', compound='left', font=("HELVETICA", 10),
        #                 text='Pastel de cajeta rebanado', width=30, relief=tk.SUNKEN, image=self.pnv)
        # lbl.image = self.img
        # lbl.grid(column=0, row=2, sticky='W')
        style_button = ttk.Style()
        style_button.configure('btn.TButton', font=("HELVETICA", 15), width=5)
        pcb = ttk.Button(self.tab2, text='+', compound='top', style='btn.TButton', image=self.pcb)
        pcb.image = self.pcb
        pcb.grid(column=1, row=2)
        pcq = ttk.Button(self.tab2, text='-', compound='top', style='btn.TButton', image=self.pcq)
        pcq.image = self.pcq
        pcq.grid(column=2, row=2)
        lpzb = ttk.Button(self.tab2, text=self.i18n.edit, compound='top', style='btn.TButton', image=self.lpz)
        lpzb.image = self.lpz
        lpzb.grid(column=3, row=2)
        eye = ttk.Button(self.tab2, text=self.i18n.details, compound='top', style='btn.TButton', image=self.ojo)
        eye.image = self.ojo
        eye.grid(column=4, row=2)
        self.inert_info()
        eye = ttk.Button(self.tab2, text=self.i18n.details, compound='top', style='btn.TButton', image=self.ojo)
        eye.image = self.ojo
        eye.grid(column=4, row=3)
        eye = ttk.Button(self.tab2, text=self.i18n.details, compound='top', style='btn.TButton', image=self.ojo)
        eye.image = self.ojo
        eye.grid(column=4, row=4)
        eye = ttk.Button(self.tab2, text=self.i18n.details, compound='top', style='btn.TButton', image=self.ojo)
        eye.image = self.ojo
        eye.grid(column=4, row=5)
        eye = ttk.Button(self.tab2, text=self.i18n.details, compound='top', style='btn.TButton', image=self.ojo)
        eye.image = self.ojo
        eye.grid(column=4, row=6)
        eye = ttk.Button(self.tab2, text=self.i18n.details, compound='top', style='btn.TButton', image=self.ojo)
        eye.image = self.ojo
        eye.grid(column=4, row=7)


    def create_tab2_test(self):
        """Crea el form de la tab2"""
        img1 = Image("photo", file="./Resources/pinguinoChef.png")
        lbl = ttk.Label(self.tab2, image=img1)
        lbl.image = img1
        lbl.grid(column=0, row=0, sticky='W')
        btn = ttk.Button(self.tab2, image=img1)
        btn.image = img1
        btn.grid(column=0, row=1)

    def test_toplevel(self):
        self.topl = Toplevel()
        self.topl.title(self.i18n.toplevel_title)
        # Se ejecuta el Toplevel como thread in daemon, padx=5, pady=5
        self.run_top = Thread(target=self.topl.mainloop())
        self.run_top.setDaemon(True)
        self.run_top.start()



app = Gui()
app.win.mainloop()
