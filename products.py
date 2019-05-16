import pickle
import os
import shutil
import tkinter as tk
from tkinter import ttk, Image, scrolledtext, Text
from message import MessagePopup
from Language import I18N


class PanqueModels:
    """ Clase de almacenamiendo y funciones CRUD de productos del Panque"""

    def __init__(self, root, parent, lang):
        """
        Primero se busca si existe la carpta de datos (bin) de no ser asi se crea.
        Segundo de busca si existe el archivo index.bin en la carpeta de datos, de no ser asi se crea.
        Al final se lee el archivo index y se establece el atributo current_index con el valor del
        archivo index.
        atributos:
        self.gui = parent es el parent del gui principal
        self.index es la bandera que marca si existe o no un index. Por defecto se inicia en False
        self.root_dir es el directorio actual donde se ejjecuta el projecto
        self.dirs es el nombre de la carpeta de datos
        self.dir_models es la ruta absoluta de la carpeta de datos
        """
        self.root = root
        self.gui = parent
        self.i18n = I18N(lang)
        self.index = False
        self.current_index = []
        self.root_dir = os.path.dirname(os.path.abspath(__file__))
        self.dirs = 'bin'
        self.search_or_make_dir('', self.dirs)
        self.dir_models = os.path.join(self.root_dir, self.dirs)
        self.search_index()
        self.load_index()
        self.pcbi = Image("photo", file="Resources/pinguinoChefPanbien.png")
        self.pcqi = Image("photo", file="Resources/pinguinoChefPanQuemado.png")
        self.lpzi = Image("photo", file="Resources/lapiz.png")
        self.ojoi = Image("photo", file="Resources/ojo.png")

    def search_index(self):
        """ Metodo que busca si existe el archivo de indice de productos (index.bin).
            De existir se marca la bandera self.index como True
        """
        with os.scandir(self.dir_models) as entries:
            for entry in entries:
                if entry.is_file():
                    if entry.name == 'index.bin':
                        self.index = True
                        break
            return self.index

    def search_or_make_dir(self, pat, direct):
        """Recibe la ruta donde se guardan los datos (pat) y el directorio a crear (direct).
            Si el pat es una cadena vacia quiere decir que se va a crear el directorio de datos(bin)
        """
        if pat != '':
            ruta = os.path.join(self.root_dir, pat)
        else:
            ruta = self.root_dir
        try:
            with os.scandir(ruta) as entries:
                ls = [dirs.name for dirs in entries if os.path.isdir(dirs)]
                if direct not in ls:
                    os.mkdir(os.path.join(ruta, direct))
        except NotADirectoryError:
            pass

    def load_index(self):
        """Metodo que lee o crea el indice de productos"""
        if self.index:
            with open(self.dir_models + '/index.bin', 'rb') as current:
                self.current_index = pickle.load(current)
        else:
            with open(self.dir_models + '/index.bin', 'wb') as current:
                pickle.dump(self.current_index, current)

    def update_index(self):
        """Metodo que actualiza el archivo del index a traves del
        valor del atributo current_index
        """
        try:
            with open(self.dir_models + '/index.bin', 'wb') as current:
                pickle.dump(self.current_index, current)
        except FileNotFoundError as fnfe:
            msg = MessagePopup(fnfe.errno, fnfe.strerror, 'e')
            msg()

    def create_product(self, name, description, cost, size, stock):
        """ Metodo que crea un nuevo producto. Actualiza el current_index
        con el nombre del producto a crear y despues ejecuta update_index
        """
        pdt = {'key': len(self.current_index) + 1, 'name': name, 'description': description, 'cost': cost, 'size': size,
               'stock': stock}
        self.search_or_make_dir(self.dir_models, str(name))
        ruta = os.path.join(self.dir_models, str(name))
        with open(ruta + '/' + str(name) + '.bin', 'wb') as product:
            pickle.dump(pdt, product)
            self.current_index += [name]
            self.update_index()

    def update_product(self, old_name, name, description, cost, size, stock):
        """Metodo que actualiza los datos de un producto"""
        pdtToUp = {'key': len(self.current_index) + 1, 'name': name, 'description': description, 'cost': cost,
                   'size': size,
                   'stock': stock}
        try:
            trash_dir = os.path.join(self.dir_models, str(name))
            shutil.rmtree(trash_dir)
            self.create_product(name, description, cost, size, stock)
        except OSError as rmex:
            msg = MessagePopup(rmex.errno, rmex.strerror, 'e')
            msg()
        except Exception as ex:
            msg = MessagePopup(ex.errno, ex.strerror, 'e')
            msg()


    def add_presentation(self):
        """Metodo que crea las presentaciones de los productos"""
        pass

    def read_product(self, name):
        """Lee un producto y retorna su valor"""
        ruta = os.path.join(self.dir_models, name) + '/'
        with open(ruta + name + '.bin', 'rb') as product:
            produc = pickle.load(product)
        return produc

    def print_product(self, name):
        """Imprime los datos de un producto"""
        pass

    def onDetails(self, event):
        n = str(event.widget)
        n = n[34:]
        self.root.new_p_toplevel(self.i18n.details, self.names[int(n)])

    def onEdit(self, event):
        n = str(event.widget)
        n = n[35:]
        self.root.new_p_toplevel(self.i18n.edit, self.names[int(n)])

    def onUpdate(self, event):
        n = str(event.widget)
        n = n[35:]
        produc = self.read_product(self.names[int(n)])
        self.update_product(self.names[int(n)], produc['name'], produc['description'], produc['cost'], produc['size'],
                            produc['stock']+1)
        self.root.actualizar_products()

    def onDown(self, event):
        n = str(event.widget)
        n = n[35:]
        produc = self.read_product(self.names[int(n)])
        if produc['stock'] < 1:
            stock = 0
        else:
            stock = produc['stock'] -1
        self.update_product(self.names[int(n)], produc['name'], produc['description'], produc['cost'], produc['size'],
                            stock)
        self.root.actualizar_products()

    def list_all_product(self):
        style_button = ttk.Style()
        style_button.configure('btn.TButton', font=("Cantarell", 15), width=5)
        try:
            with open(self.dir_models + '/index.bin', 'rb') as indx:
                all_p = pickle.load(indx)
            with os.scandir(self.dir_models) as entries:
                ls = [dirs.name for dirs in entries if os.path.isdir(dirs)]
            self.names = {}
            for d in ls:
                if d not in all_p:
                    ls.remove(d)
            for ds in ls:
                n = ls.index(ds) + 2
                with os.scandir(self.dir_models + '/' + ds) as entries:
                    for f in entries:
                        if os.path.isfile(f) and f.name == ds + '.bin':
                            with open(self.dir_models + '/' + ds + '/' + f.name, 'rb') as file:
                                dic = pickle.load(file)
                                self.names[n] = dic['name']
                                scrol_w = 30
                                scrol_h = 8
                                style_button = ttk.Style()
                                style_button.configure('btn.TButton', font=("Cantarell", 15), width=5)
                                # 1
                                self.lbl_name = Text(self.gui, wrap='word', background='aliceBlue', height=scrol_h,
                                                     width=scrol_w)
                                self.lbl_name.insert(tk.INSERT, dic['name'])
                                self.lbl_name.image_create("current", image=self.pcbi)
                                self.lbl_name.grid(column=0, row=n, sticky='W')
                                self.lbl_name.config(state='disabled')
                                # 2
                                self.pcb = ttk.Button(self.gui, name='b'+str(n), text='+', compound='top', image=self.pcbi,
                                                      style='btn.TButton')
                                self.pcb.image = self.pcbi
                                self.pcb.grid(column=1, row=n)
                                self.pcb.bind('<Button-1>', self.onUpdate)
                                self.pcq = ttk.Button(self.gui, name='c'+str(n), text='-', compound='top', style='btn.TButton',
                                                      image=self.pcqi)
                                self.pcq.image = self.pcqi
                                self.pcq.grid(column=2, row=n)
                                self.pcq.bind('<Button-1>', self.onDown)
                                # # 3
                                self.lpzb = ttk.Button(self.gui, name='a'+str(n), text=self.i18n.edit, image=self.lpzi,
                                                       style='btn.TButton', compound='top')
                                self.lpzb.image = self.lpzi
                                self.lpzb.grid(column=3, row=n)
                                self.lpzb.bind('<Button-1>', self.onEdit)
                                # #  4
                                self.eye = ttk.Button(self.gui, name=str(n), text=self.i18n.details, image=self.ojoi,
                                                      style='btn.TButton', compound='top')
                                self.eye.grid(column=4, row=n)
                                self.eye.bind('<Button-1>', self.onDetails)
                                # # 5
                                self.info_text = scrolledtext.ScrolledText(self.gui, wrap='word',
                                                                           background='aliceBlue',
                                                                           width=scrol_w,
                                                                           height=scrol_h)
                                self.info_text.insert(tk.INSERT, dic['description'])
                                self.info_text.insert(tk.END, '\n\nCosto: ')
                                self.info_text.insert(tk.CURRENT, dic['cost'])
                                self.info_text.insert(tk.END, '\nTamaño: ')
                                self.info_text.insert(tk.END, dic['size'])
                                self.info_text.insert(tk.END, '\nDisponibles: ', 'dis')
                                if dic['stock'] == 0:
                                    self.info_text.insert(tk.END, 'AGOTADO', 'cero')
                                else:
                                    self.info_text.insert(tk.END, dic['stock'], 'stock')
                                self.info_text.grid(column=5, row=n)
                                if dic['stock'] == 0:
                                    self.info_text.tag_config("cero", foreground="red")
                                else:
                                    self.info_text.tag_config("dis", foreground="green")
                                    self.info_text.tag_config("stock", foreground="green")
                                self.info_text.config(state='disabled')

        except Exception:
            pass


if __name__ == '__main__':
    app = PanqueModels('a', 'a', 'es')
    # app.create_product_test()
    app.save_image()
