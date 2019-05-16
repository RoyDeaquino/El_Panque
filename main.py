import tkinter as tk
import re
from tkinter import ttk, Image, Menu, Toplevel, scrolledtext, Text, Button
from Language import I18N
from Callbacks import Callbacks
from threading import Thread
from products import PanqueModels
from message import MessagePopup


class Gui(tk.Frame):
    """Clase que hereda de la clase Frame"""
    def __init__(self, root, language='es'):
        self.lang = language
        self.root = root
        tk.Frame.__init__(self, self.root)
        # Se llama al canvas
        self.create_frame_canvas()
        # Se crea i18n para internacionalizacion
        self.i18n = I18N(self.lang)
        # Se crea instancia del modelo
        # Se inicializan imagenes del GUI

        self.pnv = Image("photo", file="Resources/PinguinoNoVe.png")
        self.pc = Image("photo", file="Resources/pinguinoChef.png")

        self.img = Image("photo", file="Resources/panque.png")

        self.mas = Image("photo", file="Resources/mas.png")
        # Se establece propidades de root
        self.root.title(self.i18n.title)
        self.root.resizable(1,1)
        self.root.geometry("1200x700")
        self.root.tk.call('wm', 'iconphoto', self.root._w, self.img)
        # se llama al modulo callbacks
        self.call_backs = Callbacks(self)
        # Se llama a los widgets
        self.create_tabs()
        self.create_menubar()
        self.create_tab1()
        self.create_tab3()
        self.create_logo()
        self.total.set("300")
        self.tab_control.select(2)

    def create_frame_canvas(self):
        # Creacion del canvas y frame
        self.canvas = tk.Canvas(self.root, borderwidth=0, background="#ffff55")
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.vsb = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.root.bind("<Configure>", self.onTab)

    def onFrameConfigure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def onTab(self, event):
        self.tab_control.configure(width=self.canvas.winfo_width())
        if self.tab_control.winfo_height() < self.canvas.winfo_height():
            self.tab_control.configure( height=self.canvas.winfo_height()-24)

    def onSave(self, event):
        c, s = False, False
        patternStock = re.compile(r"^\b(10{0,2}|[1-9]{1,2})\b$")
        stock = self.stock.get()
        patternCost = re.compile(r"^\b([1-9][0-9]{0,3}|10000)\b$")
        cost = self.cost.get()
        matchCost = patternCost.search(cost)
        matchStock = patternStock.search(stock)
        print(matchCost, '-', matchStock)
        # if s != () & c != ():
        #     flag = True
        #     if matchCost == None:
        #         msg2 = MessagePopup(self.i18n.msgCostTitle, self.i18n.msgCostBody, 'w')
        #     else:
        #         msg = MessagePopup(self.i18n.msgStockTitle, self.i18n.msgStockBody, 'w')
        if matchCost:
            c = True
        else:
            msg2 = MessagePopup(self.i18n.msgCostTitle, self.i18n.msgCostBody, 'w')
            c= False

        if matchStock:
            s = True
        else:
            msg = MessagePopup(self.i18n.msgStockTitle, self.i18n.msgStockBody, 'w')
            s = False

        if c & s:
            self.model.create_product(self.name.get(), self.detail.get(), int(self.cost.get()), self.tam.get(),
                                      int(self.stock.get()))
            # actualizar tab 3
            self.actualizar_products()
            self.topl.destroy()
        else:
            # Redibuja el formulario
            name = self.name.get()
            detail = self.detail.get()
            cost = self.cost.get()
            tam = self.tam.get()
            stock = self.stock.get()
            dic = {'name': name, 'description': detail, 'cost': cost, 'size': tam, 'stock': stock, 'valid': 'new'}
            self.actualizar_products()
            self.topl.destroy()
            self.name.set(' ')
            self.detail.set(' ')
            self.cost.set(' ')
            self.tam.set(' ')
            self.stock.set(' ')
            self.new_p_toplevel('redraw', dic)

    def onEdit(self):
        self.model.update_product(self.name_edit, self.name.get(), self.detail.get(), int(self.cost.get()), self.tam.get(),
                                  int(self.stock.get()))
        self.actualizar_products()
        self.topl.destroy()

    def close_details(self):
        self.actualizar_products()
        self.topl.destroy()

    def create_tabs(self):
        """Crea las pestañas (notebook) del frame"""
        st = ttk.Style()
        st.configure('tab.TNotebook', font=('Z003', 30, 'bold'), foreground='green')
        self.tab_control = ttk.Notebook(self.frame,  style='tab.TNotebook')
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab1, text=self.i18n.tab1Text)
        #self.tab_control.pack(expand=1, fill="both")

        self.tab2 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab2, text=self.i18n.pedidos)
        #self.tab_control.pack(expand=1, fill="both")

        self.tab3 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab3, text=self.i18n.store)
        #self.tab_control.pack(expand=1, fill="both")
        self.tab_control.grid(column=0, row=0, sticky="ew")

    def del_tabs(self):
        self.tab_control.destroy()

    def change_language(self, language):
        self.i18n.__init__(language)
        self.del_tabs()
        self.create_tabs()
        self.create_menubar()
        self.create_logo()
        self.create_tab1()
        self.create_tab3()

    def create_menubar(self):
        """Crea el MenuBar del frame"""
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)
        pedidos_menu = Menu(menu_bar, tearoff=0)
        pedidos_menu.add_command(label=self.i18n.new)
        pedidos_menu.add_command(label=self.i18n.list)
        pedidos_menu.add_command(label=self.i18n.search)
        pedidos_menu.add_separator()
        pedidos_menu.add_command(label=self.i18n.exit, command=self.call_backs._quit)
        menu_bar.add_cascade(label=self.i18n.pedidos, menu=pedidos_menu)

        store_menu = Menu(menu_bar, tearoff=0)
        store_menu.add_command(label=self.i18n.new_product, command=lambda: self.new_p_toplevel(
                                self.i18n.new_product, ' '))
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
            el_panque = ttk.Label(tab, text=self.i18n.title, font=("Z003", 50), image=self.img, compound='right', relief=tk.SUNKEN)
            el_panque.image = self.img
            el_panque.grid(column=0, row=0, columnspan=3)

    def logo_top(self):
        """Set the logo in the Toplevel widget"""
        el_panque = ttk.Label(self.topl, text=self.i18n.title, font=("Z003", 50), image=self.img, compound='right',
                              relief=tk.SUNKEN)
        el_panque.image = self.img
        el_panque.grid(column=0, row=0, columnspan=3)

    def create_tab1(self):
        """Crea el form principal de la caja"""
        self.art = ttk.Treeview(self.tab1, columns=(self.i18n.product, self.i18n.amount, self.i18n.cost), height=25)
        self.art.heading("#0", text="N.")
        self.art.column("#0", minwidth=10, anchor=tk.W, stretch=tk.NO)
        self.art.heading(self.i18n.product, text=self.i18n.product)
        self.art.column(self.i18n.product, minwidth=200, anchor=tk.CENTER, stretch=tk.NO)
        self.art.heading(self.i18n.amount, text=self.i18n.amount)
        self.art.column(self.i18n.amount, minwidth=50, anchor=tk.W, stretch=tk.NO)
        self.art.heading(self.i18n.cost, text=self.i18n.cost)
        self.art.column(self.i18n.cost, minwidth=50, anchor=tk.W, stretch=tk.NO)
        self.art.grid(column=0, row=1, columnspan=6, rowspan=6)
        # Inicia lado derecho
        ttk.Label(self.tab1, text=self.i18n.total,
                  font=("Source Code Pro Black", 30), relief=tk.SUNKEN).grid(column=11, row=1, sticky='N')
        self.total = tk.StringVar()
        self.total_entry = ttk.Entry(self.tab1, width=10, textvariable=self.total, justify=tk.CENTER,
                                     font=("Cantarell", 30), state=tk.DISABLED)
        self.total_entry.grid(column=11, row=2)

        ttk.Label(self.tab1, text=self.i18n.cash,
                  font=("Source Code Pro Black", 30)).grid(column=11, row=3)
        self.cash = tk.StringVar()
        self.cash_entry = ttk.Entry(self.tab1, width=10, textvariable=self.cash, justify=tk.CENTER,
                                    font=("Cantarell", 30)).grid(column=11, row=4)

        ttk.Label(self.tab1, text=self.i18n.change,
                  font=("Source Code Pro Black", 30)).grid(column=11, row=5)

        self.change = tk.StringVar()
        self.change_entry = ttk.Entry(self.tab1, width=10, textvariable=self.change, justify=tk.CENTER,
                                      font=("Cantarell", 35), state=tk.DISABLED)
        self.change_entry.grid(column=11, row=6)

    def insert_header(self):
        ttk.Label(self.tab3, text=self.i18n.products,
                  font=("Cantarell", 20)).grid(column=0, row=1, columnspan=1)
        ttk.Label(self.tab3, text=self.i18n.stock,
                  font=("Cantarell", 20), width=10).grid(column=1, row=1, sticky=tk.W, columnspan=2)
        ttk.Label(self.tab3, text=self.i18n.edit, font=("Cantarell", 20), width=6,
                  ).grid(column=3, row=1)
        ttk.Label(self.tab3, text=self.i18n.details, font=("Cantarell", 20), width=10,
                  ).grid(column=4, row=1)
        ttk.Label(self.tab3, text=self.i18n.info, font=("Cantarell", 20), width=20,
                  ).grid(column=5, columnspan=2, row=1)

    # def insert_propiedades(self):
    #
    #     # foto del producto
    #     self.model.lbl_name.image_create("current", image=self.pnv)
    #     # imagen del boton +
    #     self.model.pcb.configure(image=self.pcb)
    #     # imagen del boton -
    #     self.model.pcq.configure(image=self.pcq)
    #     # imagen lapiz
    #     self.model.lpzb.configure(image=self.lpz, text=self.i18n.edit, style='btn.TButton')
    #     # imagen de ojo
    #     self.model.eye.configure(command=lambda: self.new_p_toplevel(self.i18n.details, ' '))

    def actualizar_products(self):
        self.model = PanqueModels(self, self.tab3, self.lang)
        self.insert_header()
        self.name_data = self.model.list_all_product()

    # def insert_info(self):
    #     """Inserta la informacion de los productos"""
    #     descrip = "Delciciosa rebanada de pastel\nde tres leches sabor cajeta\ncon trozos de nuez."
    #     cost = "\nCosto: 120"
    #     size = "\nTamaño: Rebanada para 1 persona"
    #     stock= "\n\nAGOTADO"
    #     scrol_w = 30;
    #     scrol_h = 8
    #     style_button = ttk.Style()
    #     style_button.configure('btn.TButton', font=("Cantarell", 15), width=5)
    #     # 1
    #     self.lbl_name = Text(self.tab3, wrap='word', background='aliceBlue', height=scrol_h, width=scrol_w)
    #     self.lbl_name.insert(tk.INSERT, 'Pastel de cajeta rebanado')
    #     self.lbl_name.image_create("current", image=self.pnv)
    #     self.lbl_name.grid(column=0, row=2, sticky='W')
    #     self.lbl_name.config(state='disabled')
    #     # 2
    #     pcb = ttk.Button(self.tab3, text='+', compound='top', style='btn.TButton', image=self.pcb)
    #     pcb.image = self.pcb
    #     pcb.grid(column=1, row=2)
    #     pcq = ttk.Button(self.tab3, text='-', compound='top', style='btn.TButton', image=self.pcq)
    #     pcq.image = self.pcq
    #     pcq.grid(column=2, row=2)
    #     # 3
    #     lpzb = ttk.Button(self.tab3, text=self.i18n.edit, compound='top', style='btn.TButton', image=self.lpz)
    #     lpzb.image = self.lpz
    #     lpzb.grid(column=3, row=2)
    #     # 4
    #     eye = ttk.Button(self.tab3, text=self.i18n.details, compound='top', style='btn.TButton', image=self.ojo,
    #                      command=lambda: self.new_p_toplevel(self.i18n.details, ' '))
    #     eye.image = self.ojo
    #     eye.grid(column=4, row=2)
    #     # 5
    #     info_text = scrolledtext.ScrolledText(self.tab3, wrap='word', background='aliceBlue', width=scrol_w,
    #                                           height=scrol_h)
    #     info_text.insert(tk.INSERT, descrip)
    #     info_text.insert(tk.END, cost)
    #     info_text.insert(tk.END, size)
    #     info_text.insert(tk.END, stock)
    #     info_text.grid(column=5, row=2)
    #     info_text.tag_add("stock", "7.0", "7.7")
    #     info_text.tag_config("stock", foreground="red")
    #     info_text.config(state='disabled')
    #     self.model = PanqueModels(self.tab3)
    #     self.model.list_all_product()
    #     self.insert_propiedades()

    def create_tab3(self):
        """Crea el form del tab2"""
        # Header
        self.actualizar_products()
        btn_mas_style = ttk.Style()
        btn_mas_style.configure('btn_mas.TButton', font=("Source Code Pro Semibold", 20))
        mas = ttk.Button(self.tab3, text=self.i18n.new, width=6, image=self.mas, compound='top',
                         style='btn_mas.TButton', command=lambda: self.new_p_toplevel(self.i18n.new_product, ' '))
        mas.image = self.mas
        mas.grid(column=7, row=1, rowspan=2)
        pc_lbl = ttk.Label(self.tab3, image=self.pc)
        pc_lbl.image = self.pc
        pc_lbl.grid(column=7, row=3, rowspan=3)

    def form_details(self, name):
        produc = self.model.read_product(name)
        self.form_new_product()
        self.name.set(produc['name'])
        self.detail.set(produc['description'])
        self.cost.set(produc['cost'])
        self.tam.set(produc['size'])
        self.stock.set(produc['stock'])
        self.btn_save.configure(state='disabled')
        self.btn_save.grid_forget()
        self.btn_close = ttk.Button(self.topl, text=self.i18n.close, command=lambda: self.topl.destroy())
        lblimg = Image('photo', file='/home/jintan/PycharmProjects/El_Panque/pin.png')
        lbl_img = ttk.Label(self.topl, image=lblimg)
        lbl_img.image = lblimg
        lbl_img.grid(column=2, row=0, rowspan=7)
        self.btn_close.grid(column=2, row=7, sticky=tk.SE)

    def form_edit(self, name):
        self.form_details(name)
        self.name_edit = name
        self.btn_close.configure(state='disabled')
        self.btn_close.grid_forget()
        self.btn_edit = ttk.Button(self.topl, text=self.i18n.edit, command=self.onEdit)
        self.btn_edit.grid(column=2, row=7, sticky=tk.SE)
        # self.btn_edit.bind("<Button-1>", self.onEdit)

    def redraw(self, name):
        produc = name
        self.form_new_product()
        self.name.set(produc['name'])
        self.detail.set(produc['description'])
        self.cost.set(produc['cost'])
        self.tam.set(produc['size'])
        self.stock.set(produc['stock'])
        if produc['valid'] == 'edit':
            pass


    def form_new_product(self):
        # Form name
        ttk.Label(self.topl, text=self.i18n.name, font=("Cantarell", 15)).grid(column=0, row=1)
        self.name = tk.StringVar()
        self.name_entry = ttk.Entry(self.topl, textvariable=self.name, font=("Cantarell", 10), width=30)
        self.name_entry.grid(column=1,row=1)
        self.name_entry.focus()
        # details
        ttk.Label(self.topl, text=self.i18n.details, font=("Cantarell", 15)).grid(column=0, row=2)
        self.detail = tk.StringVar()
        self.details_entry = ttk.Entry(self.topl, textvariable=self.detail,
                                       font=("Cantarell", 10), width=30).grid(column=1, row=2)
        # cost
        ttk.Label(self.topl, text=self.i18n.cost, font=("Cantarell", 15)).grid(column=0, row=3)
        self.cost = tk.StringVar()
        self.cost_entry = ttk.Entry(self.topl, textvariable=self.cost, font=("Cantarell", 10), width=30).grid(column=1,
                                                                                                              row=3)
        # size
        ttk.Label(self.topl, text=self.i18n.sizes, font=("Cantarell", 15)).grid(column=0, row=4)
        self.tam = tk.StringVar()
        self.tam_entry = ttk.Entry(self.topl, textvariable=self.tam, font=("Cantarell", 10), width=30).grid(column=1,
                                                                                                            row=4)
        # stock
        ttk.Label(self.topl, text=self.i18n.stock, font=("Cantarell", 15)).grid(column=0, row=5)
        self.stock = tk.StringVar()
        self.stock_entry = ttk.Entry(self.topl, textvariable=self.stock, font=("Cantarell", 10), width=30).grid(column=1
                                                                                                                , row=5)
        # save
        self.btn_save = ttk.Button(self.topl, text=self.i18n.save)
        self.btn_save.grid(column=1, row=7, sticky=tk.SE)
        self.btn_save.bind("<Button-1>", self.onSave)


    def new_p_toplevel(self, form, name):
        self.topl = Toplevel()
        self.topl.title(form)
        self.topl.tk.call('wm', 'iconphoto', self.topl._w, self.img)
        self.logo_top()
        if form == self.i18n.new_product:
            self.form_new_product()
        elif form == self.i18n.details:
            self.form_details(name)
        elif form == self.i18n.edit:
            self.form_edit(name)
        elif form == 'redraw':
            if name['valid'] == self.i18n.edit:
                self.topl.title(self.i18n.edit)
            else:
                self.topl.title(self.i18n.new_product)
            self.redraw(name)
        # Se ejecuta el Toplevel como thread in daemon, padx=5, pady=5
        self.run_top = Thread(target=self.topl.mainloop())
        self.run_top.setDaemon(True)
        self.run_top.start()


if __name__ == "__main__":
    root = tk.Tk()
    Gui(root).pack(side="top", fill="both", expand=True)
    root.mainloop()#self.info_text.tag_add("cero", "7.0", "7.7")
